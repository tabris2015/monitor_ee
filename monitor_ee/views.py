from datetime import datetime, timedelta
from django.shortcuts import render
import json     #para enviar los datos a higcharts
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#importando decorador para login
from django.contrib.auth.decorators import login_required
#importando modelos de donde obtenemos datos
from rango.models import *
#importando formularios
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from reports import ChartDia, ChartMes, Chart

#vista de prueba para la hackaton de la nasa


def index(request):
    """vista para las alarmas, estaran mostradas en tablas"""
    # Diccionario de contexto
    context_dict = {}
    # retorna el template con el contexto
    return render(request, 'home.html', context_dict)

