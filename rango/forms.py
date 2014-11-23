from django import forms
from rango.models import Dict 

class DictForm(forms.ModelForm):
    text = forms.CharField(max_length=1024, help_text="Text")
    translation = forms.CharField(max_length=1024, help_text="Translation")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Dict
        fields = ('text',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
