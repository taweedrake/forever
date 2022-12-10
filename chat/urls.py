from django.urls import path
from .views import CreateThread,ListThreads,ThreadView,Message,DM

urlpatterns=[
    path('inbox/',ListThreads.as_view(),name='inbox'),
    path('inbox/create/',CreateThread.as_view(),name='create-thread'),
    path('inbox/<int:pk>/',ThreadView.as_view(),name='thread'),
    path('inbox/<int:pk>/send/message/',Message.as_view(),name='text'),
    path('inbox/dm/<str:name>/',DM.as_view(),name='create'),

]