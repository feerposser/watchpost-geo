from django.contrib import admin

from .models import ModelBlackList


class AdminBlackList(admin.ModelAdmin):
    list_display = ('bairro', 'cidade', 'status', 'criacao')
    list_filter = ('cidade', 'status', 'usuario')
    search_fields = ['bairro', 'cidade', 'usuario']


# Register your models here.
admin.site.register(ModelBlackList, AdminBlackList)
