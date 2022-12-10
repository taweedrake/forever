from django.urls import path
from .views import Index_view,UserSearch,FollowNotificationView,DMNotificationView

urlpatterns=[
	path('',Index_view,name='home'),
	path('search/', UserSearch.as_view(), name='search'),
	path('notification/<int:not_pk>/follow/<int:profile_pk>/',FollowNotificationView.as_view(),name='follownot'),
	path('notification/<int:not_pk>/dm/<int:object_pk>/',DMNotificationView.as_view(),name='dmnot')
]