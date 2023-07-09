from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import *
class Category(models.Model):
    cid=int
    catname=models.CharField(max_length=500)

class Questions(models.Model):
    qid=int
    Question=models.TextField()
    Catid=models.ForeignKey("Category",on_delete=models.CASCADE)
class Options(models.Model):
    qid=models.ForeignKey("Questions", on_delete=models.CASCADE)
    oid=int
    option=models.CharField(max_length=1024)
class correctopt(models.Model):
    qaid=int
    qid=models.ForeignKey("Questions", on_delete=models.CASCADE)
    oid=models.ForeignKey("Options", on_delete=models.CASCADE)
class useropt(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    qcat=models.ForeignKey("Category",on_delete=models.CASCADE)
    uqid=models.ForeignKey("Questions",on_delete=models.CASCADE)
    uoid=models.ForeignKey("Options",on_delete=models.CASCADE)
class testtaken(models.Model):
    tuid=models.ForeignKey(User,on_delete=models.CASCADE)
    tcat=models.ForeignKey("Category",on_delete=models.CASCADE)
    tper=models.FloatField()
    tdate=models.DateField(auto_now_add=True)

    
