"""
This would be better served as a unit test or load test but is used as an example in the pipeline.
"""
import requests
import logging
import sys
import os
import json

VERSION = os.getenv("VERSION")
SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")

log_format = "%(asctime)s - %(levelname)s - %(process)d/%(threadName)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

data = {'fixed_acidity': 4.2, 'volatile_acidity': 0.37, 'citric_acid': 0.63, 'residual_sugar': 9.7, 'chlorides': 0.606,
        'free_sulfur_dioxide': 62, 'total_sulfur_dioxide': 276, 'density': 0.997, 'ph': 3.73, 'sulfates': 1.45,
        'alcohol': 12.9}

headers = {'Content-type': 'application/json'}


def main():
    resp = requests.post(SERVICE_ENDPOINT, data=json.dumps(data), headers=headers).status_code
    print(resp)

    if resp == 200:
        logging.info("Response:\n {}.".format(resp))
        sys.exit(0)
    else:
        logging.info("Unexpected Response:\n {}.".format(resp))
        sys.exit(1)


if __name__ == '__main__':
    main()
