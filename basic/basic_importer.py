'''
Copyright 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/conv2wp.

conv2wp is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

conv2wp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/conv2wp.  If not, see
<http://www.gnu.org/licenses/>.
'''

#===============================================================================#
# Imports.
#===============================================================================#

# base python imports
import datetime
import numbers
import re

# external modules
import MySQLdb
import bs4 # Beautiful Soup HTML parsing.

# conv2wp imports
from conv2wp.models import Author
from conv2wp.models import Batch
from conv2wp.models import Category
from conv2wp.models import Channel
from conv2wp.models import Comment
from conv2wp.models import Item

# python_utils imports
from python_utilities.strings.string_helper import StringHelper

#===============================================================================#
# Class definitions.
#===============================================================================#

class Basic_Importer():


    #---------------------------------------------------------------------------#
    # CONSTANTs-ish
    #---------------------------------------------------------------------------#
    
    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR - "
    
    POST_STATUS_NOW = "now"
    POST_STATUS_POST = "post"
    POST_STATUS_DRAFT = "draft"
    
    RSS_DATE_STRFTIME_FORMAT = "%a, %d %b %Y %H:%M:%S"
    
    #---------------------------------------------------------------------------#
    # instance variables
    #---------------------------------------------------------------------------#

    # database information
    db_server = "localhost"
    db_port = ""
    db_database = ""
    db_username = ""
    db_password = ""
    db_connection = None
    db_cursor = None

    # channel variables
    channel_title = ""
    channel_description = ""
    channel_wxr_version = "1.2"
    channel_generator = ""
    channel_base_site_url = ""
    channel_base_blog_url = ""

    # configuration variables
    time_zone = "-0500"
    time_zone_offset = -5
    store_excerpt = False

    
    #---------------------------------------------------------------------------#
    # class methods
    #---------------------------------------------------------------------------#


    @classmethod
    def get_testing_instance( cls, password_IN = "" ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        status_message = ""
        
        # create instance
        b2e_importer = cls()
        
        # initialize database
        b2e_importer.db_database = "b2"
        b2e_importer.db_username = "django_user"
        b2e_importer.db_password = password_IN
        
        # initialize channel information
        b2e_importer.channel_title = "Going home: A journal on Detroit's neighborhoods"
        b2e_importer.channel_description = "A Detroit News journal of the city's neighborhoods, starting with the Dobel St. area on the east side, just south of McNichols and east of Van Dyke. "
        b2e_importer.channel_generator = "https://github.com/jonathanmorgan/conv2wp"
        b2e_importer.channel_base_site_url = "http://detroitnews.com"
        b2e_importer.channel_base_blog_url = "http://community.detroitnews.com/blogs/index.php/neighborhood"
        
        # initialize time zone.
        b2e_importer.time_zone = "-0500"
        b2e_importer.time_zone_offset = -5
        
        instance_OUT = b2e_importer
        
        return instance_OUT

    #-- END method get_testing_instance() --#


    @classmethod
    def test_class( cls, password_IN = "", slug_IN = "" ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        status_message = ""
        
        # create instance
        b2e_importer = cls.get_testing_instance( password_IN )
        
        # run import for blog 14
        status_message = b2e_importer.import_b2e( slug_IN, 14 )

        # print the message
        print( status_message )
        
        # return instance
        instance_OUT = b2e_importer
        
        return instance_OUT
        
    #-- END class method test_class() --#
    

    @classmethod
    def find_bad_characters( cls, password_IN = "", blog_id_IN = -1, *args, **kwargs ):
        
        '''
        # get posts - if we have a blog ID, limit to that blog.
        
        # For each post:
        # - create Item, load with information from post.
        # - get author user, add it to Authors.
        # - get comments for post, store them in Comments, asociated to Item.
        # - get categories for post, look up and associate them.
        '''

        # return reference
        status_OUT = cls.STATUS_SUCCESS
        
        # declare variables
        b2e_importer = None
        my_db_cursor = None
        table_name_prefix = ""
        sql_select_posts = ""
        post_query_results = None
        current_post = None
        current_title = ""
        current_body = ""
        current_fail = False
        fail_list = []
        fail_count = 0
        
        # create instance
        b2e_importer = cls.get_testing_instance( password_IN )
        
        # retrieve database cursor.
        my_db_cursor = b2e_importer.get_database_cursor()
        
        # get table prefix
        table_name_prefix = b2e_importer.db_table_name_prefix
        
        # create query to retrieve posts and author information.
        sql_select_posts = "SELECT * FROM " + table_name_prefix + "posts ep"
        sql_select_posts += " INNER JOIN " + table_name_prefix + "categories ec"
        sql_select_posts += " ON ec.cat_ID = ep.post_main_cat_ID"
        
        # got a blog ID?
        if ( ( blog_id_IN ) and ( blog_id_IN != None ) and ( blog_id_IN != "" ) and ( isinstance( blog_id_IN, numbers.Integral ) == True ) and ( blog_id_IN > 0 ) ):
    
            # we do - add where clause.
            sql_select_posts += " WHERE ec.cat_blog_ID IN ( " + str( blog_id_IN ) + " )"
            
        #-- END check to see if ID passed in. --#
        
        # then, ORDER_BY.
        sql_select_posts += " ORDER BY ep.post_datecreated ASC;"
        
        # execute query
        try:

            # execute query and retrieve results        
            my_db_cursor.execute( sql_select_posts )
            query_results = my_db_cursor.fetchall()

            # loop over categories.
            for current_post in query_results:
                
                # initialize variables
                current_fail = False

                # get title and body.
                current_id = current_post[ "post_ID" ]
                current_title = current_post[ "post_title" ]
                current_body = [ "post_content" ]
                
                # look in title
                try:
                
                    # decode from utf-8 to ASCII
                    current_title.decode( 'utf-8' )
                    
                except Exception, e:
                
                    current_fail = True
                    fail_count += 1
                    print( "post " + str( current_id ) + ": Title failed." )
                
                #-- END decoding title --#

                try:
                
                    # decode from utf-8 to ASCII
                    current_body.decode( 'utf-8' )
                    
                except Exception, e:
                
                    current_fail = True
                    fail_count += 1
                    print( "post " + str( current_id ) + ": Body failed." )

                #-- END decoding title --#
                
                if ( current_fail == True ):
                
                    fail_list.append( current_id )
                    
                #-- END check to see if fail --#
            
            #-- END loop over posts. --#
            
        except Exception, e:
        
            status_OUT = cls.STATUS_PREFIX_ERROR + "Exception message: " + str( e )
        
        #-- END try/except around query --#
        
        print( "fail count: " + str( fail_count ) )
        
        if ( len( fail_list) > 0 ):
        
            status_OUT = cls.STATUS_PREFIX_ERROR + "Failure list: " + str( fail_list )
        
        #-- END check for failures --#
        
        return status_OUT
        
    #-- END method find_bad_characters() --#


    #---------------------------------------------------------------------------#
    # instance methods
    #---------------------------------------------------------------------------#


    def clean_blog_URL( self, content_IN, find_IN, replace_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""
        
        # declare variables
        soup = None
        old_host_and_path = ""
        new_host_and_path = ""
        re_string = ""
        re_compiled = None
        anchor_list = None
        current_anchor = None
        old_href_text = None
        new_href_text = None
        
        # store content in return variable.
        value_OUT = content_IN
        
        # make sure we have content before we do anything.
        if ( ( value_OUT ) and ( value_OUT != None ) and ( value_OUT != "" ) ):

            # get BeautifulSoup instance that contains content.
            soup = bs4.BeautifulSoup( value_OUT )
            
            #--------------------------------------------------------------------
            # look for http://community.detroitnews.com/blogs/index.php/neighborhood/
            #--------------------------------------------------------------------

            # prepare filtering regular expression
            re_string = "^" + find_IN
            
            # compile the regular expression.
            re_compiled = re.compile( re_string )
            
            # look for all <a> tags whose href matches that regular expression.
            anchor_list = soup.findAll( 'a', attrs = { 'href' : re_compiled } )
            
            # matches?
            if ( len( anchor_list ) > 0 ):

                # loop over all
                for current_anchor in anchor_list:
                
                    # get old href text.
                    old_href_text = current_anchor.get( "href" )
                    
                    # change old host and path to new host and path.
                    new_href_text = old_href_text.replace( find_IN, replace_IN )
                    
                    # change "_" to "-"
                    new_href_text = new_href_text.replace( "_", "-" )
                    
                    # then, in original post text, replace old URL with new URL
                    value_OUT = value_OUT.replace( old_href_text, new_href_text )
    
                #-- END loop over anchor list. --#
                
            #-- END check to see if any matches. --#

        #-- END check to see if we need to do anything. --#
        
        return value_OUT        
        
    #-- END method clean_blog_URL()


    def clean_blog_URLs( self, content_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""
        
        # declare variables
        soup = None
        old_host_and_path = ""
        new_host_and_path = ""
        re_string = ""
        re_compiled = None
        anchor_list = None
        current_anchor = None
        old_href_text = None
        new_href_text = None
        
        # store content in return variable.
        value_OUT = content_IN
        
        # make sure we have content before we do anything.
        if ( ( value_OUT ) and ( value_OUT != None ) and ( value_OUT != "" ) ):

            # store the host and path we'll switch to
            new_host_and_path = self.BLOG_URL_NEW_HOST_AND_PATH

            #--------------------------------------------------------------------
            # look for http://community.detroitnews.com/blogs/index.php/neighborhood/
            #--------------------------------------------------------------------

            # what we'll be replacing.
            old_host_and_path = self.BLOG_URL_OLD_HOST_AND_PATH_1

            # replace.
            value_OUT = self.clean_blog_URL( value_OUT, old_host_and_path, new_host_and_path )

            #--------------------------------------------------------------------
            # look for http://community.detnews.com/blogs/index.php/neighborhood/
            #--------------------------------------------------------------------

            old_host_and_path = self.BLOG_URL_OLD_HOST_AND_PATH_2

            # replace.
            value_OUT = self.clean_blog_URL( value_OUT, old_host_and_path, new_host_and_path )

        #-- END check to see if we need to do anything. --#
        
        return value_OUT        
        
    #-- END method clean_blog_URLs()


    def clean_content( self, content_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""
        
        # store content in return variable.
        value_OUT = content_IN
        
        # make sure we have content before we do anything.
        if ( ( value_OUT ) and ( value_OUT != None ) and ( value_OUT != "" ) ):
        
            # first, run the unicode escape method.
            value_OUT = StringHelper.unicode_escape( value_OUT )
            
            # !un-escape certain characters.
            
            # "&#60;" ==> "<"
            value_OUT = value_OUT.replace( "&#60;", "<" )
            
            # "&#62;" ==> ">"
            value_OUT = value_OUT.replace( "&#62;", ">" )
            
            # "&#34;" ==> """
            value_OUT = value_OUT.replace( "&#34;", "\"" )
            
            # "&#38;amp;" ==> "&amp;"
            value_OUT = value_OUT.replace( "&#38;amp;", "&amp;" )
            
            # clean old blog URLs in links.
            value_OUT = self.clean_blog_URLs( value_OUT )

        #-- END check to see if we need to do anything. --#
        
        return value_OUT        
        
    #-- END method clean_content()


    def clean_body_content( self, content_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""
        
        # store content in return variable.
        value_OUT = content_IN
        
        # make sure we have content before we do anything.
        if ( ( value_OUT ) and ( value_OUT != None ) and ( value_OUT != "" ) ):
        
            # first, run the shared clean code.
            value_OUT = self.clean_content( value_OUT )
            
        #-- END check to see if we need to do anything. --#
        
        return value_OUT        
        
    #-- END method clean_body_content()
    

    def clean_comment_content( self, content_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""
        
        # store content in return variable.
        value_OUT = content_IN
        
        # make sure we have content before we do anything.
        if ( ( value_OUT ) and ( value_OUT != None ) and ( value_OUT != "" ) ):
        
            # first, run the shared clean code.
            value_OUT = self.clean_content( value_OUT )

        #-- END check to see if we need to do anything. --#
        
        return value_OUT        
        
    #-- END method clean_comment_content()
    

    def close_db_connection( self ):
        
        # got a connection?
        if ( ( self.db_connection ) and ( self.db_connection != None ) ):
        
            # yes.  Close connection, None out the cursor variable.
            self.db_connection.close()
            self.db_connection = None
            self.db_cursor = None
            
        #-- END check to see if database connection. --#
        
    #-- END method close_db_connection()
    

    def connect_to_database( self, *args, **kwargs ):
    
        '''
        Uses database parameters contained in this instance to connect to
           database.
           
        Preconditions: at least db_database, db_username, and db_password must be
           populated in this instance.

        Postconditions: Stores connection in instance.  Returns status message.
        '''
        
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_db_server = ""
        my_db_database = ""
        my_db_username = ""
        my_db_password = ""
        my_db_connection = None
        
        # get database information.
        my_db_server = self.db_server
        my_db_database = self.db_database
        my_db_username = self.db_username
        my_db_password = self.db_password

        # got what we need?
        if ( ( my_db_server ) and ( my_db_server != None ) and ( my_db_server != "" ) ):
        
            if ( ( my_db_database ) and ( my_db_database != None ) and ( my_db_database != "" ) ):
        
                if ( ( my_db_username ) and ( my_db_username != None ) and ( my_db_username != "" ) ):

                    if ( ( my_db_password ) and ( my_db_password != None ) and ( my_db_password != "" ) ):

                        # connect.  No try/except - if this fails, program
                        #    should die.
                        my_db_connection = MySQLdb.connect( my_db_server, my_db_username, my_db_password, my_db_database )
                        
                        # If we get here, things are OK.  Store connection.
                        self.db_connection = my_db_connection

                    else:
                    
                        status_OUT = self.STATUS_PREFIX_ERROR + "No database password specified, so can't connect."
                    
                    #-- END check to see if password --#
                    
                else:
                
                    status_OUT = self.STATUS_PREFIX_ERROR + "No database username specified, so can't connect."
                
                #-- END check to see if username --#
            
            else:
                    
                status_OUT = self.STATUS_PREFIX_ERROR + "No database specified, so can't connect."
                    
            #-- END check to see if database name --#

        else:
                    
            status_OUT = self.STATUS_PREFIX_ERROR + "No database password specified, so can't connect."
                    
        #-- END check to see if server name --#

        return status_OUT
    
    #-- END method connect_to_database() --#


    def get_conv2wp_author( self, author_b2e_id_IN, *args, **kwargs ):
    
        '''
        Accepts author ID (B2E user ID).  First, checks to see if an author 
           exists for this User ID.  If yes, retrieves it. If no, pulls author
           information from B2E, uses it to create an Author instance, saves the
           instance, then returns it.
           
        Post-conditions: If no Author exists for E2 user ID passed in, creates
           Author instance and stores it in database.
        '''
    
        # return reference
        instance_OUT = None
        
        # declare variables
        sql_select_user = ""
        my_db_cursor = None
        result_count = -1
        query_result = None
        table_name_prefix = ""
        author_user_id = ""
        author_user_login = ""
        author_user_email = ""
        author_user_first_name = ""
        author_user_last_name = ""
        author_user_nickname = ""
        author_user_idmode = ""
        author_display_name = ""
        
        # try to find author by their E2 ID.
        try:
        
            # Try to get Author.
            instance_OUT = Author.objects.all().get( original_user_id = author_b2e_id_IN )
        
        except Exception, e:
        
            # not found - retrieve author information from B2E database.

            # retrieve database cursor.
            my_db_cursor = self.get_database_cursor()
            
            # get table prefix
            table_name_prefix = self.db_table_name_prefix
            
            # create query to retrieve posts and author information.
            sql_select_user = "SELECT * FROM " + table_name_prefix + "users WHERE user_ID = " + str( author_b2e_id_IN ) + ";"
            
            # execute query
            try:
    
                # execute query and retrieve results        
                my_db_cursor.execute( sql_select_user )
                
                # got something?
                result_count = my_db_cursor.rowcount
                if ( result_count > 0 ):

                    # got something.  Got one?
                    if ( result_count > 1 ):
                    
                        # more than one match.  Error.
                        print( self.STATUS_PREFIX_ERROR + "More than one user matches ID " + str( author_b2e_id_IN ) + ".  That should be impossible..." )
                        
                    #-- END sanity check. --#
                        
                    # get single row (assume we won't have multiple)
                    query_result = my_db_cursor.fetchone()

                    # create and populate Author instance.
                    instance_OUT = Author()

                    # retrieve Author values we will use.
                    author_user_id = query_result[ "user_ID" ]
                    author_user_login = query_result[ "user_login" ]
                    author_user_email = query_result[ "user_email" ]
                    author_user_first_name = query_result[ "user_firstname" ]
                    author_user_last_name = query_result[ "user_lastname" ]
                    author_user_nickname = query_result[ "user_nickname" ]
                    author_user_idmode = query_result[ "user_idmode" ]


                    # ==> original_user_id = models.IntegerField()
                    instance_OUT.original_user_id = author_user_id

                    # ==> login = models.CharField( max_length = 255, blank = True, null = True )
                    instance_OUT.login = author_user_login

                    # ==> email = models.CharField( max_length = 255, blank = True, null = True )
                    instance_OUT.email = author_user_email

                    # ==> first_name = models.CharField( max_length = 255, blank = True, null = True )
                    instance_OUT.first_name = author_user_first_name
                    
                    # ==> last_name = models.CharField( max_length = 255, blank = True, null = True )
                    instance_OUT.last_name = author_user_last_name

                    # ==> display_name = models.CharField( max_length = 255, blank = True, null = True )
                    
                    # set display name based on idmode value
                    if ( author_user_idmode == self.B2E_USER_DISPLAY_TYPE_NICKNAME ):
                    
                        # set display name to nickname
                        my_display_name = author_user_nickname
                        
                    elif ( author_user_idmode == self.B2E_USER_DISPLAY_TYPE_LOGIN ):
                    
                        # set display name to login name
                        my_display_name = author_user_login
                        
                    elif ( author_user_idmode == self.B2E_USER_DISPLAY_TYPE_NAMEFL ):
                    
                        # set display name to first name, last name
                        my_display_name = author_user_first_name + " " + author_user_last_name
                        
                    elif ( author_user_idmode == self.B2E_USER_DISPLAY_TYPE_NAMELF ):
                    
                        # set display name to last name, first name
                        my_display_name = author_user_last_name + " " + author_user_first_name
                        
                    elif ( author_user_idmode == self.B2E_USER_DISPLAY_TYPE_FIRSTNAME ):
                    
                        # set display name to first name
                        my_display_name = author_user_first_name
                        
                    elif ( author_user_idmode == self.B2E_USER_DISPLAY_TYPE_LASTNAME ):
                    
                        # set display name to last name
                        my_display_name = author_user_last_name
                        
                    else:
                    
                        # if nothing set, use nickname.
                        my_display_name = author_user_nickname
                    
                    #-- END check to see what we use as display name. --#
                    
                    # set display name
                    instance_OUT.display_name = my_display_name

                    # Fields we aren't populating.
                    # - middle_name = models.CharField( max_length = 255, blank = True, null = True )
                    # - suffix = models.CharField( max_length = 255, blank = True, null = True )
                    # - description = models.TextField( blank = True, null = True )
                    # - notes = models.TextField( blank = True, null = True )
                    # - create_date_time = models.DateTimeField( auto_now_add = True )
                    # - update_date_time = models.DateTimeField( auto_now = True )
                    # - last_export_date_time = models.DateTimeField( blank = True, null = True )
                    
                    # save it.
                    instance_OUT.save()                    
                    
                else:
                
                    # No match - return None
                    print( self.STATUS_PREFIX_ERROR + "No user matches ID " + str( author_b2e_id_IN ) + "." )
                    instance_OUT = None
                    
                #-- END check to see if query found B2E user. --#
                
            except Exception, e:
            
                # Database exception.  Output error message, return None.
                print( self.STATUS_PREFIX_ERROR + "Database error looking for B2E user " + str( author_b2e_id_IN ) + " - Exception message: " + str( e ) )
                instance_OUT = None
            
            #-- END try/except around author query --#
        
        #-- END try/except around retrieving Author --#
        
        return instance_OUT
    
    #-- END method get_conv2wp_author() --#


    def get_conv2wp_batch( self, slug_IN, blog_id_IN = -1, *args, **kwargs ):
    
        '''
        Accepts required slug (label for this batch, no spaces, please), blog ID
           if there is one.  Looks for existing batch with slug.  If found,
           returns it.  If not, Creates, saves, and returns batch for this
           conversion, based on values contained within this instance.
           
        Postconditions: Batch is stored in database before it is returned.  You
           must pass in a non-empty slug.  If no slug passed in, Exception is
           thrown.
        '''
        
        # return reference
        instance_OUT = None
        
        # look for Batch instance with slug passed in.
        try:

            # try to get batch object.                
            instance_OUT = Batch.objects.all().get( slug = slug_IN )
            print( "    - found existing." )
        
        except Exception, e:
        
            # not found - create new instance.
            instance_OUT = Batch()
            print( "    - created new ( " + str( e ) + " )." )
        
        #-- END check to see if item already is stored. --#
        
        # populate fields.

        # slug
        instance_OUT.slug = slug_IN
        
        # title
        instance_OUT.title = slug_IN + " - Converting B2E to WordPress"
        if ( blog_id_IN > 0 ):
        
            # we are just converting a specific blog.  Output that ID.
            instance_OUT.title += ", blog ID = " + str( blog_id_IN )
        
        #-- END check to see if blog ID. --#
               
        # save
        instance_OUT.save()

        return instance_OUT
    
    #-- END method get_conv2wp_batch() --#


    def get_conv2wp_channel( self, batch_IN, blog_id_IN = -1, *args, **kwargs ):
    
        '''
        Accepts required batch, blog ID if there is one.  Looks for channel for
           batch (should only be one, for now).  If finds one, returns it.  If
           not, creates one, saves, associates it with the batch, then returns 
           channel instance for this conversion, based on values contained within
           this instance.
           
        Postconditions: Channel is stored in database before it is returned, and
           is associated with Batch passed in.  You must pass in a batch.  If no
           batch passed in, Exception is thrown.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        pub_date = None
        
        # look for Batch instance with slug passed in.
        try:

            # try to get batch object.                
            instance_OUT = Channel.objects.all().get( batch = batch_IN )
            print( "    - found existing." )
        
        except Exception, e:
        
            # not found - create new instance.
            instance_OUT = Channel()
            print( "    - created new ( " + str( e ) + " )." )
        
        #-- END check to see if item already is stored. --#
        
        # populate fields.
        
        # ==> batch = models.ForeignKey( Batch )
        instance_OUT.batch = batch_IN

        # ==> title = models.CharField( max_length = 255, blank = True, null = True )
        instance_OUT.title = self.channel_title
        
        # ==> link = models.URLField( max_length = 255, blank = True, null = True )
        instance_OUT.link = self.channel_base_blog_url
        
        # ==> description = models.TextField( blank = True, null = True )
        instance_OUT.description = self.channel_description
        
        # ==> pubdate = models.CharField( max_length = 255, blank = True, null = True )
        # ==> pub_date_time = models.DateTimeField( blank = True, null = True )
        pub_date = datetime.datetime.now()
        instance_OUT.pubdate = pub_date.strftime( self.RSS_DATE_STRFTIME_FORMAT + " " + self.time_zone )
        instance_OUT.pub_date_time = pub_date

        # ==> generator = models.CharField( max_length = 255, blank = True, null = True )
        instance_OUT.generator = self.channel_generator
        
        # ==> wxr_version = models.CharField( max_length = 255, blank = True, null = True )
        instance_OUT.wxr_version = self.channel_wxr_version
        
        # ==> base_site_URL = models.URLField( max_length = 255, blank = True, null = True )
        instance_OUT.base_site_URL = self.channel_base_site_url
        
        # ==> base_blog_URL = models.URLField( max_length = 255, blank = True, null = True )
        instance_OUT.base_blog_URL = self.channel_base_blog_url

        # related authors, categories, tags, and terms will be added as posts
        #    are processed.  Need methods on Channel for adding each (look up,
        #    see if associated, if not, add association).
        # ==> authors = models.ManyToManyField( Author, blank = True, null = True )
        # ==> categories = models.ManyToManyField( Category, blank = True, null = True )
        # ==> tags = models.ManyToManyField( Tag, blank = True, null = True )
        # ==> terms = models.ManyToManyField( Term, blank = True, null = True )


        # Not setting, or leaving set to default:
        # --> cloud tag - example <cloud domain='capitalnewsservice.wordpress.com' port='80' path='/?rsscloud=notify' registerProcedure='' protocol='http-post' />
        # - cloud_domain = models.CharField( max_length = 255, blank = True, null = True )
        # - cloud_port = models.IntegerField( blank = True, null = True )
        # - cloud_path = models.CharField( max_length = 255, blank = True, null = True )
        # - cloud_register_procedure = models.CharField( max_length = 255, blank = True, null = True )
        # - cloud_protocol = models.CharField( max_length = 255, blank = True, null = True )
        # --> blog image
        # - blog_image_url = models.URLField( max_length = 255, blank = True, null = True )
        # - blog_image_title = models.CharField( max_length = 255, blank = True, null = True )
        # - blog_image_link = models.URLField( max_length = 255, blank = True, null = True )
        # --> blog open search atom link: <atom:link rel="search" type="application/opensearchdescription+xml" href="http://capitalnewsservice.wordpress.com/osd.xml" title="Capital News Service" />
        # - atom_open_search_rel = models.CharField( max_length = 255, blank = True, null = True )
        # - atom_open_search_type = models.CharField( max_length = 255, blank = True, null = True )
        # - atom_open_search_href = models.URLField( max_length = 255, blank = True, null = True )
        # - atom_open_search_title = models.CharField( max_length = 255, blank = True, null = True )
        # --> blog hub atom link: <atom:link rel='hub' href='http://capitalnewsservice.wordpress.com/?pushpress=hub'/>
        # - atom_blog_hub_rel = models.CharField( max_length = 255, blank = True, null = True )
        # - atom_blog_hub_type = models.CharField( max_length = 255, blank = True, null = True )
        # - atom_blog_hub_href = models.URLField( max_length = 255, blank = True, null = True )
        # - atom_blog_hub_title = models.CharField( max_length = 255, blank = True, null = True )
        # - create_date_time = models.DateTimeField( auto_now_add = True )
        # - last_export_date_time = models.DateTimeField( blank = True, null = True )

        # save
        instance_OUT.save()

        return instance_OUT
    
    #-- END method get_conv2wp_channel() --#


    def get_database_cursor( self, *args, **kwargs ):
    
        '''
        If cursor present in instance, returns it.  If not, if connection
           present, uses it to create, store, and return cursor.  If no
           connection, creates database connection using nested database
           information, then uses it to create, store, and return cursor.
           
        Postconditions: Cursor is stored in instance before it is returned.
        '''
        
        # return reference
        cursor_OUT = None
        
        # declare variables
        my_db_cursor = None
        my_db_connection = None
        connect_status = None
        
        # got a cursor?
        my_db_cursor = self.db_cursor
        if ( ( my_db_cursor ) and ( my_db_cursor != None ) ):
        
            # yes - return it.
            cursor_OUT = my_db_cursor
        
        else:
        
            # no cursor.  Got a connection?
            my_db_connection = self.db_connection
            if ( ( my_db_connection ) and ( my_db_connection != None ) ):
            
                # yes.  Use it to create and store cursor.
                
                # create cursor.
                my_db_cursor = my_db_connection.cursor( MySQLdb.cursors.DictCursor )
                
                # store it.
                self.db_cursor = my_db_cursor
                
                # return it.
                cursor_OUT = self.db_cursor
                
            else:
            
                # no.  Create connection, store it, then create cursor, store
                #    that, then return cursor.
                connect_status = self.connect_to_database()
                
                # retrieve connection.
                my_db_connection = self.db_connection
                
                # create cursor.
                my_db_cursor = my_db_connection.cursor( MySQLdb.cursors.DictCursor )
                
                # store it.
                self.db_cursor = my_db_cursor
                
                # return it.
                cursor_OUT = self.db_cursor
                
            #-- END check to see if we have a database connection. --#
        
        #-- END check to see if we have a database cursor already. --#
        
        return cursor_OUT
    
    #-- END method get_database_cursor() --#


    def import_blog( self, slug_IN, blog_id_IN = -1, *args, **kwargs ):
    
        '''
        Accepts an optional blog ID, imports all authors, posts, and
           comments from B2E blog into the conv2wp database tables, so we
           can then render them into a WXR file, for importing into
           Wordpress.
           
        Preconditions: Must place database information inside this instance.
        
        Postconditions: Categories, authors, blog posts, and comments will be
           added to the conv2wp tables, so they can be included in a WXR file.
           The B2E database tables will not be changed.
        '''
        
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_batch = None
        my_channel = None
        current_status = ""
        
        # get a batch instance
        my_batch = self.get_conv2wp_batch( slug_IN, blog_id_IN )
        
        # create a channel - my_channel
        my_channel = self.get_conv2wp_channel( my_batch, blog_id_IN )
        
        # get and save categories.
        current_status = self.process_categories( my_channel, blog_id_IN )
        
        # check status
        if ( current_status == self.STATUS_SUCCESS ):
        
            # process posts.
            status_OUT = self.process_posts( blog_id_IN, my_channel )
        
        else:
        
            # error processing categories.  Return message.
            status_OUT = current_status
            
        #-- END check status of processing categories. --#        
               
        # close database connection
        self.close_db_connection()
        
        return status_OUT
    
    #-- END method import_b2e --#


    def process_post( self, current_post_row_IN, channel_IN, *args, **kwargs ):

        '''
        Accepts a channel and a post row (result of querying B2E database for
           posts we want to migrate, in the form where the row is keyed by
           column name, not index of column).  Both are required.
        Then, does the following:  
        - creates Item, load with information from post.
        - get author user, add it to Authors.
        - get comments for post, store them in Comments, asociated to Item.
        - get categories for post, look up and associate them.
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # things we retrieve from post.
        current_post = None
        current_post_id = ""
        current_post_creator_user_id = ""
        current_post_datestart = ""
        current_post_datecreated = ""
        current_post_status = ""
        current_post_locale = ""
        current_post_content = ""
        current_post_title = ""
        current_post_urltitle = ""
        current_post_main_cat_id = -1
        current_post_views = -1
        current_post_wordcount = -1
        current_post_url = ""
        current_post_guid = ""
        current_post_cleaned_content = ""
        
        # variables to hold pieces of pub date.
        pub_date = None
        my_tz_offset = None
        my_tz_offset_seconds = None
        timedelta_time_zone_offset = None
        pub_date_GMT = None
        pub_date_year = -1
        pub_date_month = -1
        pub_date_day = -1
        
        # model for storing in new database.
        current_item_model = None
        
        # variables for parsing body.
        more_index = -1
        content_before_more = ""
        content_after_more = ""
        do_store_excerpt = False

        # variables for authors
        author_status = ""
        
        # variables for categories
        category_status = ""
        
        # variables for comments
        comment_status = ""
        
        # place row passed in into current_post
        current_post = current_post_row_IN

        # retrieve post values
        current_post_id = current_post[ "post_ID" ]
        current_post_creator_user_id = current_post[ "post_creator_user_ID" ]
        current_post_datestart = current_post[ "post_datestart" ] # this is the date the post was published.
        current_post_datecreated = current_post[ "post_datecreated" ]
        current_post_status = current_post[ "post_status" ]
        current_post_locale = current_post[ "post_locale" ]
        current_post_content = current_post[ "post_content" ]
        current_post_title = current_post[ "post_title" ]
        current_post_urltitle = current_post[ "post_urltitle" ]
        current_post_main_cat_id = current_post[ "post_main_cat_ID" ]
        current_post_views = current_post[ "post_views" ]
        current_post_wordcount = current_post[ "post_wordcount" ]

        # for now, just output.
        print( "- current post: " + str( current_post_id ) + " - " + current_post_title + " - " + current_post_urltitle + " - " + str( current_post_datestart ) )
        
        # check if item already exists.
        try:

            # try to get item object.                
            current_item_model = Item.objects.all().get( post_id = current_post_id )
            print( "    - found existing." )
        
        except Exception, e:
        
            # not found - create new instance.
            current_item_model = Item()
            print( "    - created new ( " + str( e ) + " )." )
        
        #-- END check to see if item already is stored. --#

        #---------------------------------------------------------------#
        # set values.
        #---------------------------------------------------------------#
        
        # ===> channel = models.ForeignKey( Channel )
        current_item_model.channel = channel_IN
        
        # ==> post_id = models.IntegerField( blank = True, null = True )
        current_item_model.post_id = current_post_id
        current_item_model.comment_status = Item.INTERACTION_STATUS_CLOSED
        
        # ==> post_status = models.CharField( max_length = 255, blank = True, null = True, default = POST_STATUS_PUBLISH )
        
        # is post published?
        if ( current_post_status == self.B2E_POST_STATUS_PUBLISHED ):
        
            # yes - set it to publish in WordPress
            current_item_model.status = Item.POST_STATUS_PUBLISH
            
        else:
        
            # no - set it to draft in WordPress
            current_item_model.status = Item.POST_STATUS_DRAFT
            
        #-- END check of status of post. --#
        
        # ==> post_name = models.CharField( max_length = 255, blank = True, null = True )
        # slug - convert underscores in the current_post_urltitle to hyphens.

        current_item_model.post_name = current_post_urltitle.replace( "_", "-" )
        
        # ==> post_date_time = models.DateTimeField( blank = True, null = True )
        # get and parse publication date.
        pub_date = current_post_datestart
        current_item_model.post_date_time = pub_date

        # ==> pubdate = models.CharField( max_length = 255, blank = True, null = True )
        # ==> pub_date_time = models.DateTimeField( blank = True, null = True )
        # convert post date to the following format: Sun, 01 Aug 2010 16:42:26 +0000 - could use either date, just get offset right (+-HHMM - GMT = +0000, EST = -0500)
        # RSS spec: http://cyber.law.harvard.edu/rss/rss.html#optionalChannelElements
        # RSS date format = http://asg.web.cmu.edu/rfc/rfc822.html#sec-5
        current_item_model.pubdate = pub_date.strftime( self.RSS_DATE_STRFTIME_FORMAT + " " + self.time_zone )
        current_item_model.pub_date_time = pub_date

        # ==> post_date_time_gmt = models.DateTimeField( blank = True, null = True )
        # add 5 hours for GMT.
        my_tz_offset = self.time_zone_offset
        
        # convert to seconds
        my_tz_offset_seconds = my_tz_offset * 3600
        
        # invert, since we are converting from local to GMT, not the
        #    other way around.
        my_tz_offset_seconds = my_tz_offset_seconds * -1

        # create timedelta for offset.
        timedelta_time_zone_offset = datetime.timedelta( 0, my_tz_offset_seconds )
        
        # convert pub date to GMT
        pub_date_GMT = pub_date + timedelta_time_zone_offset
        
        # store it.
        current_item_model.post_date_time_gmt = pub_date_GMT
        
        # parse 
        pub_date_year = pub_date.strftime( "%Y" )
        pub_date_month = pub_date.strftime( "%m" )
        pub_date_day = pub_date.strftime( "%d" )
        
        # Link and URL
        # sample - http://community.detroitnews.com/blogs/index.php/neighborhood/2013/03/28/another_blessing
        current_post_url = "http://community.detroitnews.com/blogs/index.php/neighborhood/" + pub_date_year + "/" + pub_date_month + "/" + pub_date_day + "/" + current_post_urltitle
        
        # ==> link = models.URLField( max_length = 255, blank = True, null = True )
        current_item_model.link = current_post_url

        # ==> guid = models.CharField( max_length = 255, blank = True, null = True )
        # sample - http://community.detroitnews.com/blogs/index.php?title=another_blessing
        current_post_guid = "http://community.detroitnews.com/blogs/index.php?title=" + current_post_urltitle
        current_item_model.guid = current_post_guid
        
        # ==> title = models.CharField( max_length = 255, blank = True, null = True )
        current_item_model.title = StringHelper.unicode_escape( current_post_title )

        # ==> content_encoded = models.TextField( blank = True, null = True )
        # ==> excerpt_encoded = models.TextField( blank = True, null = True, default = "" )
        
        do_store_excerpt = self.store_excerpt
        
        # locate "<!--more-->" in post.
        more_index = current_post_content.lower().find( "<!--more-->" )

        # did we find it?
        if ( more_index > -1 ):                

            # get content before and after more
            content_before_more = current_post_content[ 0 : more_index ]
            content_after_more = current_post_content[ more_index + 11 : len( current_post_content ) ]
        
            # store off excerpt?
            if ( do_store_excerpt == True ):
            
                # take everything before "<!--more-->" and place it in excerpt.
                content_before_more = self.clean_body_content( content_before_more )
                current_item_model.excerpt_encoded = content_before_more
                
            #-- END check to see if we store off excerpt --#
            
            # then, remove "<!--more-->" from complete post, store result in content_encoded.
            current_post_cleaned_content = content_before_more + "\n" + content_after_more
            
        else:
        
            # no <!--more--> - just store the content.
            current_post_cleaned_content  = current_post_content
            
        #-- END check to see if we found "<!--more-->" --#
        
        # escape unicode crap.
        current_post_cleaned_content = self.clean_body_content( current_post_cleaned_content )

        # set content encoded.
        current_item_model.content_encoded = current_post_cleaned_content

        # save item.
        current_item_model.save()
    
        #---------------------------------------------------------------#
        # Author
        #---------------------------------------------------------------#

        # ==> creators = models.ManyToManyField( Author, blank = True, null = True )
        author_status = self.process_post_author( current_post_creator_user_id, current_item_model )
        print( "    - Author status: " + author_status )
        
        #---------------------------------------------------------------#
        # Categories (main, other)
        #---------------------------------------------------------------#

        # ==> categories = models.ManyToManyField( Category, blank = True, null = True )
        category_status = self.process_post_categories( current_post_main_cat_id, current_item_model )
        print( "    - Category status: " + category_status )

        #---------------------------------------------------------------#
        # Comments
        #---------------------------------------------------------------#

        comment_status = self.process_post_comments( current_item_model )
        print( "    - Comment status: " + comment_status )

        # Fields we aren't setting (or are leaving set to default):
        # - guid_is_permalink = models.BooleanField( 'Is permalink?', default = False )
        # - description = models.TextField( blank = True, null = True, default = "" )
        # - comment_status = models.CharField( max_length = 255, choices = INTERACTION_STATUSES, blank = True, default = INTERACTION_STATUS_CLOSED )
        # - ping_status = models.CharField( max_length = 255, choices = INTERACTION_STATUSES, blank = True, default = INTERACTION_STATUS_CLOSED )
        # - post_parent = models.IntegerField( blank = True, null = True, default = 0 )
        # - menu_order = models.IntegerField( blank = True, null = True, default = 0 )
        # - post_type = models.CharField( max_length = 255, blank = True, null = True, default = ITEM_TYPE_POST )
        # - post_password = models.CharField( max_length = 255, blank = True, null = True )
        # - is_sticky = models.BooleanField( default = False )
        # - attachment_URL = models.URLField( max_length = 255, blank = True, null = True )
        # - tags = models.ManyToManyField( Tag, blank = True, null = True )
        
        # save item?
        #current_item_model.save()

        return status_OUT

    #-- END method process_post() --#
    
    
    def process_post_author( self, author_b2e_id_IN, item_IN, *args, **kwargs ):
    
        '''
        Accepts author ID (B2E user ID), and item for B2E blog post that has been
           initialized to contain all information from the post (including post
           ID).  First, checks to see if an author exists for this User ID.  If
           yes, retrieves it. If no, pulls author information from E2, uses it to
           create an Author instance.  Then, associates Author with item (and
           channel - item method should do that) and we're done.
           
        Post-conditions: creates Author instance and stores it in database if
           needed.  Also updates item and that item's related channel so Author
           is associated with each if it wasn't before.
        '''
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        author_model = None
        sql_select_user = ""
        my_db_cursor = None
        query_results = None
        table_name_prefix = ""
        
        # try to find author by their B2E ID.
        author_model = self.get_conv2wp_author( author_b2e_id_IN )
        
        # got one?
        if ( ( author_model ) and ( author_model != None ) ):
        
            # got one.  Associate it with item.
            item_IN.add_author( author_model )
            
        else:
        
            # could not find author.  Output error message.
            status_OUT = self.STATUS_PREFIX_ERROR + "Could not find B2E user for ID " + str( author_b2e_id_IN ) + ", so cannot process."

        #-- END check to see if we got an author for user ID. --#
        
        return status_OUT
    
    #-- END method process_post_author() --#


    def process_posts( self, blog_id_IN = -1, channel_IN = None, *args, **kwargs ):
        
        '''
        # get posts - if we have a blog ID, limit to that blog.
        
        # For each post:
        # - create Item, load with information from post.
        # - get author user, add it to Authors.
        # - get comments for post, store them in Comments, asociated to Item.
        # - get categories for post, look up and associate them.
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_db_cursor = None
        table_name_prefix = ""
        sql_select_posts = ""
        post_query_results = None
        current_post = None
        
        # retrieve database cursor.
        my_db_cursor = self.get_database_cursor()
        
        # get table prefix
        table_name_prefix = self.db_table_name_prefix
        
        # create query to retrieve posts and author information.
        sql_select_posts = "SELECT * FROM " + table_name_prefix + "posts ep"
        sql_select_posts += " INNER JOIN " + table_name_prefix + "categories ec"
        sql_select_posts += " ON ec.cat_ID = ep.post_main_cat_ID"
        
        # got a blog ID?
        if ( ( blog_id_IN ) and ( blog_id_IN != None ) and ( blog_id_IN != "" ) and ( isinstance( blog_id_IN, numbers.Integral ) == True ) and ( blog_id_IN > 0 ) ):
    
            # we do - add where clause.
            sql_select_posts += " WHERE ec.cat_blog_ID IN ( " + str( blog_id_IN ) + " )"
            
        #-- END check to see if ID passed in. --#
        
        # then, ORDER_BY.
        sql_select_posts += " ORDER BY ep.post_datecreated ASC;"
        
        # execute query
        try:

            # execute query and retrieve results        
            my_db_cursor.execute( sql_select_posts )
            query_results = my_db_cursor.fetchall()

            # loop over categories.
            for current_post in query_results:
                
                # process post
                self.process_post( current_post, channel_IN )
            
            #-- END loop over posts. --#
            
        except Exception, e:
        
            status_OUT = self.STATUS_PREFIX_ERROR + "Exception message: " + str( e )
        
        #-- END try/except around query --#
        
        return status_OUT
        
    #-- END method process_posts() --#


    def __del__( self ):
        
        # close database connection.
        self.close_db_connection()
        
    #-- END method __del__() --#
    

    def __unicode__( self ):

        # return reference
        string_OUT = ""
        
        string_OUT = "basic_importer - server: " + self.db_server + "; database: " + self.db_database + "; username: " + self.db_username

        return string_OUT

    #-- END __unicode()__ method --#


#-- END Basic_Importer class --#