from django.contrib import admin

from .models import ModelBairro, ModelBairroAuxiliar


class AdminBairro(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'endereco', 'alteracao', 'status')
    list_filter = ('cidade', 'status')
    search_fields = ['nome', 'status']


class AdminBairroAuxiliar(admin.ModelAdmin):
    list_display = ('nome', 'cidade')
    list_filter = ('cidade',)
    search_fields = ['nome',]


admin.site.register(ModelBairro, AdminBairro)
admin.site.register(ModelBairroAuxiliar, AdminBairroAuxiliar)