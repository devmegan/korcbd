## Coverage Testing

## Contents
- [Automated Testing](#automated-testing)
    - [Coverage](#coverage)
        - [Python Testing](#python-testing)
        - [Django Coverage](#django-coverage)
    - [Validation](#validation)
        - [HTML](#w3c-markup-validation)
        - [CSS](#w3c-css-validation)
        - [JavaScript](#jshint)
    - [Flake8](#flake-8)
- [User Stories Testing](#user-goals-testing)
- [Manual Testing](#manual-testing)
- [Unsolved Bugs](#bugs-remaining)

## Automated Testing

### Coverage
#### Python Testing

Python testing used to test the functionality of the backend code, using Django's inbuilt
test module. [Coverage.py](https://coverage.readthedocs.io/en/v4.5.x/) was then used to ensure that these python unit tests are coverering
a significant portion of this code.

To run the Python tests: 

```python3 manage.py test```

To run tests on a specific app: 

```python3 manage.py test <app_name>```

At deployment, 100% of the tests pass without error. 

#### Django Coverage

First make sure ```coverage``` is installed using:

```pip3 install coverage```

To find the coverage of the tests, use the command:

```coverage run manage.py test```

Coverage will check all .py files in the repo. I have not tested any automatically
generated files, and have ommited migration files and .pip files from the coverage test,
using the --omit flag:

```coverage run --omit=*migrations*,*.pip* manage.py test```

The coverage tests can be localised to a specific app using the source flag:

```coverage run --source=<app_name> manage.py test <app_name>```

A report on the results of the coverage test can then be generated using:

```coverage report```

For an interactive version of the coverage report, create a directory for the html test files 
using:

```coverage html``` 

To access the report, run the project locally using:

```python3 -m http.server 4000``` 

and open it up the browser. 

Go to the ```htmlcov`` directory to view and interact with the report.  

At deployment, ommiting migrations and .pip files, there is 86% coverage across all apps.

A breakdown of this coverage by app can be seen below:

| App | Coverage |
|-|-|
| Home | 97% |
| About | 99% |
| Blog | 97% |
| Products | 99% |
| Cart | 66% |
| Total | 86% |


A copy of the final coverage report has been written to the
[coverage_report.txt](coverage_report.txt) file. 

The cart app has significantly less coverage than the other apps.
This app and the checkout flow has undergone significant manual
testing to assure its functionality.

### Validation

#### W3C Markup Validation 

[W3C Markup Validation](https://validator.w3.org/) has been used on all HTML files in the project. The Django templating used in the raw HTML
files throws a lot of errors on the validator, so I have run it using the HTML copied from the source code of the website when it is up and running.

#### W3C CSS Validation

[W3C CSS Validation](https://jigsaw.w3.org/css-validator/) has been used on the main [style.css](static/css/style.css) file and the [stripe.css] file which 
provides the styles for the stripe and stripe-style form elements. 

Both these files pass the W3C CSS validation with no errors. 

#### JSHint

[JSHint](https://jshint.com/) has been used to validate the two main Javascript files 
used in this project. [email.js](static/js/email.js) which provides the JavaScript for 
the emailJS email form, and [striple.js](cart/static/js/stripe.js) which provides the 
JavaScript for the stripe payment API. 

JSHint didn't flag up any major errors, and the three missing semi-colons it flagged up
have been added to the JavaScript files.

### Flake8 

I have used the [Flake8](https://pypi.org/project/flake8/) python linting tool to ensure the python code 
in this project conforms to PEP8 style standards. 

To install flake8 ues:

```python3 -m pip install flake8```

To run flake8, use: 

```python3 -m flake8```

This will cover all .py files in the repo. As with the coverage testing, I have ommitted
the migration files, which are automatically generated, using: 

```python3 -m flake8 --exclude=*/migrations/*```

At deployment, I have written the output of this flake8 command to the 
[flake8_errors.txt](flake8_errors.txt) file. The only unsolved error is that
the cart.signals file is imported into the cart apps file but is unused:

```./cart/apps.py:9:9: F401 'cart.signals' imported but unused```

This import is required here so that the signals.py file runs whenever order line
items are updated on an existing order, to ensure the order is updated accordingly.

## User Goals Testing

At the begging on this project, a list of user goals were set out. These
have been tested against the project at the end of development, to ensure
that they have all been met. 

**As a user I want to be able to easily navigate the store using a layout that is consitent across all pages**
- The site uses a base template that is identical across every single page on the site. This means 
that all the nav/footer elements are exactly the same, meaning users quickly become familiar with the navigation links nav/footer elements. 
- The navbar and footer follow a conventional layout, so that users can find all elements in the 
places that they would expect them to be in. 
- On pages where there are sub-sections, such as the blog or products page, an extra div is added below the nav bar which gives breadcrumbs, 
search, sort and category options. These are positioned and styled the same in all apps that they feature in. 

**As a user I want to be able to find out a bit about the business and its products before I commit to buying them**
- There is an about page which gives an overview of the company and their products. It is easy for admin staff to 
update this about page and add new sections to it, so that if they are getting common questions or things change
with the company, they can update it to keep their customers informed. 
- All products also have a sepcific product detail page to give more information about them to the user.

**As a user I want to be able to search for specific products and content that I am interested in**
- A search bar on the product shop page allows users to filter products according to their specific search query.
- The product search queries product names, descriptions, ingredients and sku's to compile a corresponding queryset. 
- If their search returns no results, or the search query is an empty string, this is fed back to the user. 

**As a user I want to be able to filter products by categories so I don't waste time looking at products I'm not interested in**
-  Products can be filtered according to the category assigned to them using a dropdown categories list just under the nav bar
in the products page.
- If the user is viewing a product detail page, this page displays which category that product is in, and provides a link for
users to view mode products that are in the same category.

**As a user I want to be able to check that the products don't contain any ingredients that I am allergic to**
- On the product detail pages, the ingredients for each product are listed just below the product discription, so that users can check it
does not contain any products that they are allergic to. 

**As a user I want to be able to add items to my cart and checkout anonymously if I decide not to sign up to the site**
- Users can shop and add items to their cart and checkout without having to sign up for an account. Their cart items will still
persist until their browser session is cleared.
- The checkout flow is virtually identical for guest users. The only difference they will find is that the checkout personal details
form will not be pre-populated with their profile details. 

**As a user I want to be able to recieve a confirmation of my order so that I know it has been placed** 
- All users will be redirected to an order confirmation after their order is placed. They will also recieve an email copy of this order
to confirm it has been placed. 
- Signed up users with an account can view all historical order confirmations from their profile page. 
- Registed users will also be automaitcally redirected their order confirmation page. However, to keep their details secure, 
if they wish to view this order confirmation again, either accessing it by URL or by tracking, they will have to confirm their 
email address to confirm that it is the correct user accessing the confirmation. 

**As a user I want to be able to have a unique order number for my order so that it can be easily located by the company** 
- All orders have a unique order number generated using python's uuid module. This is pre-fixed with "KOR-" so that it is 
always easy to identify which company the order was for. 
- Order numbers are displayed to the user on their order confirmation page after checkout. 
- The same order number is also included in the confirmation email sent to customers after checkout. 
- For users with an account, the order number also appears in the "order history" section on their profile.

**As a user I want to be able to sign up to the site if I decide I would like to order more often**
- Users can sign up to the site using the signup link that is included in the nav bar. 
- If users try to log in without having an account, they will be redirected to the sign up page. 
- At checkout, users who are not signed up are presented with a link which prompts them to sign up to the site to save their order details.

**As a user I want to be able to save and update my shipping details so I don't have to fill them out every time I make an order** 
- Users who are signed up can save their shipping details to their profile. This prepopulates the order form with these details when
going through the checkout process.
- Users can update these details either from their profile page or by changing them at checkout and choosing to save the new details to
their profile.

**As a user I want to be able to read blog posts about the company and interact with them**
- There is a blog section to the site, where only admin staff can create blog posts.
- Users who are registered with the the site can create comments on blog posts. These comments can be viewed by all users. 
- Comments on blog posts can be deleted by admin staff, or by the user who created the comment.
- Users can "heart" posts that they like by clicking on a heart icon at the bottom. The heart will turn red when clicked.

**As a user I want to be able to be able to contact the company if I have any questions or complaints** 
- A contact form for the company, which uses emailJS, allows users to directly contact the company by email. 
- Users are asked to leave a name, phone number and email address. The name and email address are required, so that the company
can get in touch with them about their message.
- It is immediately fed back to the user whether the email has sent succesffuly. If it has not, they are alerted to this and given
the email address of the company to email them directly from their personal email account.