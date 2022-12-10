from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class BlogPost(models.Model):
    ED='Education'
    SP='Sports'
    LS='Lifestyle'
    UN='Uncategorized'
    CATEGORIES=[
        (ED,'Education'),
        (SP,'Sports'),
        (LS,'Lifestyle'),
        (UN,'Uncategorized')

    ]
    title=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    image=models.ImageField(upload_to='posts',blank=True,null=True)
    category=models.CharField(max_length=13,choices=CATEGORIES,default=UN)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=(str(self.id),(self.title)))


