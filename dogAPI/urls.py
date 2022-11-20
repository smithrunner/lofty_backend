from django.urls import include, re_path
from dogAPI import views

urlpatterns = [
    re_path(r'^api/keys$', views.key_list),
    re_path(r'^api/keys/(?P<pk>[a-zA-Z0-9]+)$', views.key_detail),
    re_path(r'^api/dogs$', views.dog_grab),
    re_path(r'^api/dogs/(?P<pk>[0-9]+)$', views.dog_display)
]
