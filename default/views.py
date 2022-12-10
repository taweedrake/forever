from django.shortcuts import redirect, render
from django.db.models import Q
from django.views import View
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Notification
from chat.models import ThreadModel

# Create your views here.

@login_required(login_url='account_login')
def Index_view(request):
    return render(request,'default/homepage.html')







class UserSearch(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        query=self.request.GET.get('q')
        if len(query)>0:
            profile_list=UserProfile.objects.filter(
                Q(user__username__icontains=query)
            )
            context={
                'accounts':profile_list
            }
            return render(request,'default/search.html',context)
        messages.error(request,('Error... Search Query reported empty!!'))
        return redirect('home')


class FollowNotificationView(View):
    def get(self,request,not_pk, profile_pk,*args,**kwargs):

        notification=Notification.objects.get(pk=not_pk)
        profile=UserProfile.objects.get(pk=profile_pk)

        notification.has_seen=True
        notification.save()

        return redirect('profile',pk=profile_pk)


class DMNotificationView(View):
    def get(self,request,not_pk, object_pk,*args,**kwargs):

        notification=Notification.objects.get(pk=not_pk)
        thread=ThreadModel.objects.get(pk=object_pk)

        notification.has_seen=True
        notification.save()

        return redirect('thread',pk=object_pk)

