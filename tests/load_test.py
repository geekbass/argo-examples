"""
Example used for load testing
"""
from locust import HttpUser, task, between
import os
import random
import json

SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def on_start(self):
        # Based on the min and max values for each column. Randomly generated.
        fixed_acidity = round(random.uniform(4, 15), 1)
        volatile_acidity = round(random.uniform(0, 1.6), 2)
        citric_acid = round(random.uniform(0, 1), 2)
        residual_sugar = round(random.uniform(0.9, 15.5), 1)
        chlorides = round(random.uniform(0.12, 0.611), 3)
        free_sulfur_dioxide = round(random.randint(1, 72))
        total_sulfur_dioxide = round(random.randint(6, 289))
        density = round(random.uniform(0.990, 1.003), 3)
        ph = round(random.uniform(2.74, 4.01), 2)
        sulfates = round(random.uniform(0.33, 2), 2)
        alcohol = round(random.uniform(8.4, 14.9), 1)


        data = {"fixed_acidity": fixed_acidity, "volatile_acidity": volatile_acidity, "citric_acid": citric_acid,
                "residual_sugar": residual_sugar, "chlorides": chlorides, "free_sulfur_dioxide": free_sulfur_dioxide,
                "total_sulfur_dioxide": total_sulfur_dioxide, "density": density, "ph": ph, "sulfates": sulfates,
                "alcohol": alcohol}

        headers = {'Content-type': 'application/json'}

        self.client.post("http://tests/predict", data=json.dumps(data), headers=headers)

