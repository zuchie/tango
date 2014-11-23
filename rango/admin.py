from django.contrib import admin

# Register your models here.
from rango.models import Category, Page
'''
class PageAdmin(admin.ModelAdmin):
#    list_display = ('title', 'category', 'url')
    list_display = ('title', 'category')
    search_fields = ['title']
'''
admin.site.register(Category)
admin.site.register(Page)
