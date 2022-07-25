from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
# def about(request):
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    print("Logging out `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}    
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff=True
            user.save() 
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://32f7628c-41d3-4ae1-9aec-9f0f3cf32569-bluemix.cloudantnosqldb.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealer_names'] = dealer_names
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://32f7628c-41d3-4ae1-9aec-9f0f3cf32569-bluemix.cloudantnosqldb.appdomain.cloud/api/review'
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context = {
            "reviews":  reviews,
            "dealer_id": dealer_id
        }
        for review in reviews:
            review.purchase = review.purchase == "True"
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    context = {}
    review = dict()
    if request.method == "GET":
        # Get dealer details from the API
        context = {
            "cars": CarModel.objects.all(),
            "dealer_id": dealer_id
        }
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        if request.user.is_authenticated:
            review['review'] = {}
            review['review']["time"] = datetime.utcnow().isoformat()
            review['review']["dealership"] = dealer_id
            review['review']["review"] = request.POST["review"]
            review['review']["purchase"] = request.POST["purchase"]
            review['review']['purchase_date'] = request.POST['purchase_date'] or "N/A"
            review['review']["car_model"] = request.POST["car_model"] or "N/A"
            review['review']["car_make"] = request.POST["car_make"] or "N/A"
            review['review']["car_year"] = request.POST["car_year"] or "N/A"
            userr = User.objects.get(username=request.user)
            review['review']['id'] = userr.id
            review['review']["name"] = userr.first_name + " " + userr.last_name

            url = 'https://32f7628c-41d3-4ae1-9aec-9f0f3cf32569-bluemix.cloudantnosqldb.appdomain.cloud/api/review'
            post_request(url, review, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
