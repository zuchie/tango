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
        req = request.GET
        form = DictForm(req)
        response_form = DictForm(request.GET.copy())
#        response_form = DictForm(initial = {'text': 'txt', 'translation': 'trans' })

        # Has 'translate' button been clicked?
        if 'translate' in req:
            # Get text from user input and strip leading/trailing whitespaces.
            input_text = form.data['text'].strip()
#            txt = form.striped_text
            # Is it a blank input?
            if input_text:
                # First letter(in case delimiters in string) of input text is not in Roman character and provided 'text' already in dictionary text field. Encode to utf-8 to make Chinese char show in Chinese.
                if input_text.encode('utf8')[0].isalpha() == False:
                    if Dict.objects.filter(text__regex = r'^%s$|\/%s\/|^%s\/|\/%s$' %(input_text, input_text, input_text, input_text)).exists() == True:
                        output_text = Dict.objects.get(text__regex = r'^%s$|\/%s\/|^%s\/|\/%s$' %(input_text, input_text, input_text, input_text)).translation
                        response_form.fields['text'].value = input_text 
                        response_form.data['translation'] = output_text 
#                        print form.is_valid() # Why is form not valid here???
                        template = 'rango/index.html'
                        return render_to_response(template, {'form': form, 'response_form': response_form}, context)
                    else:
                       # Add item into 'text' column. 
                        response_form.data['text'] = input_text 
                        response_form.data['translation'] = None 
                        template = 'rango/add_item.html'
                        return render_to_response(template, {'form': response_form}, context)
                # Input text is in Roman character and provided 'text' already in dictionary translation field. is_alpha() cannot tell '/' or ',', so use regex instead here.
                elif re.match(r'[a-zA-Z]', input_text.encode('utf8')):
                    # Search single word, or in the beginning/middle/end of entry column.
                    if Dict.objects.filter(translation__regex = r'^%s$|\/%s\/|^%s\/|\/%s$' %(input_text, input_text, input_text, input_text)).exists() == True:
                        dics = Dict.objects.filter(translation__regex = r'^%s$|\/%s\/|^%s\/|\/%s$' %(input_text, input_text, input_text, input_text))
                        print dics.count()
                        for dic in dics:
                            print dic.text, dic.translation
                        output_text = Dict.objects.get(translation__regex = r'^%s$|\/%s\/|^%s\/|\/%s$' %(input_text, input_text, input_text, input_text)).text
                        response_form.data['translation'] = output_text 
                        response_form.data['text'] = input_text 
                        template = 'rango/index.html'
                        return render_to_response(template, {'form': form, 'response_form': response_form}, context)
                    else:
                       # Add item into 'translation' column. 
                        response_form.data['text'] = input_text 
                        response_form.data['translation'] = None 
                        template = 'rango/add_item.html'
                        return render_to_response(template, {'form': response_form}, context)
                # Text not in dic, add it into dic.
                else: 
                    print 'Not a valid input text.'
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
        if input_text.encode('utf8')[0].isalpha():
            form.data['text'] = form.data['translation']
            form.data['translation'] = input_text 
        else:
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
#        if Dict.objects.filter(translation = trans).exists() == True:
        if input_text.encode('utf8')[0].isalpha() == False and Dict.objects.filter(text__regex = r'[\/|\s]+input_text[\/|\s]+').exists() == True: 
            txt = input_text
            trans = Dict.objects.get(text = input_text).translation

        elif re.match(r'[a-zA-Z]', input_text.encode('utf8')) and Dict.objects.filter(translation_contains = input_text).exists() == True: 
            trans = input_text
            txt = Dict.objects.get(translation = input_text).text
        else:
            print 'Not a valid dic entry' 

        # Has 'modify' button been clicked?
        if 'modify' in req:
            response_form = DictForm()
            # Is it a blank input?
            if txt and trans: 
                if input_text.encode('utf8')[0].isalpha(): 
                    response_form.data['text'] = txt
                    response_form.data['translation'] = trans 
                else:
                    response_form.data['text'] = trans 
                    response_form.data['translation'] = txt 
                template = 'rango/modify_item.html'
                return render_to_response(template, {'form': response_form}, context)
            # A blank input, show form.
            else:
                form = DictForm()
        elif 'submit' in req:
            final_form = DictForm(req.copy())
            if txt == input_text:
                final_form.data['text'] = input_text 
                # Delete original.
                Dict.objects.filter(text_contains = input_text).delete()
                # Save new.
                final_form.save(commit=True)
            elif trans == input_text:
                final_form.data['text'] = final_form.data['translation']
                final_form.data['translation'] = input_text 
                # Delete original.
                Dict.objects.filter(translation_contains = input_text).delete()
                # Save new.
                final_form.save(commit=True)
            else:
                print 'error'
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

