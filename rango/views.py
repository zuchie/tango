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
        # A new dic form to be used later.
        final_form = DictForm()

        # Have we been provided with a valid form 'text' field?
        if form.data['text']:
            txt = form.data['text']
            # Is provided 'text' already in dictionary?
            if Dict.objects.filter(text = txt).exists() == True:
                dic = Dict.objects.get(text = txt)
                # Pass field data to new dic form, since form is immutable.
                final_form.data['text'] = txt 
                final_form.data['translation'] = dic.translation
                # Render field data to html.
                return render_to_response('rango/translate.html', {'form': final_form}, context)
            # Text not in dic, add it into dic.
            else: 
                return render_to_response('rango/add_item.html', {'form': form}, context)
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

            # The user will be shown the homepage.
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

def translate_modify(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # User clicked 'back' button, goto home.
            if 'back' in form.data:
                return HttpResponseRedirect('/rango/')
            # User clicked 'modify' button, to modify definition
            elif 'modify' in form.data:
                return render_to_response('/rango/modify_item.html', {'form': form}, context)
               
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)


def modify_item(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP GET?
    if request.method == 'GET':
        form = DictForm(request.GET)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Delete original.
            Dict.objects.filter(text = form.data['text']).delete()
            # Save new.
            form.save(commit=True)
            # Return home
            return HttpResponseRedirect('/rango/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)

