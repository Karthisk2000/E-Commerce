from django.shortcuts import render, HttpResponse, redirect
import json
from .forms import *
from .models import *
from .constants import INCORRECT_USERNAME_PASSWORD_MESSAGE
from .constants import INVALID_REQUEST_MESSAGE
from .constants import USER_ALREADY_EXISTS
from .constants import PLEASE_TRY_AGAIN_MESSAGE


def login(request):
    """
    Function to show the login web page.
    @param request: The login request from the client.
    @return: render the login template.
    """

    # Render the login template and return it to the client
    return render(request, 'login.html')


def login_success(request):
    """
    Function to authenticate user login credentials.
    @param request: The username and password request from the client.
    @return: Return the Ajax success and error response.
    """

    if request.GET:
        username = request.GET['user_name']
        password = request.GET['password']
        # Query the UserDetails model to find a user with the given username and password
        new_user = UserDetails.objects.filter(username=username, password=password).first()
        if new_user:
            # Return JSON response indicating success
            return HttpResponse(json.dumps({
                'status_code': 200,
                'message': 'Success'
            }),content_type='application/json')

        # Return JSON response indicating error
        return HttpResponse(json.dumps({
            'status_code': 400,
            'message': INCORRECT_USERNAME_PASSWORD_MESSAGE
        }), content_type='application/json')

    # Return JSON response indicating error
    return HttpResponse(json.dumps({
        'status_code': 400,
        'message': INVALID_REQUEST_MESSAGE
    }), content_type='application/json')


def register(request):
    """
    Function to show the user registration web page.
    @param request: The register request from the client.
    @return: Render the registration template.
    """

    # Render the registration template and return it to the client
    return render(request, 'register.html')


def user_register(request):
    """
    Function to register a new user.
    @param request: The register request from the client.
    @return: Render the login template.
    """

    username = request.GET['user_name']
    password = request.GET['password']

    # Check if user with given username exists
    existing_user = UserDetails.objects.filter(username=username).first()
    if existing_user is None:
        new_user = UserDetails(username=username, password=password)
        new_user.save()

        # Return JSON response indicating success
        return HttpResponse(json.dumps({
            'status_code': 200,
            'message': 'Success'
        }), content_type='application/json')

    # Return JSON response indicating error
    return HttpResponse(json.dumps({
        'status_code': 400,
        'message': USER_ALREADY_EXISTS
    }), content_type='application/json')


def dashboard(request):
    """
    Function to get the all shoping product details from the product table.
    @param request: The dashboard render request from the client.
    @return: Render the dashboard template.
    """

    # Retrieve all products from the Product table
    products = Product.objects.all()
    context = {
        'products':products
    }

    # Render the dashboard template with context data
    return render(request, 'dashboard.html', context)


def add_product(request):
    """
    Function to get the new product details from the client and stored to the database
    @param request: The product details add request from the client.
    @return: Redirect the dashboard URL.
    """

    form=createproductform()
    if request.method== 'POST':
        # Bind form data to POST data including files
        form=createproductform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    # Prepare the context with the form
    context={'form':form}

    # Render the add product template with context data
    return render(request,'add_product.html',context)


def product_delete(request):
    """
    Function to get the product id from the client and remove the product in database table.
    @param request: The product delete request from the client.
    @return: Return the AJAX success response.
    """

    product_id = request.GET['product_id']
    # Delete the product
    Product.objects.filter(id=product_id).delete()

    # Return JSON response indicating success
    return HttpResponse(json.dumps({
        'status_code': 200,
        'message': 'Success'
    }), content_type='application/json')


def product_update(request):
    """
    Function to get the update product details from the client and update the product details in product table based \
    on the product id.
    @param request: The product details update request from the client.
    @return: Return the AJAX success and error response.
    """

    edit_product_id = request.GET['edit_product_id']
    edit_product_image = request.GET['edit_product_image']
    edit_product_description = request.GET['edit_product_description']
    edit_product_name = request.GET['edit_product_name']
    # Retrieve the product to be updated from the database
    update_product = Product.objects.filter(id=edit_product_id).first()
    if update_product:
        update_product.name = edit_product_name
        update_product.image = edit_product_image
        update_product.description = edit_product_description
        update_product.save()
        # Return JSON response indicating success
        return HttpResponse(json.dumps({
            'status_code': 200,
            'message': 'Success'
        }), content_type='application/json')

    # Return JSON response indicating error
    return HttpResponse(json.dumps({
        'status_code': 400,
        'message': PLEASE_TRY_AGAIN_MESSAGE
    }), content_type='application/json')
