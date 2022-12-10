from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserProfile(models.Model):
	Male='Male'
	Female='Female'
	GENDER_CHOICES=[
		(Male,'Male'),
		(Female,'Female')
	]

	first_name=models.CharField(max_length=200,blank=True,null=True)
	last_name=models.CharField(max_length=200,blank=True,null=True)
	gender=models.CharField(max_length=6,default='Male',choices=GENDER_CHOICES,blank=False,null=False)
	country=models.CharField(max_length=56,blank=True,null=True)
	image=models.ImageField(upload_to='profile_pics',default='default.png',blank=True,verbose_name='Profile Picture')
	dob=models.DateField(null=True,blank=True,verbose_name='Date of Birth',help_text='YEAR-MM-DD')
	user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,verbose_name='user',related_name='profile')
	bio=models.TextField(max_length=200,blank=True,null=True)
	hide_email=models.BooleanField(default=False)
	allow_chats_private=models.BooleanField(default=False,verbose_name='Allow Private Chats',help_text='Allow those who have targeted you to chat with you')
	allow_chats_public=models.BooleanField(default=False,verbose_name='Allow Public Chats',help_text='Allow anyone to chat with you even if you are not Targetting eachother')
	followers=models.ManyToManyField(User,blank=True,related_name='followers')

	def __str__(self):
		return self.user.username



@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()
 