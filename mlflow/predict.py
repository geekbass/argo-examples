import random
import requests
import json


def main():
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

    # Create sample JSON data to post to model
    data = {"fixed_acidity": fixed_acidity, "volatile_acidity": volatile_acidity, "citric_acid": citric_acid,
            "residual_sugar": residual_sugar, "chlorides": chlorides, "free_sulfur_dioxide": free_sulfur_dioxide,
            "total_sulfur_dioxide": total_sulfur_dioxide, "density": density, "ph": ph, "sulfates": sulfates,
            "alcohol": alcohol}

    # Post the random Data and print the result
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://localhost:5000/predict", data=json.dumps(data), headers=headers).json()
    print(r)


if __name__ == "__main__":
    main()
