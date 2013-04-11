# conv2wordpress

Django application that helps to convert content from other blogs to Wordpress WordPress eXtended RSS (WXR) files.

## Installation

### Dependencies

The core conv2wp classes just make use of base python packages and django.  The B2Evolution import code uses a few routines from the python_utilities package ( [https://github.com/jonathanmorgan/python_utilities](https://github.com/jonathanmorgan/python_utilities) ) and use Beautiful Soup version 4.

### Install

If you are migrating from blog software and will be reading blog posts out of a database, the easiest way to use conv2wp is to install the conv2wp django app in the database that also contains the files from which you will be getting data.  To do this:

- start a django site.
- configure your settings.py file so you can connect to a database.
- check out the conv2wp application into the base directory for your django site.
    - git clone https://github.com/jonathanmorgan/conv2wp ./
- sync django with the database.
    - python manage.py syncdb
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