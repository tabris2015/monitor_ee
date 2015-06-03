from django.contrib import admin
#importamos los modelos para administrar
from rango.models import *

# modelos personalizados 
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
# Register your models here.

class AlarmaAdmin(admin.ModelAdmin):
    list_display = ('medidor', 'tipo', 'fecha')
#REGISTRO DE MODELS PARA LA PAGINA DE ADMIN

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Medidor)
admin.site.register(Medidas)
admin.site.register(UserProfile)
admin.site.register(Alarma, AlarmaAdmin)


