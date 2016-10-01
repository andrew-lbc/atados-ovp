==========
atados-ovp
==========

.. image:: https://app.codeship.com/projects/4f1ceb70-12c4-0133-f72e-1e632cdd2280/status?branch=master


This is atados.com.br implementation of Open Volunteering Platform.

Getting Started
---------------
Running atados-ovp locally is very straightforward. It's built on top of Django.

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


Prerequisites
""""""""""""""
The project was developed and test on Python 3.5. Other versions weren't tested.

  ::   

   python 3.5
   virtualenv


Installing
""""""""""""""

1. Create a virtualenv. We are going to be using virtualenvwrapper for convenience::
 
    mkvirtualenv atados-ovp

2. Clone the project::

    git clone https://github.com/atados/atados-ovp.git
    cd atados-ovp

3. Install project dependencies::

    pip instal requirements.txt

4. Run migrations::

    ./manage.py migrate

4. Now you should be able to run the project::

    ./manage.py runserver

Your server should be now running on localhost:8000.

Testing
---------------
To test all modules

::

./manage.py test

Built with
---------------
- python
- Django
- django-rest-framework

Contributing
---------------
Please read `CONTRIBUTING.md <https://github.com/atados/atados-ovp/blob/master/CONTRIBUTING.md>`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
---------------
We use `SemVer <http://semver.org/>`_ for versioning. For the versions available, see the `tags on this repository <https://github.com/atados/atados-ovp/tags>`_. 

License
---------------
This project is licensed under the GNU GPLv3 License see the `LICENSE.md <https://github.com/atados/atados-ovp/blob/master/LICENSE.md>`_ file for details
