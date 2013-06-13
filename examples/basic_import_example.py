# import the basic importer package.
import conv2wp.basic.basic_importer

# make a test instance
database_password = ""
importer = conv2wp.basic.basic_importer.Basic_Importer.get_testing_instance( database_password )

# import all posts.
batch_slug = "cva_import-001"
import_status = importer.import_blog( batch_slug )

# Output the posts as a WXR file.

# load your batch.
import conv2wp.models
blog_import_batch = conv2wp.models.Batch.objects.get( slug = batch_slug )

# set output file path
output_file_path = "cva.wxr"

# output
output_wxr_status = blog_import_batch.output_WXR_file( output_file_path_IN = output_file_path )