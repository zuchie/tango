from rango.models import Dict 
from django import template
from rango.forms import DictForm

register = template.Library()

@register.inclusion_tag('dict_trans.html')
def get_dict(key):
    form = DictForm()
    if Dict.objects.filter(text = key).exists():
        form.data['text']= Dict.objects.get(text = key)
        form.data['translation']= Dict.objects.get(text = key).translation
        print form.data
        return {'form': form} 
    else:
        return None

@register.filter(name = 'form_get')
def form_get(form):
    my_form = DictForm()
    my_form = form 
    return my_form

