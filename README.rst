
=============
ckanext-api_basic_functions
=============

..
This CKAN extension enable an API with functions to execute SQL queries or re index solr.

------------
Requirements
------------

Tested in CKAN 2.3.3 and 2.4.3 version.


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-api_basic_functions:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-api_basic_functions Python package into your virtual environment::

     pip install ckanext-api_basic_functions

3. Add ``api_basic_functions`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Specify the needed config settings, for example:
    ckan.api_harvest.config_file = /etc/ckan/default/production.ini

    ckan.api_harvest.virtual_evnvironment_route = /etc/ckan/default


------------------------
Development Installation
------------------------

To install ckanext-api_basic_functions for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/odevsp/ckanext-api_basic_functions.git
    cd ckanext-api_basic_functions
    python setup.py develop


------------------------
Available methods
------------------------

The methods defined are available using GET and POST calls, and required request parameter or body, examples:

-Reindex solr
http://ckan_url/api_basic/reindex_solr
Method GET

-Execute query in CKAN database
http://ckan_url/api_basic/execute_query
Method POST
Body must be content the query

-Execute script SQL in CKAN database:
http://ckan_url/api_basic/execute_script_sql
Method POST
Param path must be content the absolute path to script

Only admin user using API key can call this methods.
