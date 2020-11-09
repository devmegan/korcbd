# Testing


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
- [User Goals Testing](#user-goals-testing)
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

## Testing

### Navbar/Footer
- The nav bar and footer are visible on all pages and occupy the full width of the viewport. 
- The nav bar sticks to the top of the page as the user scrolls. The footer is always at the end of each page.
- Links in the nav bar and footer all link to correct destinations.
- The company logo in the nav bar always links back to the home page.
- The icon and links turn to a pink colour on hover.
- The cart icon displays the total price of items in the cart and updates whenever the cart contents are updated.
- The contact icon in the footer opens up a modal with the contact form in it on top of a blue full-page overlay.
- If a user is not logged in, login/signup links are displayed in the nav bar.
- If a user is logged in, profile/logout links are displayed in place of the login/signup links. 
- If a user is logged in as a superuser, a dropdown admin menu is displayed in the nav bar, with links to perform tasks such as adding products/posts.
- After testing, I added a link to dropdown admin menu for the the django site administration index page by templating in the admin index URL resolver: ```{% url 'admin:index' %}```.
- Users are redirected away from pages they are not authorised to access, either because they are not logged in or are not logged in as a superuser.
- On xs to md screens the nav bar collapses into a drop down menu that can be toggled using the burger icon that is displayed on the right-hand side of the nav bar.

### Contact Form Modal
- The contact form opens as a modal in the centre of the screen on top of a blue full-page overlay.
- If a user is logged in, the email field is pre-populated with the users email address.
- The contact form requires name/email/message fields to be filled out before it will submit.
- While the form submits and an email is generated, the submit button turns into a spinner icon so that the user cannot resubmit the form.
- If the contact form successfully generates an email using emailJS, this is fed back to the user with a success message. The spinner icon turns into a green button with a checkmark inside it. Clicking this closes the contact modal.
- If the contact form does not send successfully, an error message is displayed to the user and they are given the company email address to contact directly. The spinner icon turns into a red button with a cross inside it. Clicking this closes the contact modal.

### Home Page
- The carousel always occupies the full width of the viewport. It slides between images automatically.
- All the buttons on the home page lead to the correct destinations.
- The fading text in teh banner below the main company logo fades in and out automatically.
- The order tracking form works. If the order is found in the database, then the tracking status is displayed to the user when the page reloads.
If the user inputs an incorrect order number, an error message toast is displayed to the user.
- The product category cards link to the correct categories. 
- The blog cards display the three most recent blog posts and the "read full post" buttons take the user directly to the full blog post for the card they have clicked on.

### About Page
- For users who are not logged in as superusers, the about page is a static page with subheadings and paragraphs.
- For superusers, below the subheading of each paragraph on the about page is an edit button and a delete button.
    - The edit button takes the superuser to a new page with the edit section form on it. On succesfully updating the section, the superuser
    is redirected to the about page and a success toast is displayed feeding back to the superuser which section has been updated.
    - The delete button deletes that section immediately and a message is displayed to the superuser that the section has been deleted. 

### Products
- Below the nav bar on the products page is a secondary bar which displays to the user the amount of products they are currently viewing.
- Users can filter products by category or search query. The current filter and number of products in the query set is displayed to the user as breadcrumbs.
- Users can also order products by price (high to low or low to high) by clicking the button which toggles them. The current ordering is displayed in the button.
The default ordering is low to high. 
- If the user tries to filter the products but the resulting queryset is empty, a card is displayed to the user where the products would usually be, feeding back that there were no products
which matched their query. The button below this takes the user back to view all of the products in the store. 
- Products are displayed in their own cards on the page. The product name and price are correctly displayed in the card underneath the product image. A button below links to the detailed page for that product.
- For superusers, below the button linking to the product detail page, are buttons to edit and delete the product.
    - The edit button takes the superuser to a new page with the edit product form on it. On succesfully updating the product, the superuser
    is redirected to the product detail page of the product they have just updated and a success toast is displayed to the superuser.
    - The delete button deletes the product immediately and a toast is displayed to the superuser that the product has been deleted. 

### Product Detail 
- All the product detail fields are rendered out correctly on the page - product name, category, price, quantity in stock, quantity in the users cart, description and ingredients.
- The adder and subtractor buttons update the quantity to add to the cart.
    - If the currenty quantity is 1, the subtractor button is disabled so this cannot be lowered to 0 using the button.
    - If the quantity is equal to the quantity of the product in stock, the adder button is disabled. 
    - If a user manually types in a number outside of the accepted range, a validation error is shown and the item is not added to the cart.
    - If a user already has some quantity of the product in their cart, they cannot an additional quantity of the product to their cart that would exceed the quantity in stock.
- As long as the user is adding a valid quantity of the product to the cart, clicking the "add to cart" button adds the specified quantity to the cart and a success toast is displayed to the user with a cart preview and
link to checkout in it. The cart total is automatically updated.
- The "keep shopping" button correctly directs the user back to viewing all the products.
- For superusers, the edit and delete buttons are displayed at the bottom of the product detail page. 
    - The edit button takes the superuser to a new page with the edit product form on it. On succesfully updating the product, the superuser
    is redirected back to the product detail page of the product they have just updated and a success toast is displayed to the superuser.
    - The delete button deletes that section immediately and a toast is displayed to the superuser that the product has been deleted.

### Cart
- Accessing the cart page when nothing has been added to the cart displays a message to the user that their card is empty. The "Shop Now" button takes the user to view all the products in the store.
- When a product is added to the cart, it is displayed on the cart page with the specified quantity.
- Increasing or decreasing the quantity of the product and then clicking the update button updates the quantity of that item. 
    - If the quantity value is less than 1, a validation error is shown and the update form does not submit.
    - If the quantity value is greater than the quantity of the product in stock, an alert is displayed to the user that they cannot increase the quantity of the product beyond the amount that is in stock. 
- Clicking the delete icon deletes the corresponding product from the cart entirely.
- Deleting all items in the cart returns the cart page to displaying the empty cart message.
- The correct item total is displayed at the bottom of the cart page when there are products in the cart. 
- The "keep shopping" button takes the user back to viewing all products in the store.
- The "checkout" button takes the user through to the checkout page. 

### Checkout 
- If there are no items in the cart and the user tries to access the checkout page by URL, they are redirected to their cart. 
- When there are items in the cart, the checkout form is set out as expected when. If a user is logged in, they can choose to save this
information to their profile. If a user is not
logged in, they are links to log in or sign up if they want to save the information to their profile. 
- If a user is logged in and has existing information in their user profile, the checkout form is populated with these details. 
- The Stripe payment element works correctly, and recognises card types and valid/invalid inputs.
- Any Stripe error messages are displayed to the user below the payment element.
- Testing with the [Stripe test card numbers](#https://stripe.com/docs/testing) triggers the correct payment flows - i.e. triggering a Stripe pop-up requiring
extra payment details authentication. 
- Orders are only created in webhook where there has been an error creating it directly with django. No duplicate orders are created.
- Successful/Failed payments are recoreded as Events in Stripe Developers section of the Stripe Account.
- Once the order has been created, the user is redirected to their order confirmation page. 

### Checkout Success 
- The order confiramtion number is displayed in full below the successful order message.
- The order dispatch status is correctly displayed as "preparing for dispatch". 
- The order shipping address and contact details are displayed correctly above the cart items. 
- The correct cart items and item details are displayed.
- The button at the bottom of the page links the user through to the blog page. 
- If a user tries to re-view the checkout success page by URL and they are not logged in, they are asked to confirm the email address
that the order was placed with. On successfully confirming the email address, they are given access to the page.

### Profile 
- Users must be logged in to access the profile page. Users who are not logged in are redirected to the log in page.
- Information in the users profile is correctly updated when the details are updated from profile page and checkout page. 
- User information form is laid out as expected and prepopulated with existing information. Required fields are marked with an asterisk. 
- Invalid inputs updating the user profile form produce a validation error and prevent the form submitting.
- Historical orders are displayed in the orders section in reverse chronological order.
- Order dispatch symbol changes to a check mark when the order is marked as dispatched in the django admin panel.
- Clicking on the order reference number goes to the order confirmation for that order. A toast message confirms this a historical order.
- All details are displayed correctly on the order confiramtion page and the button at the bottom of the page links back to the users profile page.

### Blog 
- Blog posts displayed in cards ordered in reverse chronological order. 
- Most recent post is in the largest card at the top of the page. 
- "Continue reading" buttons in blog post cards link to the correct blog post. 
- Clicking tags on each post filters blog posts into a queryset of posts which have the same tag. 
- Searching blog posts by query term filters blog posts into a queryset of posts which contain the search term.
- If no blog posts are returned from the view, the user sees a notice that no posts matching their search were found.
- The edit/delete buttons are displayed in each card to superusers. 
    - The edit post button takes the superuser to the edit post page, where the edit post form is rendered out pre-populated with the correct blog post.
    After editing hte post the superuser is redirected to the blog page.
    - Deleting a blog post requires the superuser to confirm that they want to delete the post. When the post is deleted, the superuser is
    redirected back to the blog page.

### Blog Post 
- The blog post is displayed below the post title, author and date the post was made. 
- Clicking on the tags below the post takes the user back to the blog page with the posts filtered into a queryset of posts which have the same tag.
- Clicking the "back to blog" button takes the user back to viewing all blog posts. 
- Logged in users can "heart" the post by clicking it, and then the heart turns red. The number of hearts is incremented by 1. 
Clicking the heart when it has already been clicked "unhearts" the post and the heart turns dark again. The number of hearts is decremented by 1. 
- Logged in users can add a comment to the post. Once a comment is added, it is displayed with the autor, date and comment body. The number of comments is incremented by 1.


## Bugs fixed during Testing
- The main bug found during testing is that while the page layout flowed well when testing on small-screen devices using goodge developer tools,
this didn't always render the same on an actual mobile device, with elements becoming squashed and/or overflowing. This has been fixed by going
through every page on the site on a mobile device to make sure that it's rendering well.
- The edit product form was not submitting successfully. This was because the product model was updated to have a field for the quantity of the product sold, but the edit
product form hadn't been updated to include this change to the model. By adding the sold_qty field into the form as a hidden field, the form is valid when submitted and
products can now be updated from the edit product page.

## Unsolved Bugs
- On the profile form, there is a checkbox that allows users that are signed in to update their profile with the order details. 
The checkbox does visually check and uncheck when the user clicks it, but when the form is submitted, it submits the checkbox as checked
regardless of its actual state. This is true regardless of whether the box is checked by default or not. I tried to write a fix for this using
jQuery's ```.attr("checked", "checked")``` and ```.prop("checked", true)/.prop("checked", false)``` methods on click but this did not solve
the problem. For now, I have built a jQuery workaround to this which toggles the value of a hidden input when the user clicks the checkbox.