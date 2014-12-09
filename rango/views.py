from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Dict 
from rango.forms import DictForm
from django.template.defaulttags import register
import re

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm(request.POST)

        if form.is_valid():
            form.save(commit = True)
            return index(request)

        else:
            print form.errors

    else:
        form = DictForm()
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)

def translate_item(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm()
    # GET
    else:
        # Get user request.
        req = request.GET.copy()
        form = DictForm(req)
#        response_form = DictForm(initial = {'text': 'txt', 'translation': 'trans' })

        # Has 'translate' button been clicked?
        if 'translate' in req:
            # Get text from user input and strip leading/trailing whitespaces.
            txt_in = form.data['text'].strip()
#            txt = form.striped_text
            # Is it a blank input?
            if txt_in:
                # Input text is not in Roman character and provided 'text' already in dictionary text field. Encode to utf-8 to make Chinese char show in Chinese.
                if txt_in.encode('utf8').isalpha() == False and Dict.objects.filter(text = txt_in).exists() == True:
                    txt_out = Dict.objects.get(text = txt_in).translation
                    form.fields['text'].value = txt_in
                    form.data['translation'] = txt_out 
#                    print form.is_valid() # Why is form not valid here???
                    template = 'rango/index.html'
                # Input text is in Roman character and provided 'text' already in dictionary translation field. is_alpha() cannot tell '/' or ',', so use regex instead here.
                elif re.match(r'[a-zA-Z]', txt_in.encode('utf8')) and Dict.objects.filter(translation = txt_in).exists() == True:
                    txt_out = Dict.objects.get(translation = txt_in).text
                    form.fields['text'].value = txt_in
                    form.data['translation'] = txt_out
                    template = 'rango/index.html'
                # Text not in dic, add it into dic.
                else: 
                    form.data['text'] = txt_in
                    template = 'rango/add_item.html'

                return render_to_response(template, {'form': form}, context)
            # A blank input, show form.
            else:
                form = DictForm()

        else:
            # Not a translate req, display the form to enter details.
            form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)


def add_item(request, input_text):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = DictForm(request.POST.copy())
        form.data['text'] = input_text
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

def modify_item(request, input_text):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        req = request.POST
        form = DictForm(req)
        trans = input_text
        if Dict.objects.filter(translation = trans).exists() == True:
            txt = Dict.objects.get(translation = trans).text
 
        # Has 'modify' button been clicked?
        if 'modify' in req:
            print 'OK'
            response_form = DictForm()
            print txt, trans
            # Is it a blank input?
            if txt and trans: 
                response_form.data['text'] = txt
                response_form.data['translation'] = trans 
                template = 'rango/modify_item.html'
                return render_to_response(template, {'form': response_form}, context)
            # A blank input, show form.
            else:
                form = DictForm()
        elif 'submit' in req:
            final_form = DictForm(req.copy())
            print final_form.data['translation']
            print form.is_valid()
            if input_text:
                final_form.data['text'] = input_text 
                print final_form.data['text']
                print final_form.data['translation']
                # Delete original.
                Dict.objects.filter(text = input_text).delete()
                # Save new.
                final_form.save(commit=True)
                # Return home
                return HttpResponseRedirect('/rango/')

        else:
            # Not a translate req, display the form to enter details.
            form = DictForm()

    else:
        # If the request was not a POST, display the form to enter details.
        form = DictForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/index.html', {'form': form}, context)

