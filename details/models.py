from django.db import models

# Create your models here.
class detail(models.Model):
    student_name=models.CharField(max_length=20)
    student_class=models.IntegerField(max_length=2)
    main_sub=models.CharField(max_length=10)
    student_Id=models.CharField(max_length=10)
    marks=models.IntegerField(max_length=3)
    Average_marks=models.FloatField(max_length=4)
