from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View
from .models import UserProfile
from chat.models import ThreadModel
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from default.models import Notification



class ProfileView(LoginRequiredMixin,View):
    def get(self,request, pk,*args,**kwargs):
        profile=UserProfile.objects.get(pk=pk)
        user=profile.user
        threads=ThreadModel.objects.filter(Q(user=request.user)| Q(receiver=request.user))
        followers=profile.followers.all()
        if len(followers)==0:
            is_following=False
        for follower in followers:
            if follower ==request.user:
                is_following=True
                break
            else:
                is_following=False

        number_of_followers=len(followers)

        context={'profile':profile,'user':user,'following':is_following,'followers':number_of_followers,'follows':followers,'threads':threads}
        return render(request,'accounts/profile.html',context)

class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=UserProfile
    fields=['first_name','last_name','gender','country','dob','image','bio','hide_email','allow_chats_private','allow_chats_public']
    template_name='accounts/profile_edit.html'
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('profile',kwargs={'pk':pk})

    def test_func(self):
        profile=self.get_object()
        return self.request.user == profile.user


class AddFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        notification=Notification.objects.create(notification_type=3,from_user=request.user,to_user=profile.user)
        return redirect('profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        notification=Notification.objects.create(notification_type=4,from_user=request.user,to_user=profile.user) 
        return redirect('profile', pk=profile.pk)



class ListFollowers(View):
    def get(self,request,pk,*args,**kwargs):
        profile=UserProfile.objects.get(pk=pk)
        followers=profile.followers.all()
        context={
            'profile':profile,
            'followers':followers
       }
        return render(request,'accounts/.html',context)


