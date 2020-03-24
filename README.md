FakeXchange
===========

This is a simple 'fake' crypto exchange built for the purpose of demonstrating
integration of cryptocurrency into an existing platform.


Installation instructions
-------------------------

It is highly recommended to run this application in it's own virtualenv.
After setting one up install the dependancies with

`pip install -r requirements.txt`

To load the initial database for the first time execute:

```python manage.py migrate
python manage.py loaddata coins```

It's a Python/Django based application, you can run it with

`python manage.py runserver`

To generate a first admin user you can use

`python manage.py createsuperuser`

You can now visit the exchange in your browser or go to /admin to enter the admin panel
