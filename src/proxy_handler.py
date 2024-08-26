from http.server import SimpleHTTPRequestHandler
from urllib import request, error, parse
import logging
from classifier import ExtractFeatures, classify_query

class SimpleHTTPProxy(SimpleHTTPRequestHandler):
    proxy_routes = {}

    @classmethod
    def set_routes(cls, proxy_routes):
        cls.proxy_routes = proxy_routes

    def do_GET(self):
        parts = self.path.split('/')
        logging.info(f'Path parts: {parts}')

        if len(parts) > 2 and parts[2] == '127.0.0.1:8080':
            self.send_error(400, "Bad request")
            return

        try:
            live_data = ExtractFeatures(parts[3])
            classification = classify_query(live_data)
            logging.info(f'Query classification: {classification}')

            if classification == "Bad":
                logging.info("Intrusion Detected")
                self.send_error(400, "Intrusion Detected")
                return

        except Exception as e:
            logging.error(f'Error during classification: {e}')
            self.send_error(500, f'Error during classification: {e}')
            return

        if len(parts) >= 2:
            target_url = 'http://' + parts[2] + '/' + '/'.join(parts[3:])
            self.proxy_request(target_url)
        else:
            super().do_GET()

    def do_POST(self):
        parts = self.path.split('/')
        logging.info(f'Path parts: {parts}')

        if len(parts) > 2 and parts[2] == '127.0.0.1:8080':
            self.send_error(400, "Bad request")
            return

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            live_data = ExtractFeatures(parts[3], post_data)
            classification = classify_query(live_data)
            logging.info(f'Query classification: {classification}')

            if classification == "Bad":
                logging.info("Intrusion Detected")
                self.send_error(400, "Intrusion Detected")
                return

        except Exception as e:
            logging.error(f'Error during classification: {e}')
            self.send_error(500, f'Error during classification: {e}')
            return

        if len(parts) >= 2:
            target_url = 'http://' + parts[2] + '/' + '/'.join(parts[3:])
            self.proxy_request(target_url, method="POST", post_data=post_data)
        else:
            super().do_POST()

    def proxy_request(self, url, method="GET", post_data=None):
        logging.info(f'Proxying request to: {url} with method: {method}')
        
        data = post_data.encode('utf-8') if post_data else None
        req = request.Request(url, data=data, method=method)
        
        try:
            with request.urlopen(req) as response:
                self.send_response(response.status)
                for name, value in response.headers.items():
                    self.send_header(name, value)
                self.end_headers()

                self.copyfile(response, self.wfile)

        except error.HTTPError as e:
            logging.error(f'HTTP error occurred: {e.code} - {e.reason}')
            self.send_response(e.code)
            self.end_headers()

        except error.URLError as e:
            logging.error(f'URL error occurred: {e.reason}')
            self.send_response(500)
            self.end_headers()

        except Exception as e:
            logging.error(f'Unexpected error occurred: {e}')
            self.send_response(500)
            self.end_headers()

    def send_error(self, code, message=None):
        self.log_error("code %d, message %s", code, message)
        self.send_response_only(code)
        self.send_header('Content-Type', self.error_content_type)
        self.end_headers()
        if message:
            self.wfile.write(message.encode('utf-8'))

    def do_CONNECT(self):
        self.send_error(501, "Unsupported method ('CONNECT')")
