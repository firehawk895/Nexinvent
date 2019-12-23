from .models import Product
import csv


def csv_parser():
    with open('data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 1
        for row in reader:
            try:
                print(count, row['supplier'], row['product'], row['sku'], row['unit'], row['description'], row['price'])
                count +=1
                Product.objects.create(supplier_id=row['supplier'], name=row['product'], sku=row['sku'], price=float(row['price']))
            except Exception as e:
                print(e)
                print("^^^^^^^^^ PROBLEM ROW^^^^^^^")


