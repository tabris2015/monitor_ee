# template tag para obtener lista de categorias
from django import template
from rango.models import Category, Medidor

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}


@register.inclusion_tag('rango/side_areas.html')
def get_areas_list(med=None):
	return {'areas': Medidor.objects.all(), 'act_med': med}

@register.inclusion_tag('rango/side_areas_alarma.html')
def get_areas_list_alarma(med=None):
	return {'areas': Medidor.objects.all(), 'act_med': med}


@register.inclusion_tag('rango/side_menu.html')
def get_menu_list(item=None):
	return {'items':[], 'act_item':item}

