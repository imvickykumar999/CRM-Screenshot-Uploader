from django.urls import path
from . import views

urlpatterns = [
    path('api/upload_screenshot', views.upload_screenshot, name='upload_screenshot'),
    path('api/screenshots', views.list_screenshots, name='list_screenshots'),
    path('', views.render_screenshots_page, name='screenshots_page'),
]
