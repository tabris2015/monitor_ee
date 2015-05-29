from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),		#mapeo de la pagina principal
	url(r'^about/', views.about, name= 'about'),	#mapeo de la pagina "acerca de"
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name = 'category'),		#mapeo de las paginas categoria
	url(r'^add_category/$', views.add_category, name = 'add_category'), 	#mapeo del formulario para aumentar categoria
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name = 'add_page'), 
	url(r'^register/$', views.register, name='register'), #mapeo para la pagina de registro de usuarios
	url(r'^login/$', views.user_login, name='login'),	#mapeo para el login
	url(r'^restricted/', views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout'), #cerrar sesion
        url(r'^javamap/$', views.javamap, name='javamap'),
    #url(r'^ult_semana/$', views.resumen_semanal, name='ult_semana'),
	url(r'^ult_dia/$', views.ult_dia, name='ult_dia'),	
	#----------------------reportes parametrizados-----------------#
        url(r'^chart_dia_json/$', views.chart_dia_json, name = 'chart_dia_json'),
        url(r'^chart_mes_json/$', views.chart_mes_json, name = 'chart_mes_json'),
	url(r'^torta_dia_json/$', views.torta_dia_json, name = 'torta_dia_json'),
        url(r'^torta_mes_json/$', views.torta_mes_json, name = 'torta_mes_json'),

    #url(r'^chart_dia_json/$', views.chart_dia_json, name = 'chart_dia_json'),
	url(r'^fuck/$', views.fuckedView, name = 'fuck'),
	#####################################################3
	url(r'^medidor/(?P<medidor_name_slug>[\w\-]+)/$', views.medidor, name = 'medidor'),
	url(r'^medidor/(?P<medidor_name_slug>[\w\-]+)/mensual/$', views.mensual, name = 'mensual'),
	url(r'^medidor/(?P<medidor_name_slug>[\w\-]+)/diario/$', views.diario, name = 'diario'),  
        #######vistas tortas ################################
	url(r'^mensual/$', views.resumen_mensual, name = 'resumen_mensual'),
        url(r'^diario/$', views.resumen_diario, name = 'resumen_diario'),
        
	######################################################
	url(r'^alarmas/$', views.alarmas, name='alarmas'),
	url(r'^alarmas/(?P<medidor_name_slug>[\w\-]+)/$', views.alarma_med, name = 'alarma_med'),
)


