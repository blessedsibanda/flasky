# my-flask-starter
A Flask Starter Boilerplate


### Create venv
### Activate venv

### Install pip packages in requirements.txt

### Set environmental variables
export FLASK_APP=flasky.py

export FLASK_ENV=development

export MAIL_USERNAME=*your-gmail-username*

export MAIL_PASSWORD=*your-gmail-password*

export FLASKY_ADMIN=*your-admin-email*

### Create and run database migrations
flask db init 

flask db migrate -m'initial migration'

flask db upgrade
