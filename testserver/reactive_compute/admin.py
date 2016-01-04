from django.contrib import admin
from reactive_compute.models import *


class DependencyAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child', 'argno')
    list_filter = ['parent', 'child']
    search_fields = ['parent', 'child']

admin.site.register(Dependency, DependencyAdmin)


class FunctionTypeAdmin(admin.ModelAdmin):
    list_display = ('node', 'functionname', 'noofargs')
    list_filter = ['functionname']
    search_fields = ['node', 'functionname']

admin.site.register(FunctionType, FunctionTypeAdmin)


class DataLogAdmin(admin.ModelAdmin):
    list_display = ('node', 'timestamp', 'value')
    list_filter = ['node', 'timestamp']
    search_fields = ['node']

admin.site.register(DataLog, DataLogAdmin)
