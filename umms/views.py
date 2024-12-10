from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Food, Messages, Order, Cart
from .forms import FoodForm
from django.contrib.auth.decorators import login_required
# views.py (checkout section)
import requests







def view_cart(request):
    """
    View to display the cart items and their total price.
    Retrieves cart data from the session and calculates the total price.
    """
    # Retrieve cart data from the session, defaulting to an empty list if not found
    cart_items = request.session.get('cart', [])

    # Initialize the total price
    total_price = 0
    processed_cart_items = []

    # Process each item to calculate totals
    for item in cart_items:
        if isinstance(item, dict):  # Validate item is a dictionary
            try:
                price = float(item.get('price', 0))
                quantity = int(item.get('quantity', 0))
                item_total = price * quantity

                # Add item details and total to processed list
                processed_cart_items.append({
                    'name': item.get('name', 'Unknown Item'),
                    'price': price,
                    'quantity': quantity,
                    'total_price': round(item_total, 2),
                })

                # Increment the total cart price
                total_price += item_total
            except (ValueError, TypeError) as e:
                # Log or skip invalid items
                print(f"Invalid item in cart: {item}. Error: {e}")
                continue

    # Pass processed items and total price to the template
    return render(request, 'view_cart.html', {
        'cart_items': processed_cart_items,
        'total_price': round(total_price, 2),
    })

def checkout(request):
    # Your checkout logic
    return redirect('payment_success')

def payment_success(request):
    # Add your view logic here
    return render(request, 'payment_success.html')

@login_required
def checkout(request):
    # Sample data for STK Push
    phone_number = request.user.profile.phone_number  # Assuming you have a user profile with a phone number
    amount = sum(item.total_price() for item in Cart.objects.filter(user=request.user))

    # Example of an STK push (this will depend on your payment API provider)
    response = requests.post('https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json={
        "phone_number": phone_number,
        "amount": amount,
        # Other necessary parameters for the API
    })

    if response.status_code == 200:
        return redirect('payment_success')
    else:
        return redirect('payment_failed')


def menus(request):
    foods = Food.objects.all()
    return render(request, 'menus.html', {'foods': foods})


def add_to_cart(request, food_id):
    # Step 1: Fetch the food item from the database using its ID
    try:
        food = Food.objects.get(id=food_id)  # Get the food item by ID from the database
    except Food.DoesNotExist:
        return redirect('error_page')  # Handle the case when the food item is not found

    # Step 2: Retrieve the current cart from the session (or initialize it if not present)
    cart = request.session.get('cart', [])

    # Step 3: Check if the item is already in the cart
    item_in_cart = next((item for item in cart if item['id'] == food.id), None)

    if item_in_cart:
        # If the item is already in the cart, increase the quantity
        item_in_cart['quantity'] += 1
    else:
        # If the item is not in the cart, add it with a quantity of 1
        cart.append({
            'id': food.id,
            'name': food.name,
            'price': food.price,  # Assuming food items have a price field
            'quantity': 1
        })

    # Step 4: Save the updated cart back to the session
    request.session['cart'] = cart

    # Step 5: Calculate the total price of the items in the cart
    total = sum(item['price'] * item['quantity'] for item in cart)

    # Step 6: Optionally, pass the cart and total to the template for display
    return redirect('cart')  # Redirect to the cart view (to display the cart details)


def cart(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', [])
    # Calculate the total price of the items in the cart
    total = sum(item['price'] * item['quantity'] for item in cart)

    return render(request, 'view_cart.html', {'cart': cart, 'total': total})
@login_required
def checkout(request):
    # Code to handle STK push goes here
    return redirect('payment_success')


from umms.models import Food  # Replace `your_app` with your app name
Food.objects.all()  # This should list all saved food items

def menu(request):
    foods = Food.objects.all()
    return render(request, 'base.html', {'foods': foods})

@staff_member_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to the menu page after adding
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form})

@staff_member_required
def edit_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = FoodForm(instance=food)
    return render(request, 'edit_food.html', {'form': form, 'food': food})

@staff_member_required
def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect('menu')  # Redirect to the menu page after deleting


# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(name, email, subject, message)
        Messages.objects.create(name=name, email=email, subject=subject, message=message)
        return render(request, 'contact.html', {'message': 'Your message has been sent!'})
    else:
        return render(request, 'contact.html' )

def faq(request):
    return render(request, 'faq.html')

def orders(request):
    # Handle only GET requests for now
    if request.method == "GET":
        # Query all orders from the database
        all_orders = Order.objects.all()

        # Transform the orders into a list of dictionaries for easy rendering
        orders_data = [
            {
                "id": order.id,
                "food_name": order.food.name,
                "customer_name": order.customer_name,
                "status": order.status,
                "price": order.food.price,
                "order_date": order.order_date,
            }
            for order in all_orders
        ]
        print(orders_data)  # Debugging print statement

        # Render the menus.html template with orders data
        return render(request, 'menus.html', {'orders': orders_data})


def menus(request):
    if request.method == "GET":
        foods = Food.objects.all()
        foods_dict = {food.id: food.name for food in foods}
        print(foods_dict)
        return render(request, 'menus.html', {'foods': foods})


def signup(request):
    return render(request, 'signup.html' )
def signin(request):
    return render(request, 'signin.html')





