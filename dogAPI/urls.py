from django.urls import include, re_path
from dogAPI import views

urlpatterns = [
    re_path(r'^api/keys$', views.key_list),
    re_path(r'^api/keys/(?P<pk>[0-9]+)$', views.key_detail)
]
