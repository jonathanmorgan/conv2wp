# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Batch'
        db.create_table(u'conv2wp_batch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('create_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_export_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Batch'])

        # Adding model 'Author'
        db.create_table(u'conv2wp_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('original_user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('create_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_export_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Author'])

        # Adding model 'Category'
        db.create_table(u'conv2wp_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_id', self.gf('django.db.models.fields.IntegerField')()),
            ('nice_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Category'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Category'])

        # Adding model 'Tag'
        db.create_table(u'conv2wp_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Tag'])

        # Adding model 'Term'
        db.create_table(u'conv2wp_term', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('term_taxonomy', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Term'])

        # Adding model 'Channel'
        db.create_table(u'conv2wp_channel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Batch'])),
            ('create_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_export_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pubdate', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pub_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('generator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wxr_version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('base_site_URL', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('base_blog_URL', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('cloud_domain', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cloud_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cloud_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cloud_register_procedure', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cloud_protocol', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('blog_image_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('blog_image_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('blog_image_link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('atom_open_search_rel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('atom_open_search_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('atom_open_search_href', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('atom_open_search_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('atom_blog_hub_rel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('atom_blog_hub_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('atom_blog_hub_href', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('atom_blog_hub_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Channel'])

        # Adding M2M table for field authors on 'Channel'
        db.create_table(u'conv2wp_channel_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm[u'conv2wp.channel'], null=False)),
            ('author', models.ForeignKey(orm[u'conv2wp.author'], null=False))
        ))
        db.create_unique(u'conv2wp_channel_authors', ['channel_id', 'author_id'])

        # Adding M2M table for field categories on 'Channel'
        db.create_table(u'conv2wp_channel_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm[u'conv2wp.channel'], null=False)),
            ('category', models.ForeignKey(orm[u'conv2wp.category'], null=False))
        ))
        db.create_unique(u'conv2wp_channel_categories', ['channel_id', 'category_id'])

        # Adding M2M table for field tags on 'Channel'
        db.create_table(u'conv2wp_channel_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm[u'conv2wp.channel'], null=False)),
            ('tag', models.ForeignKey(orm[u'conv2wp.tag'], null=False))
        ))
        db.create_unique(u'conv2wp_channel_tags', ['channel_id', 'tag_id'])

        # Adding M2M table for field terms on 'Channel'
        db.create_table(u'conv2wp_channel_terms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm[u'conv2wp.channel'], null=False)),
            ('term', models.ForeignKey(orm[u'conv2wp.term'], null=False))
        ))
        db.create_unique(u'conv2wp_channel_terms', ['channel_id', 'term_id'])

        # Adding model 'EmailAddress'
        db.create_table(u'conv2wp_emailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Author'])),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('create_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['EmailAddress'])

        # Adding model 'Item'
        db.create_table(u'conv2wp_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Channel'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('pubdate', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pub_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('guid_is_permalink', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('content_encoded', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('excerpt_encoded', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('post_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('post_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('post_date_time_gmt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('comment_status', self.gf('django.db.models.fields.CharField')(default='closed', max_length=255, blank=True)),
            ('ping_status', self.gf('django.db.models.fields.CharField')(default='closed', max_length=255, blank=True)),
            ('post_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('post_status', self.gf('django.db.models.fields.CharField')(default='publish', max_length=255, null=True, blank=True)),
            ('post_parent', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('menu_order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('post_type', self.gf('django.db.models.fields.CharField')(default='post', max_length=255, null=True, blank=True)),
            ('post_password', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('is_sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attachment_URL', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Item'])

        # Adding M2M table for field creators on 'Item'
        db.create_table(u'conv2wp_item_creators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'conv2wp.item'], null=False)),
            ('author', models.ForeignKey(orm[u'conv2wp.author'], null=False))
        ))
        db.create_unique(u'conv2wp_item_creators', ['item_id', 'author_id'])

        # Adding M2M table for field categories on 'Item'
        db.create_table(u'conv2wp_item_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'conv2wp.item'], null=False)),
            ('category', models.ForeignKey(orm[u'conv2wp.category'], null=False))
        ))
        db.create_unique(u'conv2wp_item_categories', ['item_id', 'category_id'])

        # Adding M2M table for field tags on 'Item'
        db.create_table(u'conv2wp_item_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'conv2wp.item'], null=False)),
            ('tag', models.ForeignKey(orm[u'conv2wp.tag'], null=False))
        ))
        db.create_unique(u'conv2wp_item_tags', ['item_id', 'tag_id'])

        # Adding model 'PostMetaData'
        db.create_table(u'conv2wp_postmetadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Item'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['PostMetaData'])

        # Adding model 'Comment'
        db.create_table(u'conv2wp_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Item'])),
            ('comment_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('author_email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('author_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('author_ip', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comment_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('comment_date_time_gmt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('content_encoded', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment_type', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('parent_comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Comment'], null=True, blank=True)),
            ('comment_author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conv2wp.Author'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'conv2wp', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Batch'
        db.delete_table(u'conv2wp_batch')

        # Deleting model 'Author'
        db.delete_table(u'conv2wp_author')

        # Deleting model 'Category'
        db.delete_table(u'conv2wp_category')

        # Deleting model 'Tag'
        db.delete_table(u'conv2wp_tag')

        # Deleting model 'Term'
        db.delete_table(u'conv2wp_term')

        # Deleting model 'Channel'
        db.delete_table(u'conv2wp_channel')

        # Removing M2M table for field authors on 'Channel'
        db.delete_table('conv2wp_channel_authors')

        # Removing M2M table for field categories on 'Channel'
        db.delete_table('conv2wp_channel_categories')

        # Removing M2M table for field tags on 'Channel'
        db.delete_table('conv2wp_channel_tags')

        # Removing M2M table for field terms on 'Channel'
        db.delete_table('conv2wp_channel_terms')

        # Deleting model 'EmailAddress'
        db.delete_table(u'conv2wp_emailaddress')

        # Deleting model 'Item'
        db.delete_table(u'conv2wp_item')

        # Removing M2M table for field creators on 'Item'
        db.delete_table('conv2wp_item_creators')

        # Removing M2M table for field categories on 'Item'
        db.delete_table('conv2wp_item_categories')

        # Removing M2M table for field tags on 'Item'
        db.delete_table('conv2wp_item_tags')

        # Deleting model 'PostMetaData'
        db.delete_table(u'conv2wp_postmetadata')

        # Deleting model 'Comment'
        db.delete_table(u'conv2wp_comment')


    models = {
        u'conv2wp.author': {
            'Meta': {'object_name': 'Author'},
            'create_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_export_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'original_user_id': ('django.db.models.fields.IntegerField', [], {}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'update_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'conv2wp.batch': {
            'Meta': {'object_name': 'Batch'},
            'create_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_export_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'update_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'conv2wp.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nice_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Category']", 'null': 'True', 'blank': 'True'}),
            'term_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'conv2wp.channel': {
            'Meta': {'object_name': 'Channel'},
            'atom_blog_hub_href': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_blog_hub_rel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_blog_hub_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_blog_hub_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_open_search_href': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_open_search_rel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_open_search_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atom_open_search_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Author']", 'null': 'True', 'blank': 'True'}),
            'base_blog_URL': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'base_site_URL': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Batch']"}),
            'blog_image_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'blog_image_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'blog_image_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Category']", 'null': 'True', 'blank': 'True'}),
            'cloud_domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cloud_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cloud_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cloud_protocol': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cloud_register_procedure': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'create_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'generator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_export_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pub_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pubdate': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Tag']", 'null': 'True', 'blank': 'True'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Term']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wxr_version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'conv2wp.comment': {
            'Meta': {'ordering': "['-comment_date_time']", 'object_name': 'Comment'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comment_author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Author']", 'null': 'True', 'blank': 'True'}),
            'comment_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_date_time_gmt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content_encoded': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Item']"}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Comment']", 'null': 'True', 'blank': 'True'})
        },
        u'conv2wp.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Author']"}),
            'create_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'conv2wp.item': {
            'Meta': {'object_name': 'Item'},
            'attachment_URL': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Category']", 'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Channel']"}),
            'comment_status': ('django.db.models.fields.CharField', [], {'default': "'closed'", 'max_length': '255', 'blank': 'True'}),
            'content_encoded': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Author']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'excerpt_encoded': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'guid_is_permalink': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'menu_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'ping_status': ('django.db.models.fields.CharField', [], {'default': "'closed'", 'max_length': '255', 'blank': 'True'}),
            'post_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'post_date_time_gmt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'post_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'post_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_parent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'post_password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_status': ('django.db.models.fields.CharField', [], {'default': "'publish'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_type': ('django.db.models.fields.CharField', [], {'default': "'post'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pub_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pubdate': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['conv2wp.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'conv2wp.postmetadata': {
            'Meta': {'ordering': "['item']", 'object_name': 'PostMetaData'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conv2wp.Item']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'conv2wp.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'term_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'conv2wp.term': {
            'Meta': {'ordering': "['name']", 'object_name': 'Term'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'term_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'term_taxonomy': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['conv2wp']