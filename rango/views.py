from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm

def category(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html', context_dict, context)
'''    
def pages(request, page_name_url):
    context = RequestContext(request)
    page_name = page_name_url.replace('_', ' ')
    context_dict = {'page_name': page_name}
    try:
        pages = Page.objects.get(title=page_name)
        context_dict['pages'] = pages
    except Page.DoesNotExist:
        pass
    return render_to_response('rango/page.html', context_dict, context)
'''
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dicts = {'categories': category_list, 'pages': page_list}

    for category in category_list:
        category.url = category.name.replace(' ', '_')

    #for page in page_list:
        #page.url_title = page.title.replace(' ', '_')

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dicts, context)

def about(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am bold font in the about page"}
    return render_to_response('rango/about.html', context_dict, context)
#    return HttpResponse("This is about page. <a href='/rango/index'>Index</a>")


def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/add_category.html', {'form': form}, context)

