## Coverage Testing

## Contents
1. [Automated Testing](#automated-testing)
    - [Coverage](#coverage)
        - [Python Testing](#python-testing)
        - [Django Coverage](#django-coverage)
    - [Jasmine](#jasmine)
    - [Validation](#validation)
    - [Flake8](#flake-8)


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

#### W3C CSS Validation
<a href="http://jigsaw.w3.org/css-validator/check/referer">
    <img style="border:0;width:88px;height:31px" src="http://jigsaw.w3.org/css-validator/images/vcss-blue" alt="Valid CSS!" />
</a>

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

