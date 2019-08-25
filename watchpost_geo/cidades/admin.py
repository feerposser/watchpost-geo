from django.contrib import admin

from .models import ModelCidade


class AdminCidade(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'alteracao')
    list_filter = ('nome',)
    search_fields = ['nome',]


admin.site.register(ModelCidade, AdminCidade)
