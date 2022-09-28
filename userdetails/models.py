from email.mime import audio
from django.db import models
from django.db import models
from django.contrib.auth.models import User


class DatedModel(models.Model):

     class Meta:
         abstract = True
 
     date_added = models.DateTimeField(auto_now_add=True,null=True)
     date_modified = models.DateTimeField(auto_now=True,null=True) 
 
class CreatedModel(models.Model):

     """
     Models that inherit this model should explicitly write functionality to
     update the created and modified since you do not have access to the
     request context inside models
     """
 
     class Meta:
         abstract = True
 
     created_by = models.ForeignKey(
         User,null=True, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_created")
     modified_by = models.ForeignKey(
         User, on_delete=models.SET_NULL, blank=True, null=True,
         related_name="%(app_label)s_%(class)s_modified")
# Create your models here.
class UserDetails(User,DatedModel,CreatedModel):
    
      name = models.CharField(max_length=266,null=True)
      phone_number = models.CharField(max_length=20, blank=True, null=True)

class language(DatedModel,CreatedModel):
 
      is_active = models.BooleanField(null=True)
      name = models.CharField(max_length=255,null=True)
      code = models.CharField(max_length=255,null=True)      

class content(DatedModel,CreatedModel):

      language = models.ForeignKey(language,on_delete=models.CASCADE,default=None,null=True)
      video = models.FileField(upload_to="video/",max_length=255,null=True)
      audio = models.FileField(upload_to="audio/" ,max_length=250,null=True)     
      text_content = models.TextField(null=True)
      title = models.CharField(max_length=255,null=True)
      speciality = models.CharField(max_length=255,null=True)