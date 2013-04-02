from django.http import HttpResponse,HttpResponseRedirect
from details.models import detail
from django.shortcuts import render,render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.generic.base import TemplateView
from details.forms import *

class Adds(TemplateView):
    template_view='adds.html'
    def get(self,request):
         form=TestForm()
         return render_to_response('adds.html',locals(),context_instance=RequestContext(request))
    def post(self, request):
        form=TestForm(request.POST)
        if form.is_valid():
             student = form.cleaned_data['student_name']
             class_ = form.cleaned_data['student_class']
             main_sub=form.cleaned_data['main_sub']
             Id=form.cleaned_data['student_Id']
             marks=form.cleaned_data['marks']
             Average=form.cleaned_data['Average_marks']
             detail.objects.create(student_name=student,student_class=class_,main_sub=main_sub,student_Id=Id,marks=marks,Average_marks=Average)
             HttpResponseRedirect('/')
        else:
             return HttpResponseRedirect('/errors/')
             #return HttpResponse('Some Problem')
        return HttpResponseRedirect('/')

class Details(TemplateView):
    template_view='details.html'
    def get(self, request):
        s=detail.objects.all()
        return render_to_response('details.html',locals(),context_instance=RequestContext(request))

class Shows(TemplateView):
    template_view='shows.html'
    def get(self,request,id):
        s=detail.objects.get(id=id)
        return render_to_response('shows.html',locals(),context_instance=RequestContext(request))

class Deletes(TemplateView):
    def get(self,request,id):
        d=detail.objects.get(id=id)
        d.delete()
        return render(request,'details.html')
class Errors(TemplateView):
    def get(self,request):
        return render(request,'errors.html')
