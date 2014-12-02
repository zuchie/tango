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
    # GET
    else:
        # Make form mutable.
        mutable_req_POST = request.GET.copy()
        form = DictForm(mutable_req_POST)

        # Has 'translate' button been clicked?
        if 'translate' in request.GET:
            # Save mutable request.GET for other views.
            request.session['_old_get'] = mutable_req_POST
            # Get text from user input and strip leading/trailing whitespaces.
            text_input = form.data['text'].strip()
            # Is it a blank input?
            if text_input: 
                # Is provided 'text' already in dictionary?
                if Dict.objects.filter(text = text_input).exists() == True:
                    form.data['translation'] = Dict.objects.get(text = text_input).translation
                    template = 'rango/index.html'
                # Text not in dic, add it into dic.
                else: 
                    form.data['text'] = form.data['text'].strip()
                    template = 'rango/add_item.html'

                return render_to_response(template, {'form': form}, context)
            # A blank input, show form.
            else:
                form = DictForm()

        # Has 'modify' button been clicked?
        elif 'modify' in request.GET:
            # Get text.
            old_get = request.session.get('_old_get')
            text_input = old_get['text'].strip()
            form.data['text'] = text_input 
            form.data['translation'] = Dict.objects.get(text = text_input).translation
            template = 'rango/modify_item.html'
            return render_to_response(template, {'form': form}, context)

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
            form.data['translation'] = trans.strip()
            # Delete original.
            Dict.objects.filter(text = txt).delete()
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

