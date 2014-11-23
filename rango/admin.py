from django.contrib import admin

# Register your models here.
from rango.models import Dict 

class DictAdmin(admin.ModelAdmin):
    list_display = ('text', 'translation')
    search_fields = ['text']

admin.site.register(Dict, DictAdmin)
