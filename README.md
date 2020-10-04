# KOR CBD e-Commerce Store
<img src="README/assets/img/mockup-home.jpg" style="margin: 0; width: 75%">

The KOR CBD e-Commerce store is for a company which sells CBD products to athletes, and is particularly targeted towards martial artists. It is designed to 
allow users to shop and checkout either anonymously or as a logged in user using Stripe's Payment appearing. Extra features are available to logged in users, such as persiting their user
profile information, a saved order history, and the ability to interact with blog posts. The whole app is written in Python using the Django framework. 

The django app is deployed using Amazon Web Services and Heroku and is availabe here: <deployed_link>

## Contents
1. [Client](#client)
    - [Client Information](#client-information)
2. [UX](#ux)
    - [Users](#users)
    - [User Goals](#user-goals)
    - [Wireframes](#wireframes)
    - [Colour Palette](#colour-palette)
 2. [Information Architecture](#information-architecture)
    - [Database](#database)
    - [Data Models](#data-models)
 3. [Design Choices](#design-choices)
     - [Colours](#colours)
 4. [Features](#features)
     - [Navigation](#navigation)
     - [Home](#home)
     - [Allauth](#allauth)
     - [About](#about)
     - [Products](#products)
     - [Cart & Checkout](#cart-and-checkout)
     - [Profiles](#profiles)
     - [Blog](#blog)
     - [404](#404)
     - [Toasts](#toasts)
     - [Future Features](#future-features)
5. [Technologies Used](#technologies-used)
    - [Frameworks](#frameworks)
    - [Template Engines](#template-engines)
    - [Databases](#databases)
    - [Backend Libraries](#backend-libraries)
    - [Frontend Libraries](#frontend-libraries)
    - [Languages](#languages)
    - [Development Tools](#development-tools)
6. [Testing](#testing)
7. [Deployment](#deployment)
    - [Requirements](#requirements)
    - [Git Instructions](#git-instructions)
    - [Heroku Instructions](#heroku-instructions)
8. [Credits](#credits)
    - [Content and Code](#content-and-code)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)


## Client Information

The goals that KOR CBD have given for this e-Commerce store are: 

- Present a clinical and reputable brand aesthetic without appearing bland. 
- Target the website to martial artists, without using jargon that excludes athletes from other sports. 
- Have a smooth payment flow for customers from the moment a project is added to the cart.
- Provide a record of all orders placed so that they can be fulfilled. 
- Provide customers with extra information about the company through an about page and a blog. 
- Restrict certain activities to KORCBD staff such as CRUD functionality for products and blog posts.
- Link the store to the companies social media accounts to bootst customer interaction. 

## UX

### Users

Users of the KOR CBD website are most likely looking to buy CBD products. While the company targets itself at martial artists, many of their customers are athletes in other sports. The website needs to still be accessible to them. 

## User Goals 

- As a customers I want to be able to:
    - Easily navigate the store using a layout that is consitent across all pages. 
    - Find out a bit about the business and its products before I commit to buying them. 
    - Search for specific products and content that I am interested in.
    - Filter products by categories so I don't waste time looking at products I'm not interested in.  
    - Check that the products don't contain any ingredients that I am allergic to. 
    - Add items to my cart and checkout anonymously if I decide not to sign up to the site. 
    - Recieve a confirmation of my order so that I know it has been placed. 
    - Have a unique order number for my order so that it can be easily located by the company. 
    - Sign up to the site if I decide I would like to order more often. 
    - Save my billing and shipping details so I don't have to fill them out every time I make an order. 
    - Update my profile details as and when they change. 
    - View my order history and the details of each order. 
    - Read blog posts about the company and interact with them. 
    - Be able to contact the company if I have any questions or complaints. 
    - Be able to connect with the business on social media. 

## Wireframes 

## Colour Palette

# Information Architecture

## Database

The app was developed using the local [sqlite]() database that is installed with django. For the deployed version of the app, a [PostgreSQL]() database is used that is provided by [Heroku](). 

## Database Models 

### User

The User model is provided by the ```django.contrib.auth.models``` import.

### Products

The ```Product``` model in the ```Products``` app contains data on each product in the store.

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Name | name | max_length=100 | CharField
Sku | sku | max_length=254 | CharField
Category | category | | ForeignKey
Image_URL | image_url |  | URLField
Description | description |  | TextField
Ingredients | ingredients |  | TextField
Price | price | max_digits=6, decimal_places=2 | DecimalField

### Orders 

The ```Order``` model ```OrderLineItem``` model  in the ```Cart``` app contains data on each order that is made.

#### Order Model

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Order Reference | order_reference | max_length=32 | CharField
User Profile | user_profile | | ForeignKey
Full Name | full_name | max_length=100 | CharField
Email | email | max_length=254 | EmailField
Phone Number | phone_number |  max_length=20 | TextField
Country | country |  | CountryField
Post Code | postcode | max_length=20 | CharField
Town or City | town_or_city | max_length=40| CharField
County| County | max_length=40| CharField
Street Address 1 | street_address1 | max_length=80 | CharField
Street Address 2 | street_address2 | max_length=80 | CharField
Date | date | auto_now_add=True | DateTimeField
Order Total | order_total | max_digits=10, decimal_places=2 | DecimalField
Paid | paid | | BooleanField
Dispatched | dispatched | | BooleanField
Original Cart | original_cart | | TextField
Stripe PID | stripe_pid | max_length=254 |TextField

#### Order Line Item Model 

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Order | order | | ForeignKey
Product | product | | ForeignKey
Quantity | quantity | | IntgerField
Line Item Price Per Unit | lineitem_price_per_unit | max_digits=6 | DecimalField
Line Item Total | lineitem_total |  max_length=20 | DecimalField

### Profiles 

The ```Profile``` in the ```Profiles``` app contains data on user profiles.

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
User | user | | OneToOneField
Profile Phone Number | profile_phone_number |  max_length=20 | TextField
Profile Country | profile_country |  | CountryField
Post Code | profile_postcode | max_length=20 | CharField
Town or City | profile_town_or_city | max_length=40| CharField
County| County | max_length=40| CharField
Street Address 1 | profile_street_address1 | max_length=80 | CharField
Street Address 2 | profile_street_address2 | max_length=80 | CharField

### Blog

The ```Post``` model and ```Comment``` in the ```Blog``` app contains data on blog posts and user comments on them.

#### Post 

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Title | user | max_length=255 | CharField
Author | author |  | ForeignKey
Body | body |  | TextField
Date | date | auto_now_add=True | DateField
Image Url | image_url | max_length=40 | CharField
Tag 1 | tag_1 | max_length=20| CharField
Tag 2 | tag_2 | max_length=20 | CharField
Tag 3 | tag_3 | max_length=20 | CharField
Hearts | hearts | | ManyToManyField

#### Comment

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Post To Comment | post_to_comment | | ForeignKey
Author | author |  | ForeignKey
Comment Body | body |  | TextField
Date | date | auto_now_add=True | DateField


