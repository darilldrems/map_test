from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^api/add_click_data$', views.add_click_location_to_store),
    url(r'^api/reset_data$', views.reset_data)
]