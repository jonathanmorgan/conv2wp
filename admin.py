from django.contrib import admin

# Import my models.
from conv2wordpress.conv2wp.models import Batch
from conv2wordpress.conv2wp.models import Category
from conv2wordpress.conv2wp.models import Channel
from conv2wordpress.conv2wp.models import Creator
from conv2wordpress.conv2wp.models import EmailAddress
from conv2wordpress.conv2wp.models import Item
from conv2wordpress.conv2wp.models import PostMetaData
from conv2wordpress.conv2wp.models import Tag


# Register their default admin pages (good enough for now).
admin.site.register( Batch )
admin.site.register( Category )
admin.site.register( Channel )
admin.site.register( Creator )
admin.site.register( EmailAddress )
admin.site.register( Item )
admin.site.register( PostMetaData )
admin.site.register( Tag )
