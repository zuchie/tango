from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Dict 
from rango.forms import DictForm

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm(request.POST)
        final_form = DictForm()

#        print form.__dict__['data']['text']
#        print form.data['text'] # use form.__dict__ to see what info can be access
        # Have we been provided with a valid form?
        if form.data['text']:
            txt = form.data['text']
            # Save the new category to the database.
#            form.save(commit=True)
#            txt = form.cleaned_data['text']
            # Now call the index() view.
            # The user will be shown the homepage.
#            print form.data['translation']
#            print form.data['text'] # use form.__dict__ to see what info can be access
            if Dict.objects.filter(text = txt).exists() == True:
                dic = Dict.objects.get(text = txt)
#            print dic.translation
                final_form.data['text'] = txt 
                final_form.data['translation'] = dic.translation
                return render_to_response('rango/translate.html', {'form': final_form}, context)
            else: # text not in dic, create one
                return render_to_response('rango/add_item.html', {'form': form}, context)
                
#            print final_form.data
#            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)

def add_item(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
#            return index(request)
            return HttpResponseRedirect('/rango')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)


'''
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
'''
'''
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

def add_page(request, category_name_url):
    context = RequestContext(request)

    #category.url = category_name_url
    #category_name = decode_url(category_name_url)
    category_name = category_name_url.replace('_', ' ')
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)
'''
