===================
To-Do List REST API
===================

It provides a REST API for a simple To-Do List APP on Django

Some considerations
===================

* The default auth.User model has been used to create users.
* The Session Authentication method has been used in this project. ( http://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication )
* The project will only work with Python 3.5+.
* The project is configured to use SQLite as the default database.
* A default user with username **novastone** and password **test** is created automatically when the migrations are loaded.
* A user can't retrieve, modify or delete other users' tasks.


Usage
===========

1. Install the required packages with (``pip install -r requirements.txt``).
2. Create the tables an a default user with (``cd src/todolist && python manage.py migrate``)
3. Run the application with (``python manage.py runserver``)
4. The API will be available at http://127.0.0.1:8000/api/

Task Model
----------

The task model has six attributes: created, modified, title, description, completed and user.

End Points
===========

* /api/login/ - Log in a user. The username and password must be sent by a POST request.
* /api/logout/ - Log out the current user.
* /api/tasks/ - Create a new task or return the tasks for the logged in user.
* /api/tasks/<int:pk>/ - Retrieve, update or delete the task with the ID specified.


Examples
========

It is a good idea to install **httpie** to test the API from the command line (``pip install httpie``)

* Logging in to the API

    http POST http://127.0.0.1:8000/api/login/ username=novastone password=test --session=/tmp/session1.json -h
    
* Logging out from the API
    
    http GET http://127.0.0.1:8000/api/logout/ --session=/tmp/session1.json

We will store the sessionid and csrf token for future requests.
    
Creating a task
---------------

    http POST http://127.0.0.1:8000/api/login/ title="Gym" description="I will try to do 20 push-ups" X-CSRFToken:xAbNhjBFulObPanKbtwkAyoxS7rxvgJe23ojC1mEenS9jANseaEb1JiL0oR61VDd --session=/tmp/session1.json -h

Retrieving all the tasks for the logged in user
---------------

    http GET http://127.0.0.1:8000/api/tasks/ --session=/tmp/session1.json
    
Retrieving a task created for the logged in user
---------------

    http GET http://127.0.0.1:8000/api/tasks/1/ --session=/tmp/session1.json
    
Deleting a task 
---------------

    http DELETE http://127.0.0.1:8000/api/tasks/1/ --session=/tmp/session1.json
    
Partial update
---------------

For example, we will set a task as completed

    http PATCH http://127.0.0.1:8000/api/tasks/1/ completed=True X-CSRFToken:xAbNhjBFulObPanKbtwkAyoxS7rxvgJe23ojC1mEenS9jANseaEb1JiL0oR61VDd --session=/tmp/session1.json -h
