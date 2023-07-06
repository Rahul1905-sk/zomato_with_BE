 
import pickle
from flask import Flask, jsonify, request
 

app = Flask(__name__)
 


@app.route('/')
def index():
    return 'Welcome to Zesty Zomato!'
 

 
def load_menu_data():
    try:
        with open('menu.pkl', 'rb') as menu_file:
            menu_data = pickle.load(menu_file)
    except FileNotFoundError:
        
        menu_data = []
    return menu_data

 
def save_menu_data(menu_data):
    with open('menu.pkl', 'wb') as menu_file:
        pickle.dump(menu_data, menu_file)
 
def generate_unique_id(menu_data):
    if menu_data:
        max_id = max(dish['id'] for dish in menu_data)
        return max_id + 1
    else:
        return 1
 
@app.route('/addDish', methods=['POST'])
def add_dish():
    dish = request.get_json()

    menu_data = load_menu_data()
     
    dish['id'] = generate_unique_id(menu_data)
     
    menu_data.append(dish)
     
    save_menu_data(menu_data)
    
    return jsonify({'message': 'Dish added successfully', 'dish': dish}), 201
 
@app.route('/menu', methods=['GET'])
def get_menu():
    menu_data = load_menu_data()
    return jsonify(menu_data)
 
@app.route('/deleteMenu/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    menu_data = load_menu_data()
     
    deleted_dish = None
    for dish in menu_data:
        if dish['id'] == dish_id:
            deleted_dish = dish
            menu_data.remove(dish)
            break
     
    save_menu_data(menu_data)
    
    if deleted_dish:
        return jsonify({'message': 'Dish deleted successfully', 'deleted_dish': deleted_dish})
    else:
        return jsonify({'message': 'Dish not found'}), 404



@app.route('/updateMenu', methods=['PATCH', 'PUT'])

def update_dish():
    dish_updates = request.get_json()

    menu_data = load_menu_data()

    for existing_dish in menu_data:
        if existing_dish['id'] == dish_updates['id']:
            existing_dish.update(dish_updates)
            break

    save_menu_data(menu_data)

    return jsonify({'message': 'Dish updated successfully'}), 200

## all crud operation ends from admin side
 

def load_orders():
    try:
        with open('orders.pkl', 'rb') as orders_file:
            orders = pickle.load(orders_file)
    except FileNotFoundError:
        orders = []
    return orders

def save_orders(orders):
    with open('orders.pkl', 'wb') as orders_file:
        pickle.dump(orders, orders_file)

# def update_order_ids(orders):
#     for i, order in enumerate(orders, start=1):
#         order['order_id'] = i

def calculate_order_total(order):
    total_price = 0.0
    for item in order['items']:
        price = item['price']
        quantity = item['quantity']
        item_total = price * quantity
        total_price += item_total
    return total_price

def calculate_customer_total(customer_name, orders):
    customer_total = 0.0
    for order in orders:
        if order['customer_name'] == customer_name:
            customer_total += order['total_price']
    return customer_total

@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()

    orders = load_orders()

    order_id = len(orders) + 1
    customer_name = order_data['customer_name']
    items = order_data['items']
    status = 'received'

    new_order = {
        'order_id': order_id,
        'customer_name': customer_name,
        'items': items,
        'status': status
    }

    orders.append(new_order)

    save_orders(orders)

    total_price = calculate_order_total(new_order)
    new_order['total_price'] = total_price

    return jsonify({'message': 'Order created successfully', 'order': new_order}), 201

@app.route('/orders/<int:order_id>', methods=['PUT', 'PATCH'])
def update_order_status(order_id):
    order_data = request.get_json()

    orders = load_orders()

    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = order_data['status']
            break

    save_orders(orders)

    return jsonify({'message': 'Order status updated successfully'}), 200

# @app.route('/orders/<int:order_id>', methods=['DELETE'])
# def delete_order(order_id):
#     orders = load_orders()

#     for order in orders:
#         if order['order_id'] == order_id:
#             orders.remove(order)
#             save_orders(orders)
#             # update_order_ids(orders)
#             return jsonify({'message': 'Order deleted successfully'}), 200

#     return jsonify({'message': 'Order not found'}), 404

@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = load_orders()
    return jsonify(orders), 200

# @app.route('/customers/<string:customer_name>/total', methods=['GET'])
# def get_customer_total(customer_name):
#     orders = load_orders()
#     customer_total = calculate_customer_total(customer_name, orders)
#     return jsonify({'customer_name': customer_name, 'total_price': customer_total}), 200










if __name__ == '__main__':
    app.run(debug=True)
