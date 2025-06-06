import stripe

def product_details(product):
    prices = stripe.Price.list(product=product['id'])
    price = prices['data'][0]
    product_details = {
        'id': product['id'],
        'name': product['name'],
    }
    return product_details