from django.http import HttpRequest
from django.contrib.auth.models import User
import random


def generate_username(name: str) -> str:
    """
        Function that returns a random generated username
        :param name: Complete User name given
        :return str: User name based characters randomly joined with 
                    numbers and special characters like _ or .
    """
    special_characters: list = ['_', '.']
    numbers: list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    
    username: str = name.lower().replace(" ", random.choice(special_characters))
    username += random.choice(special_characters)
    username += random.choice(numbers)
    username += random.choice(numbers)
    username += random.choice(numbers)
    username += random.choice(numbers)
    username += random.choice(numbers)
    username += random.choice(numbers)

    return username


def generate_firstname(name: str) -> str:
    """
        Function that returns the first name from the User name given
        :param name: String containing the complete User name
        :return str: New User's based name generated first name
    """
    return name.split(" ")[0]


def generate_lastname(name: str) -> str:
    """
        Function that returns the last name from the User name given
        :param name: String containing the complete User name
        :return str: New User's based name generated last name
    """
    if len(name) > 1:
        return name.split(" ")[-1]
    
    return None


def get_registerform_data(request: HttpRequest) -> dict:
    """
        Function that receives the given request object and generates all the fields
        required to create a new user
        :param request: Request object containing the incoming form data
        :return dict: Dictionary with all the data ready for new user creation
    """
    name: str = request.POST['name']
    username: str = generate_username(name)
    email: str = request.POST['email']
    password: str = request.POST['password']
    firstname: str = generate_firstname(name)
    lastname: str = generate_lastname(name)

    return {
        'username': username,
        'email': email,
        'password': password,
        'firstname': firstname,
        'lastname': lastname
    }


def create_new_user(data: dict) -> User:
    """
        Function that creates a new User object
        :param data: Data dictionary containing all the required fields for the user creation
        :return User: New User object created and saved
    """
    new_user: User = User.objects.create_user(
        username=data['username'], 
        email=data['email'],
        password=data['password']
    )

    new_user.first_name = data['firstname']

    if data['lastname']:
        new_user.last_name = data['lastname']

    new_user.save()

    return new_user