import requests
import logging
import sys
import os

VERSION = os.getenv("VERSION")
SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")

log_format = "%(asctime)s - %(levelname)s - %(process)d/%(threadName)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

expected_resp = {
    "model": "ML",
    "statusCode": 200,
    "version": VERSION
}


def main():
    resp = requests.post(SERVICE_ENDPOINT).json()

    if resp == expected_resp:
        logging.info("Response:\n {}.".format(resp))
        sys.exit(0)
    else:
        logging.info("Unexpected Response:\n {}.".format(resp))
        sys.exit(1)


if __name__ == '__main__':
    main()
