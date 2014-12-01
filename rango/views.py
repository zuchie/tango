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
        form = DictForm()
    else:
        form = DictForm(request.GET)
        trans_form = DictForm()

        # Have we been provided with a valid form 'text' field?
#        if form.data['text']:
        if 'translate' in request.GET:
            request.session['_old_get'] = request.GET
            txt = form.data['text']
            # Is it a blank input?
            if txt: 
                # Is provided 'text' already in dictionary?
                if Dict.objects.filter(text = txt).exists() == True:
                    trans = Dict.objects.get(text = txt).translation
                    trans_form.data['text'] = txt
                    trans_form.data['translation'] = trans
                    return render_to_response('rango/index.html', {'form': form, 'trans_form': trans_form}, context)
                # Text not in dic, add it into dic.
                else: 
                    dict_template = 'rango/add_item.html'
                    dict_form = form
                    return render_to_response(dict_template, {'form': dict_form}, context)
            # a blank input
            else:
                form = DictForm()

        elif 'modify' in request.GET:
            old_get = request.session.get('_old_get')
            txt = old_get['text']
            trans = Dict.objects.get(text = txt).translation
            trans_form.data['text'] = txt 
            trans_form.data['translation'] = trans 
            dict_template = 'rango/modify_item.html'
            return render_to_response(dict_template, {'form': trans_form}, context)

        else:
            # The supplied form contained errors - just print them to the terminal.
#            print form.errors
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

    # A HTTP POST?
    if request.method == 'POST':
        # Get text field value from old session.
        old_get = request.session.get('_old_get')
        txt = old_get['text']
        # make request.POST mutable
        mutable_req_POST = request.POST.copy()
        # Get new form from POST.
        form = DictForm(mutable_req_POST)
        # Get new translation value from new form.
        trans = form['translation'].value()
        # Have we been provided with a valid form?
#        if form.is_valid():
        if Dict.objects.filter(text = txt).exists() == True:
            form.data['text'] = txt
            form.data['translation'] = trans
            # Delete original.
            Dict.objects.filter(text = txt).delete()
            # Save new.
            form.save(commit=True)
            # Return home
            return HttpResponseRedirect('/rango/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    # GET 
    elif request.method == 'GET':
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

