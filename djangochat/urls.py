from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chat import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
      # payement striple
    path('payments/', include('payments.urls')),

    # Home & Index
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),

    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),

    # Profil utilisateur
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/', views.user_profile, name='profile'),
    path('user_profile/<int:user_id>/', views.users, name='user_profile'),
    path('users/', views.users_list, name='users'),
    

    # Group Chat Rooms
    path('room/<int:room_id>/rename/', views.rename_room, name='rename_room'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),

    # Chat privé
    path('send-message/', views.send_private_message, name='send_private_message'),
    path('get-chat-messages/<int:chat_id>/', views.get_chat_messages, name='get_chat_messages'),
    path('get-new-messages/<int:chat_id>/', views.get_new_messages, name='get_new_messages'),
    path('delete-conversation/<int:user_id>/', views.delete_conversation, name='delete_conversation'),
    path('private-chat/<int:user_id>/', views.private_chat, name='private_chat'),
    path('typing/<int:chat_id>/', views.typing_status, name='typing_status'),

    # Chat général (room.html)
    path('checkview', views.checkview, name='checkview'),
    path('send/', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('<str:room>/', views.room, name='room'),
    # Snippets
    path('snippet/nouveau/', views.create_snippet, name='create'),
    path('snippet/liste/', views.snippet_list, name='list'),
       path('<slug:slug>/ajax-delete/', views.ajax_delete_snippet, name='ajax_delete'),
    path('snippet/<slug:slug>/', views.snippet_detail, name='detail'),
    path('<slug:slug>/like/', views.like_snippet, name='like'),
    path('snippet/<slug:slug>/ajax-update/', views.ajax_update_snippet, name='ajax_update'),
 
    
    # PWA
    path('', include('pwa.urls')),

    
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', lambda request: redirect('login')),
    

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
  
    