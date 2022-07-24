from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50, default='undefined')
    # - Name
    description = models.TextField(null=True)
    # - Description
    def __str__(self):
    # - __str__ method to print a car make object
        return self.name + ": " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)  
    name = models.CharField(null=False, max_length=40)
    dealer_id = models.IntegerField(null=True)
    
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    SPORTS = 'Sports'
    HATCHBACK = 'Hatchback'
    CONVERTIBLE = 'Convertible'
    MINIVAN = 'Minivan'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (SPORTS, 'Sports'),
        (HATCHBACK, 'Hatchback'),
        (CONVERTIBLE, 'Convertible'),
        (MINIVAN, 'Minivan'),   
    ]
    
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=WAGON
    )
    
    year = models.DateTimeField('date designed')
    def __str__(self):
        return self.name + ", " + str(self.year) + ", " + self.type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name  
        self.id = id  
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st  
        self.state = state  
        self.zip = zip
        self.idx = 0

    def __str__(self):
        return "Dealer name: " + self.full_name + " located at " + self.address

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, id, name, purchase, review, car_make=None, car_model=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id 
        self.name = name  
        self.purchase = purchase 
        self.purchase_date = purchase_date
        self.review = review  
        self.sentiment = sentiment  

    def __str__(self):
        return "Reviewer: " + self.name + " Review: " + self.review
