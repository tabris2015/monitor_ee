#importamos herencias
from django.db import models
#importamos herramienta para crear urls
from django.template.defaultfilters import slugify
#importamos el model de usuario
from django.contrib.auth.models import User

# MODELOS DE LA APP
# Los modelos son clases de python que interactuan con la base de datos

class Category(models.Model):
    """clase Categoria para las paginas web"""
    #campo name del tipo char
    name = models.CharField(max_length= 128, unique = True) 
    views= models.IntegerField(default = 0)
    likes= models.IntegerField(default = 0)
    # slugify
    slug = models.SlugField()
    
    #funcion para guardar el nombre cambiado con guiones
    def save(self, *args, **kwargs):
	self.slug = slugify(self.name)
	super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
	return self.name

class Page(models.Model):
    """clase Pagina que contiene info sobre la pagina"""
    #campo categoria es una llave externa
    category = models.ForeignKey(Category)
    title = models.CharField(max_length= 128)
    url = models.URLField()
    views = models.IntegerField(default = 0)

    def __unicode__(self):
	return self.title

class Medidor(models.Model):
    """clase que contiene informacion sobre los medidores"""
    # nombre del medidor
    nombre = models.CharField(max_length = 128, unique = True)
    area = models.CharField(max_length = 128, default="planta")
    descripcion = models.TextField(null=True)
    
    # slugify
    slug = models.SlugField(null=True)

    #funcion para guardar el nombre cambiado con guiones
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Medidor, self).save(*args, **kwargs)

    #para que devuelva el nombre del medidor
    def __unicode__(self):
	return self.nombre

class Medidas(models.Model):
    """clase Medidas que contiene las medidas de los medidores"""
    medidor = models.ForeignKey(Medidor)   #medidor al que corresponde
    fecha = models.DateTimeField()	   #fecha y hora de la medida
    kwh = models.IntegerField(default = 0) #medida en KWH
    
    def __unicode__(self):
	return str(self.kwh)

class Alarma(models.Model):
    """
        modelo alarmas que contiene las alarmas del sistema
    """
    BAJO="B"
    ALTO="A"
    ALARMAS_CHOICES=(
        (BAJO,'Nivel muy bajo detectado!'),
        (ALTO,'Nivel muy alto detectado!'),
    )

    medidor = models.ForeignKey(Medidor)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=2,
        choices=ALARMAS_CHOICES, default=ALTO)
    def evento_bajo(self):
        return self.tipo == self.BAJO
    def evento_alto(self):
        return self.tipo == self.ALTO
        

class UserProfile(models.Model):
    """clase para los usuarios de la pagina"""
    # requiere un objeto tipo usuario
    user = models.OneToOneField(User)
    
    # atributos adicionales para incluir
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    # sobreescribimos el metodo para retornar algo
    def __unicode__(self):
	return self.user.username

class Alumno(models.Model):
    nombre = models.CharField(max_length = 100)
    apellido = models.CharField(max_length = 100)
    edad = models.IntegerField(default = 0)

    def __unicode__(self):
	return self.nombre
