from django.db import models

# Create your models here.

class Batch( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    title = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date_time = models.DateTimeField( auto_now_add = True )
    update_date_time = models.DateTimeField( auto_now = True )
    last_export_date_time = models.DateTimeField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.title + " (" + self.update_date_time.strftime( "%b %d, %Y" ) + ")"
        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Batch --#


# Category model
class Category( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    name = models.CharField( max_length = 255 )
    label = models.CharField( max_length = 255 )
    description = models.TextField( blank = True, null = True )
    parent_category = models.ForeignKey( 'self', blank = True, null = True )
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

#= End Category Model =========================================================


# Tag model
class Tag( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    name = models.CharField( max_length = 255 )
    label = models.CharField( max_length = 255 )
    description = models.TextField( blank = True )
    parent_tag = models.ForeignKey( 'self', blank = True, null = True )
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


# Channel model
class Channel( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    batch = models.ForeignKey( Batch )
    title = models.CharField( max_length = 255, blank = True, null = True )
    link = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    pub_date_time = models.DateTimeField( blank = True, null = True )
    generator = models.CharField( max_length = 255, blank = True, null = True )
    WXR_version = models.CharField( max_length = 255, blank = True, null = True )
    base_URL = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    site_URL = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    create_date_time = models.DateTimeField( auto_now_add = True )
    last_export_date_time = models.DateTimeField( blank = True, null = True )
    categories = models.ManyToManyField( Category, blank = True, null = True )
    tags = models.ManyToManyField( Tag, blank = True, null = True )

    # - cloud? - example <cloud domain='capitalnewsservice.wordpress.com' port='80' path='/?rsscloud=notify' registerProcedure='' protocol='http-post' />
    cloud_domain = models.CharField( max_length = 255, blank = True, null = True )
    cloud_port = models.IntegerField( blank = True, null = True )
    cloud_path = models.CharField( max_length = 255, blank = True, null = True )
    cloud_register_procedure = models.CharField( max_length = 255, blank = True, null = True )
    cloud_protocol = models.CharField( max_length = 255, blank = True, null = True )
    blog_image_url = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    blog_image_title = models.CharField( max_length = 255, blank = True, null = True )
    blog_image_link = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )

    # - blog open search atom link: <atom:link rel="search" type="application/opensearchdescription+xml" href="http://capitalnewsservice.wordpress.com/osd.xml" title="Capital News Service" />
    atom_open_search_rel = models.CharField( max_length = 255, blank = True, null = True )
    atom_open_search_type = models.CharField( max_length = 255, blank = True, null = True )
    atom_open_search_href = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    atom_open_search_title = models.CharField( max_length = 255, blank = True, null = True )

    # - blog hub atom link: <atom:link rel='hub' href='http://capitalnewsservice.wordpress.com/?pushpress=hub'/>
    atom_blog_hub_rel = models.CharField( max_length = 255, blank = True, null = True )
    atom_blog_hub_type = models.CharField( max_length = 255, blank = True, null = True )
    atom_blog_hub_href = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    atom_blog_hub_title = models.CharField( max_length = 255, blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.title + " (" + self.pub_date_time.strftime( "%b %d, %Y" ) + ")"
        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Channel --#


# Creator model
class Creator( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    first_name = models.CharField( max_length = 255, blank = True, null = True )
    middle_name = models.CharField( max_length = 255, blank = True, null = True )
    last_name = models.CharField( max_length = 255, blank = True, null = True )
    suffix = models.CharField( max_length = 255, blank = True, null = True )
    username = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    create_date_time = models.DateTimeField( auto_now_add = True )
    update_date_time = models.DateTimeField( auto_now = True )
    last_export_date_time = models.DateTimeField( blank = True, null = True )

    create_date_time = models.DateTimeField( auto_now_add = True )
    update_date_time = models.DateTimeField( auto_now = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


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


#-- END model class Creator --#


class EmailAddress( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    creator = models.ForeignKey( Creator )
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


# Item model
class Item( models.Model ):

    '''
    Item based on Wordpress eXtended RSS file spec (WXR).  Sample document at:
    http://google-blog-converters-appengine.googlecode.com/svn/trunk/samples/wordpress-sample.wxr
    '''

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


    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    channel = models.ForeignKey( Channel )
    title = models.CharField( max_length = 255, blank = True, null = True )
    link = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    pub_date_time = models.DateTimeField( blank = True, null = True )
    creators = models.ManyToManyField( Creator, blank = True, null = True )
    guid = models.CharField( max_length = 255, blank = True, null = True )
    guid_is_permalink = models.BooleanField( 'Is permalink?', default = False )
    description = models.TextField( blank = True, null = True )
    content_encoded = models.TextField( blank = True, null = True )
    excerpt = models.TextField( blank = True, null = True )
    post_id = models.IntegerField( blank = True, null = True )
    post_date_time = models.DateTimeField( blank = True, null = True )
    post_date_time_gmt = models.DateTimeField( blank = True, null = True )
    comment_status = models.CharField( max_length = 255, choices = INTERACTION_STATUSES, blank = True, default = INTERACTION_STATUS_CLOSED )
    ping_status = models.CharField( max_length = 255, choices = INTERACTION_STATUSES, blank = True, default = INTERACTION_STATUS_CLOSED )
    post_name = models.CharField( max_length = 255, blank = True, null = True )
    post_status = models.CharField( max_length = 255, blank = True, null = True, default = POST_STATUS_PUBLISH )
    post_parent = models.IntegerField( blank = True, null = True, default = 0 )
    menu_order = models.IntegerField( blank = True, null = True, default = 0 )
    item_type = models.CharField( max_length = 255, blank = True, null = True, default = ITEM_TYPE_POST )
    post_password = models.CharField( max_length = 255, blank = True, null = True )
    is_sticky = models.BooleanField( default = False )
    attachment_URL = models.URLField( max_length = 255, verify_exists = False, blank = True, null = True )
    categories = models.ManyToManyField( Category, blank = True, null = True )
    tags = models.ManyToManyField( Tag, blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __unicode__( self ):

        string_OUT = str( self.id ) + " - " + self.title + " (" + self.pub_date_time.strftime( "%b %d, %Y" ) + ")"
        return string_OUT

    #-- END method __unicode__() --#


#-- END model class Item --#


# PostMetaData model
class PostMetaData( models.Model ):

    #----------------------------------------------------------------------
    # instance members
    #----------------------------------------------------------------------

    item = models.ForeignKey( Item )
    name = models.CharField( max_length = 255 )
    value = models.TextField( blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    last_modified = models.DateField( auto_now = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.name + ": " + self.value
        return string_OUT

#= End PostMetaData Model =========================================================