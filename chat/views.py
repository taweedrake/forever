from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import ChatForm,MessageForm
from .models import ThreadModel,MessageModel
from accounts.models import UserProfile
from default.models import Notification
# Create your views here.


class ListThreads(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        threads=ThreadModel.objects.filter(Q(user=request.user)| Q(receiver=request.user))
        context={'threads':threads}

        return render(request,'chat/listchat.html',context)


class CreateThread(LoginRequiredMixin,View):
    def get(self,request,*args,**kawrgs):
        form=ChatForm()
        context={'form':form}
        return render(request,'chat/createthread.html',context)
    def post(self,request,*args,**kwargs):
        form=ChatForm(request.POST)
        user=request.user.username
        username=request.POST['username']
        if username==user:
            messages.error(request,'You cant start thread with yourself')
            return redirect('create-thread')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'User doesnt exist')
            return redirect('create-thread')
        account=UserProfile.objects.get(user__username__contains=username)
        if account.allow_chats_public==True:
            try:
                receiver=User.objects.get(username=username)
                if ThreadModel.objects.filter(user=request.user,receiver=receiver).exists(): 
                    thread= ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                    return redirect('thread', pk=thread.pk)
                elif ThreadModel.objects.filter(user=receiver,receiver=request.user).exists():
                    thread= ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                    return redirect('thread', pk=thread.pk)
                if form.is_valid():
                    thread=ThreadModel(user=request.user,receiver=receiver)
                    thread.save()
                    return redirect('thread',pk=thread.pk)
            except Exception as e:
                messages.error(request,'User Doesnt Exist')
                return redirect('create-thread')
        messages.error(request,f'{account.user.username} doesnot allow Public Chats')
        return redirect('create-thread')

class ThreadView(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        form=MessageForm()
        thread=ThreadModel.objects.get(pk=pk)
        message_list=MessageModel.objects.filter(thread__pk__contains=pk)
        context={
            'thread':thread,
            'form':form,
            'message':message_list
        }
        return render(request,'chat/messages.html',context)

class Message(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        form=MessageForm(request.POST,request.FILES)

        thread=ThreadModel.objects.get(pk=pk)
        if thread.receiver==request.user:
            receiver=thread.user
        else:
            receiver=thread.receiver
        body=request.POST.get('message')
        if form.is_valid():
            mess=form.save(commit=False)
            mess.thread=thread
            mess.sender_user=request.user
            mess.receiver_user=receiver
            mess.save()
            notification=Notification.objects.create(notification_type=5,from_user=request.user,to_user=receiver,thread=thread)
            return redirect('thread', pk=pk)

class DM(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        username=kwargs.get('name')
        try:
            receiver=User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user,receiver=receiver).exists(): 
                thread= ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver,receiver=request.user).exists():
                thread= ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            thread=ThreadModel(user=request.user,receiver=receiver)
            thread.save()
            return redirect('thread',pk=thread.pk)
        except Exception as e:
            return redirect('create-thread')

