from datetime import datetime, timedelta
from django.shortcuts import render
import json	#para enviar los datos a higcharts
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#importando decorador para login
from django.contrib.auth.decorators import login_required
#importando modelos de donde obtenemos datos
from rango.models import *
#importando formularios
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


#vista de prueba para la hackaton de la nasa

def fuckedView(request):
    return HttpResponse(request.POST.get('datos'))


def alarmas(request):
    """vista para las alarmas, estaran mostradas en tablas"""
    # Diccionario de contexto
    alarmas_list = Alarma.objects.order_by('-fecha')[:7]
    context_dict = {'alarmas': alarmas_list}
    # retorna el template con el contexto
    return render(request, 'rango/alarmas.html', context_dict)

def alarma_med(request, medidor_name_slug):
    """vista para las alarmas, estaran mostradas en tablas"""
    # Diccionario de contexto
    context_dict = {}
    try:
        # buscamos un nombre slug con el nombre dado
        # si no existe sale un error
        #el metodo .get() retorna una instancia modelo
        medidor = Medidor.objects.get(slug=medidor_name_slug)
        context_dict['medidor_name'] = medidor.nombre

        #recuperamos el consumo del ultimo mes
        #last_alarma = Alarma.objects.filter(medidor=medidor)[0]
        # aumente al contexto
        #context_dict['last_alarma'] = last_alarma
        # tambien aumentamos el objeto categoria de la base de datos
        # usaremos esto en la plantilla para verificar
        context_dict['medidor']=medidor
        alarmas_list = Alarma.objects.filter(medidor=medidor).order_by('-fecha')[:7]
        context_dict['alarmas']=alarmas_list
    except Medidor.DoesNotExist:
        #si es que no encontramos la categoria
        pass
    context_dict['medidor_name_slug'] = medidor_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/alarmas.html', context_dict)

#vistas
def index(request):
    """vista indice principal de la aplicacion rango"""
    # Construye un diccionario para pasar al motor de templates
    # Note la llave 'boldmessage' es el mismo del template
    ###########################################################
    #setear una cookie test
    #request.session.set_test_cookie()
    # consultamos la db por una lista de todas las categorias
    #ordenamos categorias por likes en orden descendente
    # mostramos los primeros 5
    # ponemos la lista en el contexto de la plantilla
    #--------------------------------------
    # prueba para los datos del request GET
    #-----------------------------
    consulta = request.GET.get('q', '')
    if consulta:
        formato_fecha = "%Y-%m-%d"
        fecha = datetime.strptime(consulta,formato_fecha)
    else:
        fecha = datetime.today()
    #-------------------------------------------------
    print type(consulta), type(fecha)
    print consulta, fecha
    category_list = Category.objects.order_by('-likes')[:7]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}
    #-------------------------------------------
    # prueba para los datos del ultimo dia
    medidores = Medidor.objects.all()
    context_dict['medidores'] = medidores
    context_dict['fecha']=fecha

    #--------------------------------------------
    visits = int(request.COOKIES.get('visits','1'))
    reset_last_visit_time = False
    response = render(request, 'rango/index.html', context_dict)
    # si existe la cookie de ultima visita
    
    #response = render(request, 'rango/index.html', context_dict)
    return response

#areas para los medidores
def areas_main(request):
    """vista indice principal de la aplicacion de medidor"""
    # Construye un diccionario para pasar al motor de templates
    ###########################################################
    # pasamos los datos de los medidores de las areas y la ultima medida

    medidor_list = Medidor.objects.all()
    medidas_list = Medidas.objects.order_by('id')[:1]
    context_dict = {'categories': medidor_list, 'medidas': medidas_list}
  
    response = render(request, 'rango/index.html', context_dict)
    return response


#pagina de medidor
def medidor(request, medidor_name_slug):
    """vista para cada categoria independiente"""
    #creamos el diccionario de contexto para la plantilla
    context_dict = {}
    try:
        # buscamos un nombre slug con el nombre dado
        # si no existe sale un error
        #el metodo .get() retorna una instancia modelo
        medidor = Medidor.objects.get(slug=medidor_name_slug)
        context_dict['medidor_name'] = medidor.nombre

        #recuperamos la ultima medida del medidor
        last_medida = Medidas.objects.filter(medidor=medidor)[0]

        # aumente al contexto
        context_dict['last_medida'] = last_medida
        # tambien aumentamos el objeto categoria de la base de datos
        # usaremos esto en la plantilla para verificar
        context_dict['medidor']=medidor
    except Medidor.DoesNotExist:
        #si es que no encontramos la categoria
        pass
    context_dict['medidor_name_slug'] = medidor_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/medidor.html', context_dict)

# vista para resumen mensual
def mensual(request, medidor_name_slug):
    """
        vista para crear resumenes mensuales
    """
    #creamos el diccionario de contexto para la plantilla
    context_dict = {}
    try:
        # buscamos un nombre slug con el nombre dado
        # si no existe sale un error
        #el metodo .get() retorna una instancia modelo
        medidor = Medidor.objects.get(slug=medidor_name_slug)
        context_dict['medidor_name'] = medidor.nombre

        #recuperamos el consumo del ultimo mes
        last_medida = Medidas.objects.filter(medidor=medidor)[0]
        # aumente al contexto
        context_dict['last_medida'] = last_medida
        # tambien aumentamos el objeto categoria de la base de datos
        # usaremos esto en la plantilla para verificar
        context_dict['medidor']=medidor
    except Medidor.DoesNotExist:
        #si es que no encontramos la categoria
        pass
    context_dict['medidor_name_slug'] = medidor_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/mensual.html', context_dict)

################################
def diario(request, medidor_name_slug):
    """
        vista para crear resumenes diarios
    """
    #creamos el diccionario de contexto para la plantilla
    context_dict = {}
    try:
        # buscamos un nombre slug con el nombre dado
        # si no existe sale un error
        #el metodo .get() retorna una instancia modelo
        medidor = Medidor.objects.get(slug=medidor_name_slug)
        context_dict['medidor_name'] = medidor.nombre

        #recuperamos el consumo del ultimo mes
        last_medida = Medidas.objects.filter(medidor=medidor)[0]
        # aumente al contexto
        context_dict['last_medida'] = last_medida
        # tambien aumentamos el objeto categoria de la base de datos
        # usaremos esto en la plantilla para verificar
        context_dict['medidor']=medidor
    except Medidor.DoesNotExist:
        #si es que no encontramos la categoria
        pass
    context_dict['medidor_name_slug'] = medidor_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/diario.html', context_dict)

def resumen_mensual(request):
    """
	vista para crear un resumen para las tortas
    """
    context_dict = {}
    #try:
        # buscamos un nombre slug con el nombre dado
        # si no existe sale un error
        #el metodo .get() retorna una instancia modelo
        #medidor = Medidor.objects.get(slug=medidor_name_slug)
        #context_dict['medidor_name'] = medidor.nombre

        #recuperamos el consumo del ultimo mes
        #last_medida = Medidas.objects.filter(medidor=medidor)[0]
        # aumente al contexto
        #context_dict['last_medida'] = last_medida
        # tambien aumentamos el objeto categoria de la base de datos
        # usaremos esto en la plantilla para verificar
        #context_dict['medidor']=medidor
    #except Medidor.DoesNotExist:
        #si es que no encontramos la categoria
        #pass
    #context_dict['medidor_name_slug'] = medidor_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/resumen_mensual1.html', context_dict)

def resumen_diario(request):
    """
        vista para crear un resumen para las tortas
    """
    context_dict = {}
    #try:
        # buscamos un nombre slug con el nombre dado
        # si no existe sale un error
        #el metodo .get() retorna una instancia modelo
        #medidor = Medidor.objects.get(slug=medidor_name_slug)
        #context_dict['medidor_name'] = medidor.nombre

        #recuperamos el consumo del ultimo mes
        #last_medida = Medidas.objects.filter(medidor=medidor)[0]
        # aumente al contexto
        #context_dict['last_medida'] = last_medida
        # tambien aumentamos el objeto categoria de la base de datos
        # usaremos esto en la plantilla para verificar
        #context_dict['medidor']=medidor
    #except Medidor.DoesNotExist:
        #si es que no encontramos la categoria
        #pass
    #context_dict['medidor_name_slug'] = medidor_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/resumen_diario1.html', context_dict)

def resumen_planta(request):
    context_dict = {}
    return render (request, 'rango/resumen_planta.html', context_dict)


############################################################
#######VISTA EJEMPLO######################
################################
#-------------------------

def ult_total(request):
    medidores = Medidor.objects.all()
    datos, datos1 = [], []
    acc = 0
    for med in medidores:
	acc += Medidas.objects.filter(medidor=med)[0].kwh

    series = []
    series.append({'name': "ultima Medida", 'data': acc})

    return HttpResponse(json.dumps(series), content_type='application/json')

def ult_dia(request):
    medidores = Medidor.objects.all()

    datos, datos1 = [], []
    acc = 0
    for med in medidores:
        acc += Medidas.objects.filter(medidor=med)[0].kwh

    series = []
    series.append({'name': "ultima Medida", 'data': acc})

    return HttpResponse(json.dumps(series), content_type='application/json')

#--------------------------
def javamap(request):

    fecha_in = datetime(2012,4,4)
    fecha_fin = fecha_in + timedelta(days=1)
    #if request.is_ajax(): ## probar con highcharts
    medidores = Medidor.objects.all()
    datos = []
    datos1=[]
    #extrae datos entre 2 fechas desde la base de datos
    for med in medidores:
	datos.append(
	    Medidas.objects.filter(
		medidor=med
	    ).exclude(
		fecha__gte=fecha_fin	#fecha fin
	    ).filter(
		fecha__gte=fecha_in  #fecha inicio
	    )
	)
    
    for dato in datos:
	aux=[]
	for med in dato:
	    aux.append(med.kwh)
	datos1.append(aux)
 
    series = []
    for i,j in enumerate(medidores):
        series.append({
            'name':medidores[i].nombre,
            'data':datos1[i]
        })

    return HttpResponse(json.dumps(series), content_type='application/json')
    #raise Http404 

from reports import ChartDia, ChartMes
#----------------------------------------
@login_required 
def chart_dia_json(request):
    data = {}
    #recuperamos parametros del GET request
    dia = request.GET.get('dia', '')
    medidor_slug = request.GET.get('medidor_slug', '')
    
    if dia and not dia == "undefined":
        formato_fecha = "%Y-%m-%d"
        fecha = datetime.strptime(dia,formato_fecha)
        print fecha
    else:
        fecha = datetime.today()

    data= ChartDia.get_day_power(day=fecha, medidor_slug=medidor_slug)
    #data = ChartMes.get_month_power(month=fecha, medidor_slug=medidor_slug)
    return HttpResponse(json.dumps(data), content_type='application/json')
#----------------------------------------------
@login_required 
def chart_mes_json(request):
    data = {}
    #recuperamos parametros del GET request
    mes = request.GET.get('mes', '')
    medidor_slug = request.GET.get('medidor_slug', '')
    
    print "mes: " + mes + ", medidor: " + medidor_slug
    if mes and not mes == "undefined":
        formato_fecha = "%Y-%m"
        fecha = datetime.strptime(mes,formato_fecha)
        print "fecha:" #+ fecha
    else:
        fecha = datetime.today() #- timedelta(days=30)

    #data= ChartDia.get_day_power(day=fecha, medidor_slug=medidor_slug)
    data = ChartMes.get_month_power(month=fecha, medidor_slug=medidor_slug)
    return HttpResponse(json.dumps(data), content_type='application/json')
#--------------------------------------
@login_required
def torta_mes_json(request):
    data = {}
    #recuperamos parametros del GET request
    mes = request.GET.get('mes', '')
    #medidor_slug = request.GET.get('medidor_slug', '')

    print "mes: " + mes
    if mes and not mes == "undefined":
        formato_fecha = "%Y-%m"
        fecha = datetime.strptime(mes,formato_fecha)
        print "fecha:" #+ fecha
    else:
        fecha = datetime.today() #- timedelta(days=30)

    #data= ChartDia.get_day_power(day=fecha, medidor_slug=medidor_slug)
    data = ChartMes.get_month_torta(month=fecha)
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def torta_dia_json(request):
    data = {}
    #recuperamos parametros del GET request
    dia = request.GET.get('dia', '')
    medidor_slug = request.GET.get('medidor_slug', '')

    if dia and not dia == "undefined":
        formato_fecha = "%Y-%m-%d"
        fecha = datetime.strptime(dia,formato_fecha)
        print fecha
    else:
        fecha = datetime.today()

    data= ChartDia.get_day_torta(day=fecha)
    #data = ChartMes.get_month_power(month=fecha, medidor_slug=medidor_slug)
    return HttpResponse(json.dumps(data), content_type='application/json')


def about(request):
    """vista para informacion del desarrollador y la aplicacion"""
    # Diccionario de contexto
    context_dict = {'message': "aplicacion RANGO"}
    # retorna el template con el contexto
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
    """vista para cada categoria independiente"""
    #creamos el diccionario de contexto para la plantilla
    context_dict = {}
    try:
	# buscamos un nombre slug con el nombre dado
	# si no existe sale un error
	#el metodo .get() retorna una instancia modelo
	category = Category.objects.get(slug=category_name_slug)
	context_dict['category_name'] = category.name
	
	# recuperamos paginas asociadas
	# note que el dintro retorna >= 1 instancias modelo
	pages = Page.objects.filter(category=category)
	
	# aumente al contexto
	context_dict['pages'] = pages
	# tambien aumentamos el objeto categoria de la base de datos
	# usaremos esto en la plantilla para verificar
	context_dict['category']=category
    except Category.DoesNotExist:
	#si es que no encontramos la categoria
	pass
    context_dict['category_name_slug'] = category_name_slug
    # renderizamos la respuesta
    return render(request, 'rango/category.html', context_dict)
#vistas de formularios
@login_required
def add_category(request):
    """vista para el formulario de crear categoria"""
    # verifica un request http POST
    if request.method == 'POST':
	form = CategoryForm(request.POST)
	
	#si el formulario es valido
	if form.is_valid():
	    # guarda la nueva categoria en la base de datos
	    form.save(commit=True) #IMPORTANTE!!
	    # una vez guadado llamamos a la vista index
	    # para retornar a la pagina principal
	    return index(request)
	else:
	    # error si es que no es valida
	    print form.errors
    else:
	# si el request no fuera un POST muestro el formulario
	form = CategoryForm()
    #devuelve la plantilla
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    """vista del formulario para crear pagina"""
    try:
	cat = Category.objects.get(slug=category_name_slug)
	print cat
    except Category.DoesNotExist:
	cat = None

    if request.method == 'POST':
	print "mandando..."
	form = PageForm(request.POST)
	if form.is_valid():
	    if cat:
		page = form.save(commit=False)
		page.category = cat
		page.views = 0
		page.save()
		print "pagina salvada"
		# mejor que redireccionar
		return category(request, category_name_slug)
	else:
	    print form.errors
    else:
	form = PageForm()
    context_dict = {'form':form, 'category':cat}

    return render(request, 'rango/add_page.html', context_dict)

# control de usuarios...........................
def register(request):
    """vista para registrar nuevos usuarios"""
    #manejo de cookie
    if request.session.test_cookie_worked():
	print ">>>> TEST COOKIE WORKED!"
	request.session.delete_test_cookie()
    #un booleano para verificar registro exitoso, falso por defecto
    registered = False
    
    # si es un POST queremos procesar la forma
    if request.method == 'POST':
	# intentamos extraer la informacion del form
	# usarmos userform y userprofileform
	user_form= UserForm(data=request.POST)
	profile_form = UserProfileForm(data=request.POST)
	if user_form.is_valid() and profile_form.is_valid():
	    #guardamos los datos
	    user = user_form.save()
	    
	    #ahora verificamos el password
	    #una vez verificado actualizamos
	    user.set_password(user.password)
	    user.save()
	    
	   # instanciamos userprofile
	    # necesitamos setear nosotros
	    #esto retrasa salvar el model hasta que estemos listos
	    profile = profile_form.save(commit=False)
	    profile.user = user
	    
	    #verificamos si hay imagenes
	    if 'picture' in request.FILES:
		profile.picture= request.FILES['picture']
	    
	    # guardamos la instancia
	    profile.save()
	    #actualizamos la variable
	    registered = True

	# para formularios invalidos
	# imprimimos problemas

	else:
	    print user_form.errors, profile_form.errors

    #si no es un POST dibujamos los formularios
    # formularios en blanco
    else:
	user_form = UserForm()
	profile_form = UserProfileForm()

    #renderizamos el template
    return render(request,
	    'rango/register.html',
	    {'user_form':user_form, 'profile_form': profile_form, 'registered': registered})

#para logear
def user_login(request):
    """vista para ingresar con un usuario"""
    #si es un POST
    if request.method=='POST':
	#estraer los datos
	#esta informacion se obtiene del form login
		# esamos request.POST.get('<variable>')
	username = request.POST.get('username')
	password = request.POST.get('password')

	#usa herramientas de django para ver si el usuario exxiste
	user = authenticate(username=username, password=password)
	# si tenemos un usuario
	if user:
	    if user.is_active:
		#si la cuenta es valida y activa mandamos a la pagina inicial
		login(request,user)
		return HttpResponseRedirect('/rango/')
	    else:
		#una cuenta inactiva
		return HttpResponse("su cuenta esta inhabilitada")
	else:
	    # datos incorrectos
	    print "invalid login details: {0}, {1}".format(username,password)
	    return HttpResponse("datos incorrectos!")
	    
    #si no es un POST mostrar el formulario
    else:
	#no hay varialbes que mostrar en la pagina"
	return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    """funcion para cerrar la sesion actual"""
    #como el usuario esta activo simplemente salimos
    logout(request)
    #volver al inicio
    return HttpResponseRedirect('/rango/')

