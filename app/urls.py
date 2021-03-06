from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('profiles',views.ProfileViewset)
router.register('posts', views.PostViewset)
router.register('comments', views.CommentViewset)
router.register('polls', views.PollViewset)

urlpatterns = [
    path('', include(router.urls)),
]