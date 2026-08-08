# Profile657 #

A simple "vibe coded" Django signup and login app.

## Requirements ##

* Django

## Tested with ##

```
django==6.0.5
```

## Installation ###

### Install with pip ###

``` bash
pip install -U git+https://github.com/oscfr657/profile657.git@main
```

### Django settings ###

In the settings file

add to the INSTALLED_APPS

``` python
INSTALLED_APPS = [
    'profile657',
]
```

and 

``` python
PROFILE657_SIGNUP_LOCKED = False
```

### Django url ###

To the django projects' url.py add

``` python
from django.urls import path, include
```

and

``` python
urlpatterns += [
    path("accounts/", include("profile657.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

### Database configuration ###

``` bash
python manage.py migrate
```

### Collectstatic ###

``` bash
python manage.py collectstatic
```

sudo systemctl daemon-reload

## For development ##

### Create a new release ###

#### Make migrations ####

``` bash
python manage.py makemigrations
python manage.py migrate
```

#### Run black ####

``` bash
python -m venv env 
source env/bin/activate
python -m pip install black
python -m black . -S -t py310 -t py311 -t py312 --extend-exclude .migrations --diff
python -m black . -S -t py310 -t py311 -t py312 --extend-exclude .migrations
```

#### Run tests ####

Copy test_settings.py to your django project dir

``` bash 
python manage.py test chat657
```

Update version in VERSION.txt

Update CHANGELOG.md

#### Build release ####

``` bash
python -m pip install build
python -m build --sdist
```

#### Publish to Git ####

``` bash
git commit -a -m 'Changelog message.'
git push
```

## TODO: ##

feat: create Django model tests
feat: Add invite only functionality
chore: Update setuptools and min python versions