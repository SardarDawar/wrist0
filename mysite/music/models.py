from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model



class profileModel(models.Model):
    user                        =   models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    contactNumber               =   models.IntegerField(blank = True, null=True)
    city                        =   models.CharField(max_length=100)
    county                      =   models.CharField(max_length=100)
    state                       =   models.CharField(max_length=100)
    country                     =   models.CharField(max_length=100)
    continent                   =   models.CharField(max_length=100)
   
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

# class wrist_band(models.Model):

#     wrist_band_id                =  models.CharField(max_length=15)
#     created                      =  models.DateTimeField(auto_now=True)
#     updated                      =  models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.wrist_band_id 



class  Information(models.Model):
    user                          =  models.ForeignKey(User,on_delete=models.CASCADE)
    wrist_band_id                 =  models.CharField(max_length=100)
    first_name_child              =   models.CharField(max_length=100)
    last_name_child               =   models.CharField(max_length=100)
    picture_child                 =   models.ImageField(blank=True)
    important_information_child   =   models.CharField(max_length=100)
    first_name_soc                =   models.CharField(max_length=100)
    last_name_soc                 =   models.CharField(max_length=100)
    relation_to_child             =   models.CharField(max_length=100)
    phone_number_soc              =   models.BigIntegerField()
    created                       =  models.DateTimeField(auto_now=True)
    updated                       =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name_child
