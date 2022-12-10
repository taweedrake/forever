from django.urls import path
from .views import BlogView,BlogDetailView,AddPostView,PreDeleteView,PostDeleteView

urlpatterns=[
    path('',BlogView.as_view(),name='blog'),
    path('article/<int:pk>/<str:blogname>/',BlogDetailView.as_view(),name='post'),
    path('article/post/',AddPostView.as_view(),name='addpost'),
    path('postmanager/<int:pk>/',PreDeleteView.as_view(),name='predelete'),
    path('<int:pk>/delete/',PostDeleteView.as_view(),name='delete')
]