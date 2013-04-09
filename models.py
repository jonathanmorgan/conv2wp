from django.db import models

# Create your models here.

class Batch( models.Model ):

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
    # instance members
    #----------------------------------------------------------------------

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
    post_password = models.CharField( max_length = 255, blank = True, null = True )
    is_sticky = models.BooleanField( default = False )
    attachment_URL = models.URLField( max_length = 255, blank = True, null = True )
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

    COMMENT_STATUS_APPROVED = True
    COMMENT_STATUS_NOT_APPROVED = False

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
    comment_type = models.CharField( max_length = 255, blank = True, null = True )
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

    def __unicode__( self ):
        string_OUT = str( self.id ) + " - " + self.author_name + ": " + self.comment_date_time.strftime( "%b %d, %Y" )
        return string_OUT

#= End Comment Model =========================================================