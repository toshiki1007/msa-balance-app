from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^update/', views.update, name='update'),
]