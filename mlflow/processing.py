"""
This file acts as a data processing task in an ML Pipeline. This generates random data for training but would likely
be some other kind of process such as downloading data, scraping data, processing data, uploading it elsewhere etc...
"""

import random
import csv


def main():
    # CSV Columns
    columns = ["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide",
               "total sulfur dioxide", "density", "pH", "sulphates", "alcohol", "quality"]

    # Initialize List of rows
    rows = []

    # Generate some random Data
    for rand_row in range(1000):
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
        quality = round(random.randint(5, 10))

        row = [fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide,
               total_sulfur_dioxide, density, ph, sulfates, alcohol, quality]

        rows.append(row)

    with open("/work/mlflow/wine_data.csv", 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, delimiter=';')

        # writing the fields
        csvwriter.writerow(columns)

        # writing the data rows
        csvwriter.writerows(rows)


if __name__ == "__main__":
    main()
