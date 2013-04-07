from django.http import HttpResponse

def import_article_HTML( request ):

    '''
    This view renders a form that lets a user specify a directory where HTML
    lives and a few regular expressions that allow the program to isolate common
    elements of an article.  Once the form is submitted, then a subsequent view
    actually does the import and outputs log messages of the result.
    '''

    return HttpResponse("Hello, world. You're at import_article_HTML.")

#-- END view import_article_HTML() --#