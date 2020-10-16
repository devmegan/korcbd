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

### Django Coverage

First make sure ```coverage``` is installed using:

```pip3 install coverage```

To find the coverage of the tests, use the command:

```coverage run manage.py test```

Coverage will check all .py files in the repo. I have not tested any automatically
generated files, and have ommited migration files and pip3 files from the coverage test,
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

At deployment, there is 86% coverage across all apps.

A copy of the final coverage report has been written to the
[coverage_report.txt](coverage_report.txt) file. 
