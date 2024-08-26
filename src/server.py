import os
import logging
from http.server import HTTPServer
from dotenv import load_dotenv
from proxy_handler import SimpleHTTPProxy
from logger import configure_logging

# Load environment variables from .env file
load_dotenv()

def run(server_class=HTTPServer, handler_class=SimpleHTTPProxy, port=int(os.getenv("PORT", 8082))):
    configure_logging()
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Starting HTTP server on {server_address}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping HTTP server')
