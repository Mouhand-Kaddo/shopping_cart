# shopping_cart
python 3.10.7 and django 4.0.8 was used to make this project 

## About The Project

In this project, a shopping cart was made. In this shopping cart, you're able to add products from the inventory, remove products from the cart, or buy what is currently in the cart.

## preview

![image](https://user-images.githubusercontent.com/73709175/194751976-fec7d60d-f26a-4a35-a541-5f2a7229d0cb.png)


## instructions on how to install

the needed libraries are in the requirements.txt to install and run this project follow these steps:
- clone the git repo
```
git clone https://github.com/Mouhand-Kaddo/shopping_cart.git
```
- then make and enter a virtual environment to run the project from
```
python -m venv .venv
.venv\Scripts\activate
```
- then install the needed libraries
```
pip install -r requirements.txt
```
- now run the webapp using the following command
```
python manage.py runserver
```
## admin user
to enter the admin user either enter the premade user which has the following username:

> mouhand

and password:

> testpass

or create a new admin with the following command:
```
python manage.py createsuperuser
```
