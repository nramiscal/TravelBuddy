from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^my_page$', views.my_page),
    url(r'^show/(?P<trip_id>\d+)$', views.show),
    url(r'^add$', views.add),
    url(r'^createTrip$', views.createTrip),
    url(r'^join/(?P<trip_id>\d+)/(?P<user_id>\d+)$', views.join)

]
