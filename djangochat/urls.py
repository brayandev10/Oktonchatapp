from django.contrib import admin
from django.urls import path
from chat import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('checkview', views.checkview, name='checkview'),
    path('send/', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('<str:room>/', views.room, name='room'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)