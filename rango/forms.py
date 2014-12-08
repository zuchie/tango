from django import forms
from rango.models import Dict 

class DictForm(forms.ModelForm):
    text = forms.CharField(max_length=1024, help_text="")
    translation = forms.CharField(max_length=1024, help_text="")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Dict
        fields = ('text', 'translation') 

    # Return cleaned data.
    def clean_text(self):
        cleaned_data = self.cleaned_data
        text = cleaned_data.get('text')
        # If text has trailing or leading whitespaces, trim them. 
        return text.strip() 
    def clean_translation(self):
        cleaned_data = self.cleaned_data
        translation = cleaned_data.get('translation')
        # If translation has trailing or leading whitespaces, trim them. 
        return translation.strip()
    def striped_text(self):
        return self.data.get('text').strip()
