def calculate_sale(count, total_price):
    if 100000 <= count <= 150000:
        total_price = round(total_price * 0.9)
    elif 150000 < count <= 200000:
        total_price = round(total_price * 0.85)
    elif 200000 < count:
        total_price = round(total_price * 0.8)
    return total_price