"""
WSGI config for student project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
'''
Created on 27-Nov-2012

@author: Dharmendra Verma
'''
from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField
from django.db.models.signals import post_delete
import settings
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=settings.UPLOADED_FILE_LOCATION)


class Application(models.Model):
    user=models.ForeignKey(User)
    name=models.CharField(max_length=30)
    min_price = models.FloatField()
    max_price = models.FloatField()
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    offer = models.BooleanField()
    
    def save(self, *args, **kwargs):
        if int(self.min_price) >= int(self.max_price):
            raise ValueError('Minimum price cant be more than Maximum price')
        elif Application.objects.filter(name__iexact = self.name).exists():
            raise ValueError('Name already exist please try some other name')
        else:
            super(Application, self).save(*args, **kwargs)

class AppMedia(models.Model):
    user=models.ForeignKey(User)
    appid = models.CharField(max_length=30)
    image=models.ImageField(upload_to=settings.MEDIA_UPLOADS+"/images/default", storage=fs)
    icon=models.ImageField(upload_to=settings.MEDIA_UPLOADS+"/images/icon", storage=fs)
    video=models.URLField()
    

class AppStat(models.Model):
    appid=models.CharField(max_length=30, unique=True)
    downloads = models.IntegerField(default=0, blank=True, null=True)
    rating = models.FloatField(default=0, blank=True, null=True)
    revenue = models.FloatField(default=0,blank=True, null=True)
    totaluser_rated = models.IntegerField(default=1, blank=True, null=True)


class AppUser(models.Model):
    appid=models.CharField(max_length=30)
    user=models.ForeignKey(User, unique=True)
    rating = models.IntegerField()
    review =models.TextField(blank=True, null=True)\
    
    
    def save(self, *args, **kwargs):
        if int(self.rating)>10 or int(self.rating)<1:
            raise ValueError('Rating is possible only from 1 to 10')
        else:
            try:
                query  = AppStat.objects.get(appid=self.appid)
                query.totaluser_rated += 1 
                query.rating = (query.rating + int(self.rating))/query.totaluser_rated
                query.save()
            except:
                AppStat.objects.create(appid=self.appid, rating=self.rating)
 
            super(AppUser, self).save(*args, **kwargs)

    
      
class Category(models.Model):
    category=models.CharField(max_length=30)
    description=models.TextField()


class AppCategory(models.Model):
    appid=models.CharField(max_length=30)
    category_id=models.CharField(max_length=30)
    
class DefaultCombo(models.Model):
    name=models.CharField(max_length=30)
    applist=ListField(default=[])
    image=models.ImageField(upload_to=settings.MEDIA_UPLOADS+"/images/combo", storage=fs)
    description=models.TextField()
    min_price=models.FloatField()
    max_price=models.FloatField()
                                
class ComboStats(models.Model):
    combo_id=models.CharField(max_length=30)
    downloads=models.IntegerField(default=0)
    revenue=models.FloatField(default=0)

    
def delete(sender, **kwargs):
    deleter = kwargs.get('instance')
    deleter.image.storage.delete(deleter.image.path)
    deleter.icon.storage.delete(deleter.icon.path)
    
def deleteAppExt(sender, **kwargs):
    deleter = kwargs.get('instance')
    AppMedia.objects.filter(appid=deleter.id).delete()
    AppUser.objects.filter(appid=deleter.id).delete()
    query = ComboStats.objects.all()
    for que in query:
        if deleter.id in que.applist:
            que.applist = (que.applist)[0:(que.applist).index(deleter.id)]+(que.applist)[(que.applist).index(deleter.id)+1:]
            que.save()

def deleteComboEx(sender, **kwargs):
    deleter = kwargs.get('instance')
    deleter.image.storage.delete(deleter.image.path)
    ComboStats.objects.filter(combo_id=deleter.id).delete()

def deleteCatEx(sender, **kwargs):
    deleter = kwargs.get('instance')
    AppCategory.objects.filter(category_id=deleter.id).delete()
    
post_delete.connect(delete, AppMedia)
post_delete.connect(deleteAppExt, Application)
post_delete.connect(deleteComboEx, DefaultCombo)
post_delete.connect(deleteCatEx, Category)








