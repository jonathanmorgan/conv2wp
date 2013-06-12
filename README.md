# conv2wordpress

Django application that helps to convert content from other blogs to Wordpress WordPress eXtended RSS (WXR) files.

## Installation

### Dependencies

The core conv2wp classes just make use of base python packages and django.  The B2Evolution import code uses a few routines from the python_utilities package ( [https://github.com/jonathanmorgan/python_utilities](https://github.com/jonathanmorgan/python_utilities) ) and use Beautiful Soup version 4.

### Install

If you are migrating from blog software and will be reading blog posts out of a database, the easiest way to use conv2wp is to install the conv2wp django app in the database that also contains the files from which you will be getting data.  To do this:

- install pip

        (sudo) easy_install pip

- install django

        (sudo) pip install django

- install South (data migration tool), if it isn't already installed.

        (sudo) pip install South

- in your work directory, create a django site ( see [https://docs.djangoproject.com/en/dev/intro/tutorial01/](https://docs.djangoproject.com/en/dev/intro/tutorial01/) for more details )

        django-admin.py startproject <site_directory>
    
- cd into the site\_directory

        cd <site_directory>
    
- pull in python\_utilities

        git clone https://github.com/jonathanmorgan/python_utilities.git

- pull in our python code

        git clone https://github.com/jonathanmorgan/conv2wp.git

### Configure

- from the site\_directory, cd into the site configuration directory, where settings.py is located (it is named the same as site\_directory, but nested inside site\_directory, alongside all the other django code you pulled in from git - <site\_directory>/<same\_name\_as\_site\_directory>).

        cd <same_name_as_site_directory>

- in settings.py, set USE_TZ to false to turn off time zone support:

        USE_TZ = False

- configure the database in settings.py

    - For mysql:

        - create mysql database.
            - at the least, make your database use character set utf8 and collation utf8_unicode_ci
            - To support emoji and crazy characters, in mysql >= 5.5.2, you can try setting encoding to utf8mb4 and collation to utf8mb4\_unicode\_ci instead of utf8 and utf8\_unicode\_ci.  It didn't work for me, but I converted the database instead of starting with it like that from scratch, so your mileage may vary.  If you need to do this to an existing database:

                    ALTER DATABASE <database_name> CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

        - create user to interact with mysql database.  Set permissions so user has all permissions to your database.
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.mysql"
            - set the database NAME, USER, and PASSWORD.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': '<database_name>',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': '<mysql_username>',
                        'PASSWORD': '<mysql_password>',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
                }

    - For sqlite3:

        - figure out what file you want to hold the database.  For the initial implementation, we used reddit.sqlite in same directory as code (/home/socs/socs_reddit/reddit_collect/reddit.sqlite).
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.sqlite3"
            - set the database NAME (path to file), USER and PASSWORD if you set one on the database.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': '<full_path_to_database_file>',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': '',
                        'PASSWORD': '',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
                }


- in settings.py, add 'south' to the INSTALLED\_APPS list.  Example:
    
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # Uncomment the next line to enable the admin:
            # 'django.contrib.admin',
            # Uncomment the next line to enable admin documentation:
            # 'django.contrib.admindocs',
            'south',
        )

- Once database is configured in settings.py, in your site directory, run "python manage.py syncdb" to create database tables.

- in settings.py, add 'conv2wp' to the INSTALLED\_APPS list.  Example:
    
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # Uncomment the next line to enable the admin:
            # 'django.contrib.admin',
            # Uncomment the next line to enable admin documentation:
            # 'django.contrib.admindocs',
            'south',
            'conv2wp',
        )

- run `python manage.py migrate conv2wp`.

- Then, to run code, use the python shell via django, so it knows of the packages in your site:
    - python manage.py shell

## Usage

First, you need to get your blog content into the conv2wp objects:

- Make a batch instance
- create and associate a channel instance with it
- create instances for all authors, categories, tags, and terms referenced by your blog posts.
- add all authors, categories, tags, and terms referenced in any of the blog posts to the channel.
- then, add each blog post as an Item instance, associated with the channel
    - inside, create and associate authors, categories, and comments with the Item.
    
Then, you can output the blog data to a WXR XML file on the file system.

- load your batch into a Batch instance.
- call the output\_WXR\_file() method, passing it the path and file name where you want the file to be output.
- This creates a WXR file that you can import into Wordpress.

### Getting started and initialization

The easiest way to run code from a shell is to go to your django sites folder and use manage.py to open a shell:

    python manage.py shell
    
If you choose, you can also just open the base python interpreter:

    python
    
Or you can install something fancier like ipython, and then run ipython:

    ipython
    
If you don't use manage.py to open a shell (or if you are making a shell script that will be run on its own), you'll have to do a little additional setup to pull in and configure django:

    # make sure the site directory is in the sys path.
    import sys
    site_path = '<site_folder_full_path>'
    if site_path not in sys.path:
        
        sys.path.append( site_path )
        
    #-- END check to see if site path is in sys.path. --#
    
    # if not running in django shell (python manage.py shell), make sure django
    #    classes have access to settings.py
    # set DJANGO_SETTINGS_MODULE environment variable = "<site_folder_name>.settings".
    import os
    os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "<site_folder_name>.settings"

## Example

There is a complete example of how to put blog data into the conv2wp objects in the /b2e directory, in the file b2e\_importer.py.  The method that starts it all off is import\_b2e().  Pass it a slug to identify your batch with and an optional blog number.  This method will walk you through the steps and common gotchas involved in populating objects that are then turned into a WXR file.

## Notes
- official WXR sample from automattic: [https://wpcom-themes.svn.automattic.com/demo/theme-unit-test-data.xml](https://wpcom-themes.svn.automattic.com/demo/theme-unit-test-data.xml)
- Explanation of WXR files: [http://ipggi.wordpress.com/2011/03/16/the-wordpress-extended-rss-wxr-exportimport-xml-document-format-decoded-and-explained/](http://ipggi.wordpress.com/2011/03/16/the-wordpress-extended-rss-wxr-exportimport-xml-document-format-decoded-and-explained/)
- sample WXR file: [http://code.google.com/p/google-blog-converters-appengine/source/browse/trunk/samples/wordpress-sample.wxr](http://code.google.com/p/google-blog-converters-appengine/source/browse/trunk/samples/wordpress-sample.wxr)
- stack overflow on WXR: [http://stackoverflow.com/questions/9356099/wordpress-wxr-specification](http://stackoverflow.com/questions/9356099/wordpress-wxr-specification)

### Notes on HTML in post, comments
- If you have to encode to deal with special characters, make sure to replace entities for HTML characters (<, >, and ", for example) with the actual characters again once you are done.  If you don't the HTML won't parsed correctly by wordpress.
- If you need a library to encode unicode characters that won't translate to ASCII, you can use the StringHelper.unicode_escape() function, in python_utilities.strings.string_helper. 

## License

Copyright 2012, 2013 Jonathan Morgan

This file is part of [http://github.com/jonathanmorgan/conv2wp](http://github.com/jonathanmorgan/conv2wp).

conv2wp is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

conv2wp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with [http://github.com/jonathanmorgan/conv2wp](http://github.com/jonathanmorgan/conv2wp).  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).