# SQL Injection Detection System

This project is a simple HTTP proxy that detects and blocks potential SQL injection attempts. It inspects incoming HTTP requests and classifies them as "Good" or "Bad" based on the presence of known SQL injection patterns.

## Features

- Extracts features from HTTP requests to detect SQL injection.
- Classifies requests using a simple heuristic-based approach.
- Logs and blocks suspicious requests.

## Project Structure

sqli_detection_system/
│
├── src/
│   ├── main.py              # Entry point for the application
│   ├── server.py            # Server setup and running logic
│   ├── proxy_handler.py     # HTTP proxy and request classification logic
│   ├── classifier.py        # Feature extraction and classification logic
│   └── logger.py            # Logging configuration
│
├── .env                     # Environment variables
├── .gitignore               # Files and directories to be ignored by Git
├── README.md                # Project documentation

## this project is not design for handling https requests. It is a mini project and needs furthur improvements.