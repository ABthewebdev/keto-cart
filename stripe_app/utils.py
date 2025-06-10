import stripe

def get_product_details(product):
    price_id = product.get("default_price")

    if not price_id:
        raise ValueError(f"Product {product['id']} has no default_price set.")

    price = stripe.Price.retrieve(price_id)

    return {
        'id': product['id'],
        'name': product.get('name', 'Unnamed Product'),
        'image': product.get('images', [''])[0] if product.get('images') else '',
        'description': product.get('description', ''),
        'price': price['unit_amount'] / 100 if price.get('unit_amount') else 0
    }
