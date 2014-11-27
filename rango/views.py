from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Dict 
from rango.forms import DictForm
from django.template.defaulttags import register

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm(request.POST)
        trans_form = DictForm()

        # Have we been provided with a valid form 'text' field?
        if form.data['text']:
            txt = form.data['text']
            # Is provided 'text' already in dictionary?
            if Dict.objects.filter(text = txt).exists() == True:
                trans = Dict.objects.get(text = txt).translation
                trans_form.data['text'] = txt
                trans_form.data['translation'] = trans
                return render_to_response('rango/index.html', {'form': form, 'trans_form': trans_form}, context)
#                dict_template = 'rango/translate.html'
#                my_dict = Dict.objects.get(text = txt) 
#                return render_to_response(dict_template, {'dict': my_dict}, context)
            # Text not in dic, add it into dic.
            else: 
                dict_template = 'rango/add_item.html'
                dict_form = form
                return render_to_response(dict_template, {'form': dict_form}, context)
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

def modify_item(request):
    # Get the context from the request.
    context = RequestContext(request)

    print request.GET.__dict__
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
    # POST
    elif request.method == 'POST':
        form = DictForm(request.GET)
        print form.data
        if form.is_valid():
            return render_to_response('rango/modify_item.html', {'form': form}, context)
    else:
        # If the request was not a POST, display the form to enter details.
        form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)

