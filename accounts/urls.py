from django.urls import path
from .views import ProfileEditView,ProfileView,AddFollower,RemoveFollower


urlpatterns=[
	path('account/{<int:pk>}/',ProfileView.as_view(),name='profile'),
	path('edit/<int:pk>/{{request.user}}/',ProfileEditView.as_view(),name='edit'),
	path('profile/<int:pk>/add/',AddFollower.as_view(),name='follow'),
	path('profile/<int:pk>/remove/',RemoveFollower.as_view(),name='unfollow'),
]