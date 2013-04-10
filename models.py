# Imports

# base python modules.
import datetime
import codecs

# django
from django.db import models

# Create your models here.

class Batch( models.Model ):

    #----------------------------------------------------------------------
    # declaring a few "constants"
    #----------------------------------------------------------------------

    # status messages.
    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR - "


    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    slug = models.CharField( max_length = 255 )
    title = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date_time = models.DateTimeField( auto_now_add = True )
    update_date_time = models.DateTimeField( auto_now = True )
    last_export_date_time = models.DateTimeField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def output_WXR_file( self, output_file_path_IN = "", time_zone_IN = "-0500", *args, **kwargs ):

        '''
        This method accepts a file path, opens the file for writing, then
           outputs the <xml> and <rss> elements before handing off the file
           handle to the channel model, which outputs the rest of the XML.
        '''
        
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        output_file_handle = None
        my_channel_rs = None
        my_channel_count = -1
        current_channel = None
        
        # make sure we have a file path.
        if ( ( output_file_path_IN ) and ( output_file_path_IN != None ) and ( output_file_path_IN != "" ) ):
        
            # Get nested channel instance(s).
            my_channel_rs = self.channel_set.all()
            my_channel_count = my_channel_rs.count()
                
            # make sure we have at least one.
            if ( my_channel_count > 0 ):

                # we do.  open path for writing.
                # with open( output_file_path_IN, "w" ) as output_file_handle:
                with codecs.open( output_file_path_IN, "w", 'utf-8' ) as output_file_handle:
                
                    # output opening xml element, comment that outlines the generator, and 
                    #    opening rss tag.
                    output_file_handle.write( "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" )
                    output_file_handle.write( "<!-- generator=\"https://github.com/jonathanmorgan/conv2wp\" created=\"" + datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S" ) + "\" -->\n" )
                    output_file_handle.write( "<rss version=\"2.0\" xmlns:excerpt=\"http://wordpress.org/export/1.2/excerpt/\" xmlns:content=\"http://purl.org/rss/1.0/modules/content/\" xmlns:wfw=\"http://wellformedweb.org/CommentAPI/\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:wp=\"http://wordpress.org/export/1.2/\">\n" )
                
                    # loop over channels, passing each the file for output.
                    for current_channel in my_channel_rs:
                    
                        # call the output_WXR_to_file() method on channel.
                        current_channel.output_WXR_to_file( output_file_handle, time_zone_IN )
                    
                    #-- END loop over channels. --#
                    
                    # close the <rss> element, then close the file.
                    output_file_handle.write( "</rss>\n" )
                    output_file_handle.close()
                
                #-- END with open ( output_file_path_IN ) --#
                
            #-- END check to make sure we have a channel --#
        
        else:
        
            status_OUT = self.STATUS_PREFIX_ERROR + "No file path passed in, so can't output." 
        
        #-- END check to make sure we have a path. --#
        
        return status_OUT
        
    #-- END method to_WXR_string()
    

    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.title + " (" + self.update_date_time.strftime( "%b %d, %Y" ) + ")"
        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Batch --#

#===============================================================================#
# Models that are components of an item.
#===============================================================================#

# Author model
class Author( models.Model ):


    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    login = models.CharField( max_length = 255, blank = True, null = True )
    email = models.CharField( max_length = 255, blank = True, null = True )
    display_name = models.CharField( max_length = 255, blank = True, null = True )
    first_name = models.CharField( max_length = 255, blank = True, null = True )
    middle_name = models.CharField( max_length = 255, blank = True, null = True )
    last_name = models.CharField( max_length = 255, blank = True, null = True )
    suffix = models.CharField( max_length = 255, blank = True, null = True )
    original_user_id = models.IntegerField()
    description = models.TextField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date_time = models.DateTimeField( auto_now_add = True )
    update_date_time = models.DateTimeField( auto_now = True )
    last_export_date_time = models.DateTimeField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def to_xml_string( self, *args, **kwargs ):
        
        '''
        Example:
        <wp:wp_author>
            <wp:author_login>themedemos</wp:author_login>
            <wp:author_email>nanobar+demos@gmail.com</wp:author_email>
            <wp:author_display_name><![CDATA[Theme Buster]]></wp:author_display_name>
            <wp:author_first_name><![CDATA[]]></wp:author_first_name>
            <wp:author_last_name><![CDATA[]]></wp:author_last_name>
        </wp:wp_author>
        '''
        
        # return reference
        value_OUT = ""
        
        value_OUT += "        <wp:wp_author>\n"
        value_OUT += "            <wp:author_login>" + self.login + "</wp:author_login>\n"
        value_OUT += "            <wp:author_email>" + self.email + "</wp:author_email>\n"
        value_OUT += "            <wp:author_display_name><![CDATA[" + self.display_name + "]]></wp:author_display_name>\n"
        value_OUT += "            <wp:author_first_name><![CDATA[" + self.first_name + "]]></wp:author_first_name>\n"
        value_OUT += "            <wp:author_last_name><![CDATA[" + self.last_name + "]]></wp:author_last_name>\n"
        value_OUT += "        </wp:wp_author>\n"        
        
        return value_OUT
        
    #-- END method to_xml_string() --#

    
    def __unicode__( self ):

        # return reference
        string_OUT = ""

        # declare variables
        separator = ""

        string_OUT = str( self.id ) + " - "
        
        if ( self.last_name ):

            string_OUT += self.last_name
            separator = ", "

        if ( self.first_name ):

            string_OUT += separator + self.first_name
            separator = " "

        if ( self.middle_name ):

            string_OUT += separator + self.middle_name
            separator = " "

        # eventually add in email addresses.

        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Author --#


# Category model
class Category( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    term_id = models.IntegerField()
    nice_name = models.CharField( max_length = 255 )
    parent_category = models.ForeignKey( 'self', blank = True, null = True )
    name = models.CharField( max_length = 255 )

    # housekeeping
    label = models.CharField( max_length = 255 )
    description = models.TextField( blank = True, null = True )
    last_modified = models.DateField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def to_xml_string( self, *args, **kwargs ):

        '''
        Sample:
        <wp:category>
            <wp:term_id>33280</wp:term_id>
            <wp:category_nicename>arrangement</wp:category_nicename>
            <wp:category_parent></wp:category_parent>
            <wp:cat_name><![CDATA[arrangement]]></wp:cat_name>
        </wp:category>
        '''
        
        # return reference
        value_OUT = ""

        # declare variables
        parent_id = ""
        
        # create WXR XML
        value_OUT += "        <wp:category>\n"
        value_OUT += "            <wp:term_id>" + str( self.term_id ) + "</wp:term_id>\n"
        value_OUT += "            <wp:category_nicename>" + self.nice_name + "</wp:category_nicename>\n"
        
        # do we have a parent category?
        if ( ( self.parent_category ) and ( self.parent_category != None ) ):
        
            # yes.  Set parent ID.
            parent_id = self.parent_category.term_id
            
        #-- END check to see if parent category --#
    
        value_OUT += "            <wp:category_parent>" + str( parent_id ) + "</wp:category_parent>\n"
        value_OUT += "            <wp:cat_name><![CDATA[" + self.name + "]]></wp:cat_name>\n"
        value_OUT += "        </wp:category>\n"
        
        return value_OUT
        
    #-- END method to_xml_string() --#

    
    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.name
        return string_OUT

#= End Category Model =========================================================


# Tag model
class Tag( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    term_id = models.IntegerField( blank = True, null = True )
    slug = models.CharField( max_length = 255 )
    name = models.CharField( max_length = 255 )

    # housekeeping
    label = models.CharField( max_length = 255 )
    description = models.TextField( blank = True )
    last_modified = models.DateField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.name
        return string_OUT

#= End Tag Model =========================================================


# Term model
class Term( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    term_id = models.IntegerField( blank = True, null = True )
    term_taxonomy = models.CharField( max_length = 255 )
    slug = models.CharField( max_length = 255 )
    name = models.CharField( max_length = 255 )

    # housekeeping
    label = models.CharField( max_length = 255 )
    description = models.TextField( blank = True )
    last_modified = models.DateField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.name
        return string_OUT

#= End Term Model =========================================================


# Channel model
class Channel( models.Model ):


    #----------------------------------------------------------------------
    # declaring a few "constants"
    #----------------------------------------------------------------------

    # status messages.
    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR - "


    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    # !TODO add language field, time zone field.

    # housekeeping
    batch = models.ForeignKey( Batch )
    create_date_time = models.DateTimeField( auto_now_add = True )
    last_export_date_time = models.DateTimeField( blank = True, null = True )

    # information on channel.
    title = models.CharField( max_length = 255, blank = True, null = True )
    link = models.URLField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    pubdate = models.CharField( max_length = 255, blank = True, null = True )
    pub_date_time = models.DateTimeField( blank = True, null = True )
    generator = models.CharField( max_length = 255, blank = True, null = True )
    wxr_version = models.CharField( max_length = 255, blank = True, null = True )
    base_site_URL = models.URLField( max_length = 255, blank = True, null = True )
    base_blog_URL = models.URLField( max_length = 255, blank = True, null = True )

    # related authors, categories, tags, and terms
    authors = models.ManyToManyField( Author, blank = True, null = True )
    categories = models.ManyToManyField( Category, blank = True, null = True )
    tags = models.ManyToManyField( Tag, blank = True, null = True )
    terms = models.ManyToManyField( Term, blank = True, null = True )

    # - cloud tag - example <cloud domain='capitalnewsservice.wordpress.com' port='80' path='/?rsscloud=notify' registerProcedure='' protocol='http-post' />
    cloud_domain = models.CharField( max_length = 255, blank = True, null = True )
    cloud_port = models.IntegerField( blank = True, null = True )
    cloud_path = models.CharField( max_length = 255, blank = True, null = True )
    cloud_register_procedure = models.CharField( max_length = 255, blank = True, null = True )
    cloud_protocol = models.CharField( max_length = 255, blank = True, null = True )

    # blog image
    blog_image_url = models.URLField( max_length = 255, blank = True, null = True )
    blog_image_title = models.CharField( max_length = 255, blank = True, null = True )
    blog_image_link = models.URLField( max_length = 255, blank = True, null = True )

    # - blog open search atom link: <atom:link rel="search" type="application/opensearchdescription+xml" href="http://capitalnewsservice.wordpress.com/osd.xml" title="Capital News Service" />
    atom_open_search_rel = models.CharField( max_length = 255, blank = True, null = True )
    atom_open_search_type = models.CharField( max_length = 255, blank = True, null = True )
    atom_open_search_href = models.URLField( max_length = 255, blank = True, null = True )
    atom_open_search_title = models.CharField( max_length = 255, blank = True, null = True )

    # - blog hub atom link: <atom:link rel='hub' href='http://capitalnewsservice.wordpress.com/?pushpress=hub'/>
    atom_blog_hub_rel = models.CharField( max_length = 255, blank = True, null = True )
    atom_blog_hub_type = models.CharField( max_length = 255, blank = True, null = True )
    atom_blog_hub_href = models.URLField( max_length = 255, blank = True, null = True )
    atom_blog_hub_title = models.CharField( max_length = 255, blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def add_author( self, author_IN, *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_author_set = None
        author_id = -1
        author_rs = None
        author_rs_count = -1
        
        # get author set.
        my_author_set = self.authors
        
        # get author's ID.
        author_id = author_IN.id

        # check to see if author is already associated.
        author_rs = my_author_set.filter( pk = author_id )
        
        # got anything?
        author_rs_count = author_rs.count()
        if ( author_rs_count <= 0 ):
        
            # no - associate author with this instance.
            my_author_set.add( author_IN )

        #-- END check to make sure the author isn't already in there. --#
 
        return status_OUT
    
    #-- END method add_author() --#


    def add_category( self, category_IN, *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_category_set = None
        category_id = -1
        category_rs = None
        category_rs_count = -1
        
        # get category set.
        my_category_set = self.categories
        
        # get category's ID.
        category_id = category_IN.id

        # check to see if category is already associated.
        category_rs = my_category_set.filter( pk = category_id )
        
        # got anything?
        category_rs_count = category_rs.count()
        if ( category_rs_count <= 0 ):
        
            # no - associate category with this instance.
            my_category_set.add( category_IN )

        #-- END check to make sure the category isn't already in there. --#
 
        return status_OUT
    
    #-- END method add_category() --#


    def output_WXR_to_file( self, file_object_IN, time_zone_IN = "-0500", *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        me = "output_WXR_to_file"
        current_string = ""
        author_rs = None
        current_author = None
        category_rs = None
        current_category = None
        item_rs = None
        current_item = None
        post_fail_list = []
        post_fail_count = 0
        
        # make sure we have an open file.
        if ( ( file_object_IN ) and ( file_object_IN != None ) and ( file_object_IN.closed == False ) ):
        
            # file is OK.  Output channel element.
            file_object_IN.write( "    <channel>\n" )
            file_object_IN.write( "        <title>" + self.title + "</title>\n" )
            file_object_IN.write( "        <link>" + self.link + "</link>\n" )
            file_object_IN.write( "        <description>" + self.description + "</description>\n" )
            file_object_IN.write( "        <pubDate>" + datetime.datetime.now().strftime( "%a, %d %b %Y %H:%M:%S" ) + " " + time_zone_IN + "</pubDate>\n" )
            file_object_IN.write( "        <language>en</language>\n" )
            file_object_IN.write( "        <wp:wxr_version>" + self.wxr_version + "</wp:wxr_version>\n" )
            file_object_IN.write( "        <wp:base_site_url>" + self.base_site_URL + "</wp:base_site_url>\n" )
            file_object_IN.write( "        <wp:base_blog_url>" + self.base_blog_URL + "</wp:base_blog_url>\n" )

            #-------------------------------------------------------------------#
            # output associated authors
            #-------------------------------------------------------------------#

            author_rs = self.authors.all()  
            for current_author in author_rs:
            
                # have author render itself as XML string.
                current_string = current_author.to_xml_string()
                
                # write that string to the file.
                file_object_IN.write( current_string + "\n" )
            
            #-- END loop over authors --#

            #-------------------------------------------------------------------#
            # output associated categories
            #-------------------------------------------------------------------#

            category_rs = self.categories.all()
            for current_category in category_rs:
            
                # have author render itself as XML string.
                current_string = current_category.to_xml_string()
                
                # write that string to the file.
                file_object_IN.write( current_string + "\n" )
            
            #-- END loop over categories --#
            
            # !TODO - tags and terms.
            
            # output the rest of the channel XML.
            file_object_IN.write( "        <generator>" + self.generator + "</generator>\n" )

            # !TODO - more channel elements.

            '''
        <cloud domain='wpthemetestdata.wordpress.com' port='80' path='/?rsscloud=notify' registerProcedure='' protocol='http-post' />
        <image>
            <url>https://s2.wp.com/i/buttonw-com.png</url>
            <title>Theme Unit Test Data</title>
            <link>http://wpthemetestdata.wordpress.com</link>
        </image>
        <atom:link rel="search" type="application/opensearchdescription+xml" href="http://wpthemetestdata.wordpress.com/osd.xml" title="Theme Unit Test Data" />
        <atom:link rel='hub' href='http://wpthemetestdata.wordpress.com/?pushpress=hub'/>
            '''            
            
            #-------------------------------------------------------------------#
            # output associated posts
            #-------------------------------------------------------------------#
            
            item_rs = self.item_set.all()
            for current_item in item_rs:
            
                # have item render itself as XML string.
                current_string = current_item.to_xml_string()
                
                try:

                    # write that string to the file.
                    file_object_IN.write( current_string + "\n" )

                except Exception, e:
                
                    # print the current_string
                    post_fail_count += 1
                    post_fail_list.append( current_item.id )
                    # print( current_string )
                
                #-- END try/except --#
            
            #-- END loop over posts --#
            
            # output post failure information.
            print( "- In " + me + "(): post fail count: " + str( post_fail_count ) + "; post_fail_list: " + str( post_fail_list ) )
            
            # close out the channel element.
            file_object_IN.write( "    </channel>\n" )

        else:
        
            status_OUT = self.STATUS_PREFIX_ERROR + "In " + me + "(): File not valid.  Not outputting anything."
        
        #-- END check to see if file is OK.
        
        return status_OUT
    
    #-- END method output_WXR_to_file() --#
    
    
    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.title + " (" + self.pub_date_time.strftime( "%b %d, %Y" ) + ")"
        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Channel --#


class EmailAddress( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    author = models.ForeignKey( Author )
    email_address = models.CharField( max_length = 255 )
    create_date_time = models.DateTimeField( auto_now_add = True )
    update_date_time = models.DateTimeField( auto_now = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.email_address

        if ( creator ):

            # output creator's information
            string_OUT += ": " + str( creator )

        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Batch --#

#===============================================================================#
# Item model itself.
#===============================================================================#

# Item model
class Item( models.Model ):

    '''
    Item based on Wordpress eXtended RSS file spec (WXR).  Sample document at:
    https://wpcom-themes.svn.automattic.com/demo/theme-unit-test-data.xml
    '''

    # !TODO add Author, Category, Comment to Item
    # create methods that add the above to the Item, and also associate
    #    them with Related Channel.

    #----------------------------------------------------------------------
    # declaring a few "constants"
    #----------------------------------------------------------------------

    INTERACTION_STATUS_OPEN = "open"
    INTERACTION_STATUS_CLOSED = "closed"
    INTERACTION_STATUSES = (
        ( "open", "Open" ),
        ( "closed", "Closed" )
    )

    POST_STATUS_DRAFT = "draft"
    POST_STATUS_PUBLISH = "publish"
    POST_STATUS_INHERIT = "inherit"

    ITEM_TYPE_POST = "post"
    ITEM_TYPE_PAGE = "page"
    ITEM_TYPE_ATTACHMENT = "attachment"
    
    # isPermaLink values
    IS_PERMA_LINK_TRUE = "true"
    IS_PERMA_LINK_FALSE = "false"
    
    # date format strings
    DATE_FORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S"
    
    # status messages.
    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR - "


    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    channel = models.ForeignKey( Channel )
    title = models.CharField( max_length = 255, blank = True, null = True )
    link = models.URLField( max_length = 255, blank = True, null = True )
    pubdate = models.CharField( max_length = 255, blank = True, null = True )
    pub_date_time = models.DateTimeField( blank = True, null = True )
    creators = models.ManyToManyField( Author, blank = True, null = True )
    guid = models.CharField( max_length = 255, blank = True, null = True )
    guid_is_permalink = models.BooleanField( 'Is permalink?', default = False )
    description = models.TextField( blank = True, null = True, default = "" )
    content_encoded = models.TextField( blank = True, null = True )
    excerpt_encoded = models.TextField( blank = True, null = True, default = "" )
    post_id = models.IntegerField( blank = True, null = True )
    post_date_time = models.DateTimeField( blank = True, null = True )
    post_date_time_gmt = models.DateTimeField( blank = True, null = True )
    comment_status = models.CharField( max_length = 255, choices = INTERACTION_STATUSES, blank = True, default = INTERACTION_STATUS_CLOSED )
    ping_status = models.CharField( max_length = 255, choices = INTERACTION_STATUSES, blank = True, default = INTERACTION_STATUS_CLOSED )
    post_name = models.CharField( max_length = 255, blank = True, null = True )
    post_status = models.CharField( max_length = 255, blank = True, null = True, default = POST_STATUS_PUBLISH )
    post_parent = models.IntegerField( blank = True, null = True, default = 0 )
    menu_order = models.IntegerField( blank = True, null = True, default = 0 )
    post_type = models.CharField( max_length = 255, blank = True, null = True, default = ITEM_TYPE_POST )
    post_password = models.CharField( max_length = 255, blank = True, null = True, default = "" )
    is_sticky = models.BooleanField( default = False )
    attachment_URL = models.URLField( max_length = 255, blank = True, null = True )
    categories = models.ManyToManyField( Category, blank = True, null = True )
    tags = models.ManyToManyField( Tag, blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def add_author( self, author_IN, *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_author_set = None
        author_id = -1
        author_rs = None
        author_rs_count = -1
        
        # get author set.
        my_author_set = self.creators
        
        # get author's ID.
        author_id = author_IN.id

        # check to see if author is already associated.
        author_rs = my_author_set.filter( pk = author_id )
        
        # got anything?
        author_rs_count = author_rs.count()
        if ( author_rs_count <= 0 ):
        
            # no - associate author with this instance.
            my_author_set.add( author_IN )

        #-- END check to make sure the author isn't already in there. --#
 
        # add to list of authors associated with current channel.
        self.channel.add_author( author_IN )
        
        return status_OUT
    
    #-- END method add_author() --#


    def add_category( self, category_IN, *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_category_set = None
        category_id = -1
        category_rs = None
        category_rs_count = -1
        
        # get category set.
        my_category_set = self.categories
        
        # get category's ID.
        category_id = category_IN.id

        # check to see if category is already associated.
        category_rs = my_category_set.filter( pk = category_id )
        
        # got anything?
        category_rs_count = category_rs.count()
        if ( category_rs_count <= 0 ):
        
            # no - associate category with this instance.
            my_category_set.add( category_IN )

        #-- END check to make sure the category isn't already in there. --#
 
        # add to list of categories associated with current channel.
        self.channel.add_category( category_IN )
        
        return status_OUT
    
    #-- END method add_category() --#


    def to_xml_string( self, *args, **kwargs ):

        # return reference
        value_OUT = ""
        
        # declare variables
        author_rs = None
        current_author = None
        author_login = ""
        is_permalink_string = ""
        is_sticky_string = ""
        password_string = ""
        
        # variables for processing categories.
        category_rs = None
        category_count = -1
        current_category = None
        category_domain = ""
        category_name = ""
        category_nice_name = ""
        
        # variables for processing comments
        comment_rs = None
        comment_count = -1
        current_comment = None
        comment_string = ""
        
        # render XML
        value_OUT += "        <item>\n"
        value_OUT += "            <title>" + self.title + "</title>\n"
        value_OUT += "            <link>" + self.link + "</link>\n"
        value_OUT += "            <pubDate>" + self.pubdate + "</pubDate>\n"
        
        # author(s)
        author_rs = self.creators.all()
        for current_author in author_rs:
        
            # output creator tag
            value_OUT += "            <dc:creator>" + current_author.login + "</dc:creator>\n"
            
        #-- END loop over authors. --#
        
        # isPermaLink string
        if ( self.guid_is_permalink == True ):
        
            # yes - set to "true"
            is_permalink_string = self.IS_PERMA_LINK_TRUE

        else:
        
            # no - set to "false"
            is_permalink_string = self.IS_PERMA_LINK_FALSE
            
        #-- END set isPermaLink string value. --#
        
        value_OUT += "            <guid isPermaLink=\"" + is_permalink_string + "\">" + self.guid + "</guid>\n"
        value_OUT += "            <description>" + self.description + "</description>\n"
        value_OUT += "            <content:encoded><![CDATA[" + self.content_encoded + "]]></content:encoded>\n"
        value_OUT += "            <excerpt:encoded><![CDATA[" + self.excerpt_encoded + "]]></excerpt:encoded>\n"
        value_OUT += "            <wp:post_id>" + str( self.post_id ) + "</wp:post_id>\n"
        value_OUT += "            <wp:post_date>" + self.post_date_time.strftime( self.DATE_FORMAT_DEFAULT ) + "</wp:post_date>\n"
        value_OUT += "            <wp:post_date_gmt>" + self.post_date_time_gmt.strftime( self.DATE_FORMAT_DEFAULT ) + "</wp:post_date_gmt>\n"
        value_OUT += "            <wp:comment_status>" + self.comment_status + "</wp:comment_status>\n"
        value_OUT += "            <wp:ping_status>" + self.ping_status + "</wp:ping_status>\n"
        value_OUT += "            <wp:post_name>" + self.post_name + "</wp:post_name>\n"
        value_OUT += "            <wp:status>" + self.post_status + "</wp:status>\n"
        value_OUT += "            <wp:post_parent>" + str( self.post_parent ) + "</wp:post_parent>\n"
        value_OUT += "            <wp:menu_order>" + str( self.menu_order ) + "</wp:menu_order>\n"
        value_OUT += "            <wp:post_type>" + self.post_type + "</wp:post_type>\n"
        
        password_string = self.post_password
        if ( password_string == None ):
        
            password_string = ""
            
        #-- END check to see if password is None --#
        
        value_OUT += "            <wp:post_password>" + password_string + "</wp:post_password>\n"

        # is_sticky string
        if ( self.is_sticky == True ):
        
            # yes - set to "1"
            is_sticky_string = "1"

        else:
        
            # no - set to "0"
            is_sticky_string = "0"
            
        #-- END set isPermaLink string value. --#

        value_OUT += "            <wp:is_sticky>" + is_sticky_string + "</wp:is_sticky>\n"
        
        # !TODO tags
        
        # do we have any categories?
        category_rs = self.categories.all()
        category_count = category_rs.count()
        if ( category_count > 0 ):
        
            # we do.  loop and output each.
            # sample: <category domain="category" nicename="uncategorized"><![CDATA[Uncategorized]]></category>
            
            for current_category in category_rs:

                # get values
                category_domain = "category" # (always category for now)
                category_name = current_category.name
                category_nice_name = current_category.nice_name

                # output.
                value_OUT += "            <category domain=\"" + category_domain + "\" nicename=\"" + category_nice_name + "\"><![CDATA[" + category_name + "]]></category>\n"

            #-- END loop over categories. --#
        
        #-- END check to see if we have any categories. --#
        
        # !TODO wp:meta
        
        # do we have any comments?
        comment_rs = self.comment_set.all()
        comment_count = comment_rs.count()
        if ( comment_count > 0 ):
        
            # we do.  loop and output each.
            for current_comment in comment_rs:

                # get xml string
                comment_string = current_comment.to_xml_string()

                # add it to output.
                value_OUT += comment_string + "\n"

            #-- END loop over categories. --#
        
        #-- END check to see if we have any comments --#
        
        value_OUT += "        </item>\n"
        
        return value_OUT
        
    #-- END method to_xml_string() --#

    
    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.title + " (" + self.pub_date_time.strftime( "%b %d, %Y" ) + ")"
        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Item --#


#===============================================================================#
# Things that reference Item model.
#===============================================================================#

# PostMetaData model
class PostMetaData( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    item = models.ForeignKey( Item )
    key = models.CharField( max_length = 255 )
    value = models.TextField( blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    last_modified = models.DateField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'item' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.name + ": " + self.value
        return string_OUT

#= End PostMetaData Model =========================================================


# Comment model
class Comment( models.Model ):


    #----------------------------------------------------------------------
    # declaring a few "constants"
    #----------------------------------------------------------------------

    COMMENT_STATUS_APPROVED = True
    COMMENT_STATUS_NOT_APPROVED = False
    
    COMMENT_TYPE_COMMENT = "comment"

    # date format strings
    DATE_FORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S"
    

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    item = models.ForeignKey( Item )
    comment_id = models.IntegerField( blank = True, null = True )
    author_name = models.CharField( max_length = 255, blank = True, null = True )
    author_email = models.CharField( max_length = 255, blank = True, null = True )
    author_url = models.CharField( max_length = 255, blank = True, null = True )
    author_ip = models.CharField( max_length = 255, blank = True, null = True )
    comment_date_time = models.DateTimeField( blank = True, null = True )
    comment_date_time_gmt = models.DateTimeField( blank = True, null = True )
    content_encoded = models.TextField( blank = True, null = True )
    approved = models.BooleanField( default = False )
    comment_type = models.CharField( max_length = 255, blank = True, null = True, default = "" )
    parent_comment = models.ForeignKey( 'self', blank = True, null = True )
    comment_author = models.ForeignKey( Author, blank = True, null = True )

    # housekeeping
    description = models.TextField( blank = True, null = True )
    last_modified = models.DateField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ '-comment_date_time' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def to_xml_string( self, *args, **kwargs ):

        '''
        Sample:
            <wp:comment>
                <wp:comment_id>167</wp:comment_id>
                <wp:comment_author><![CDATA[Anon]]></wp:comment_author>
                <wp:comment_author_email>anon@example.com</wp:comment_author_email>
                <wp:comment_author_url></wp:comment_author_url>
                <wp:comment_author_IP>59.167.157.3</wp:comment_author_IP>
                <wp:comment_date>2007-09-04 10:49:28</wp:comment_date>
                <wp:comment_date_gmt>2007-09-04 00:49:28</wp:comment_date_gmt>
                <wp:comment_content><![CDATA[Anonymous comment.]]></wp:comment_content>
                <wp:comment_approved>1</wp:comment_approved>
                <wp:comment_type></wp:comment_type>
                <wp:comment_parent>0</wp:comment_parent>
                <wp:comment_user_id>0</wp:comment_user_id>
            </wp:comment>
        '''

        # return reference
        value_OUT = ""

        # declare variables
        author_url_string = ""
        author_ip_string = ""
        comment_approved_string = "0"
        comment_type_string = ""
        parent_comment_id = 0
        comment_author_id = 0
        
        # output.
        value_OUT += "            <wp:comment>\n"
        value_OUT += "                <wp:comment_id>" + str( self.comment_id ) + "</wp:comment_id>\n"
        value_OUT += "                <wp:comment_author><![CDATA[" + self.author_name + "]]></wp:comment_author>\n"
        value_OUT += "                <wp:comment_author_email>" + self.author_email + "</wp:comment_author_email>\n"
        
        author_url_string = self.author_url
        if ( author_url_string == None ):
        
            author_url_string = ""
            
        #-- END check to see if author URL is None --#
        
        value_OUT += "                <wp:comment_author_url>" + author_url_string + "</wp:comment_author_url>\n"

        author_ip_string = self.author_ip
        if ( author_ip_string == None ):
        
            author_ip_string = ""
            
        #-- END check to see if author IP is None --#
        
        value_OUT += "                <wp:comment_author_IP>" + author_ip_string + "</wp:comment_author_IP>\n"

        value_OUT += "                <wp:comment_date>" + self.comment_date_time.strftime( self.DATE_FORMAT_DEFAULT ) + "</wp:comment_date>\n"
        value_OUT += "                <wp:comment_date_gmt>" + self.comment_date_time_gmt.strftime( self.DATE_FORMAT_DEFAULT ) + "</wp:comment_date_gmt>\n"
        value_OUT += "                <wp:comment_content><![CDATA[" + self.content_encoded + "]]></wp:comment_content>\n"

        # set comment_approved string.
        if ( self.approved == True ):
        
            # yes - set to "1"
            comment_approved_string = "1"

        else:
        
            # no - set to "0"
            comment_approved_string = "0"
            
        #-- END set comment_approved string value. --#

        value_OUT += "                <wp:comment_approved>" + comment_approved_string + "</wp:comment_approved>\n"

        # got a comment type?
        if ( ( self.comment_type ) and ( self.comment_type != None ) and ( self.comment_type != "" ) ):
        
            # we do.  use it.
            comment_type_string = self.comment_type
            
        #-- END check to see if we have comment type.
        
        value_OUT += "                <wp:comment_type>" + comment_type_string + "</wp:comment_type>\n"

        # got a comment parent?
        if ( ( self.parent_comment ) and ( self.parent_comment != None ) ):
        
            # we do.  use it.
            parent_comment_id = self.parent_comment.comment_id
            
        #-- END check to see if we have comment type.
        
        value_OUT += "                <wp:comment_parent>" + str( parent_comment_id ) + "</wp:comment_parent>\n"
 
        # !TODO - comment_user_id other than 0

        value_OUT += "                <wp:comment_user_id>0</wp:comment_user_id>\n"
        value_OUT += "            </wp:comment>\n"

        return value_OUT

    #-- END method to_xml_string --#


    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.author_name + ": " + self.comment_date_time.strftime( "%b %d, %Y" )
        return string_OUT

#= End Comment Model =========================================================