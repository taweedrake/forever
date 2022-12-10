from django.db import models
from django.utils import timezone
from chat.models import ThreadModel
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    #3 follow #4 unfollow #5 dm
    notification_type=models.IntegerField()
    to_user=models.ForeignKey(User,related_name='notification_to', on_delete=models.CASCADE,null=True)
    from_user=models.ForeignKey(User,related_name='notification_from', on_delete=models.CASCADE,null=True)
    date=models.DateTimeField(default=timezone.now)
    has_seen=models.BooleanField(default=False)
    thread=models.ForeignKey(ThreadModel,on_delete=models.CASCADE,related_name='+',blank=True,null=True)
