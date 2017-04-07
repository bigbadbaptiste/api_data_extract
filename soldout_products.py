import requests
import csv


def get_products():
    filename = "C:\\Users\\hausmannb\\Google Drive\\SEO\\D. Special Ops & Temp" \
               "\\20170201- Uplift COCR Magazine DE\\Data\\" \
               "Product list_complete_20170405(2).csv"
    with open(filename) as openFile:
        reader = csv.reader(openFile)
        for line in reader:
            url = line[0]
            data = requests.get(url).json()
            products = data['products']
            if not products:
                continue
            else:
                yield products[0]


def main():
    headers = [
        "products.id",
        "products.url_key",
        "products.available",
        "products.vertical",
        "products.brand_id",
        "products.price"
    ]

    filename = 'soldOut_products.csv'
    with open(filename, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';')
        writer.writerow(headers)
        for product in get_products():
            writer.writerow([
                product['id'],
                product['url_key'],
                product['available'],
                product['vertical'],
                product['brand_id'],
                product['price'],
            ])


if __name__ == '__main__':
    main()