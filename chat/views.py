from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
import re
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
import mimetypes
from django.db.models import Q


def index(request):
    return render(request, 'index.html')
    
@login_required
def user_profile(request):
    return render(request, 'profile.html', {'user': request.user})
    
 
@login_required
def users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    is_admin = user.is_staff or user.is_superuser

    return render(request, "profile_user.html", {
        "user": user,
        "is_admin": is_admin
    })

@login_required
def users_list(request):
    chats = PrivateChat.objects.filter(user1=request.user) | PrivateChat.objects.filter(user2=request.user)

    contacted_users = set()
    for chat in chats:
        if chat.user1 != request.user:
            contacted_users.add(chat.user1)
        if chat.user2 != request.user:
            contacted_users.add(chat.user2)

    # Marque les admins dans contacted_users
    for user in contacted_users:
        user.is_admin = user.is_staff or user.is_superuser

    all_users = User.objects.exclude(id=request.user.id)
    for user in all_users:
        user.is_admin = user.is_staff or user.is_superuser

    return render(request, "users.html", {
        "contacted_users": contacted_users,
        "all_users": all_users,
    })

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = request.user.userprofile
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat = PrivateChat.objects.filter(
        Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user)
    ).first()
    if chat and request.method == "POST":
        # Supprimer les messages liés
        PrivateMessage.objects.filter(chat=chat).delete()
        chat.delete()
    return redirect('users')
    

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Vérification si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà utilisé.')
            return redirect('register')

        # Sécurité du mot de passe
        errors = []
        if len(password) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r'[A-Z]', password):
            errors.append("Le mot de passe doit contenir au moins une lettre majuscule.")
        if not re.search(r'[a-z]', password):
            errors.append("Le mot de passe doit contenir au moins une lettre minuscule.")
        if not re.search(r'\d', password):
            errors.append("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register')

        # Création de l'utilisateur inactif
        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active = False
        user.save()

        # Génération du token et de l'URL de confirmation
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_url = request.build_absolute_uri(
            reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
        )

        # Envoi de l'e-mail
        send_mail(
    'Bienvenue sur CodeZone – Confirme ton adresse email',
    f"""
Salut {username} !

Merci de t'être inscrit sur CodeZone, la plateforme dédiée aux passionnés de code.

Pour activer ton compte et commencer à partager, apprendre et coder avec la communauté, clique simplement sur le lien ci-dessous :

{confirmation_url}

Si tu n’es pas à l’origine de cette inscription, tu peux ignorer ce message.

À très vite sur CodeZone !
L’équipe CodeZone
""",
    'brayantematio1@gmail.com',
    [email],
    fail_silently=False,
)

        messages.success(request, "Inscription réussie ! Vérifiez vos e-mails pour confirmer votre compte.")
        return redirect('login')

    return render(request, 'register.html')
    
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

def confirm_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email confirmé avec succès. Vous pouvez maintenant vous connecter.")
        return redirect('login')
    else:
        messages.error(request, "Le lien de confirmation est invalide ou a expiré.")
        return redirect('register')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('login')

        # Vérifie si l'utilisateur existe
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur inexistant.")
            return redirect('login')

        # Authentifie l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
# Page d'accueil affichant les salles
@login_required
def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {
        'rooms': rooms,
        'user': request.user
    })
    
    
@login_required
def rename_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user != room.created_by:
        return HttpResponseForbidden()

    if request.method == "POST":
        new_name = request.POST.get("new_name")
        if new_name:
            room.name = new_name
            room.save()
    return redirect('home')

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user != room.created_by:
        return HttpResponseForbidden()

    if request.method == "POST":
        room.delete()
    return redirect('home')    
       


@login_required
def room(request, room):
    try:
        room_details = Room.objects.get(name=room)
    except Room.DoesNotExist:
        return HttpResponse("Salle non trouvée", status=404)

    return render(request, 'room.html', {
        'username': request.user.username,
        'room': room,
        'room_details': room_details
    })

@login_required
def checkview(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')

        if not room_name:
            return JsonResponse({'error': 'Nom du groupe requis'}, status=400)

        room, created = Room.objects.get_or_create(
            name=room_name,
            defaults={'created_by': request.user}
        )

        return redirect(f'/{room.name}/')
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)



@login_required
@csrf_exempt
def send(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        room_id = request.POST.get('room_id')
        file = request.FILES.get('file')

        if not room_id:
            return JsonResponse({'error': 'Champs manquants'}, status=400)

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room introuvable'}, status=404)

        Message.objects.create(
            value=message,
            user=request.user,
            room=room,
            file=file
        )

        return JsonResponse({'status': 'Message envoyé'})

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
   
def getMessages(request, room):
    try:
        room_obj = Room.objects.get(name=room)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Salle non trouvée'}, status=404)

    messages = Message.objects.filter(room=room_obj).select_related('user').order_by('date')

    data = []
    for m in messages:
        try:
            profile_picture = m.user.userprofile.profile_picture
            profile_picture_url = request.build_absolute_uri(profile_picture.url) if profile_picture else None
        except UserProfile.DoesNotExist:
            profile_picture_url = None

        data.append({
            'user': m.user.username,
            'is_admin': m.user == room_obj.created_by,
            'user_id': m.user.id,
            'user_profile_picture': profile_picture_url,
            'value': m.value,
            'date': m.date.isoformat(),
            'read': m.read,
            'file_url': request.build_absolute_uri(m.file.url) if m.file else '',
            'file_name': m.file.name.split('/')[-1] if m.file else '',
            'file_size': m.file.size if m.file else 0,
        })

    return JsonResponse({'messages': data})
    
@login_required
def private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    user1, user2 = sorted([request.user, other_user], key=lambda u: u.id)
    chat, created = PrivateChat.objects.get_or_create(user1=user1, user2=user2)

    return render(request, 'chat.html', {
        'chat': chat,
        'other_user': other_user,
    })

@csrf_exempt
def send_private_message(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        content = request.POST.get('content', '')
        file = request.FILES.get('file')
        description = request.POST.get('file_description', '')

        chat = get_object_or_404(PrivateChat, id=chat_id)

        message = PrivateMessage.objects.create(
            chat=chat,
            sender=request.user,
            content=content,
            file=file,
            file_description=description
        )

        return JsonResponse({
            'sender': message.sender.username,
            'content': message.content,
            'file_url': message.file.url if message.file else '',
            'file_type': request.FILES['file'].content_type if 'file' in request.FILES else '',
            'file_description': message.file_description,
            'timestamp': message.timestamp.strftime('%H:%M')
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
def get_new_messages(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    messages = chat.messages.order_by('timestamp')
    data = [
        {
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'is_self': msg.sender == request.user
        }
        for msg in messages
    ]
    return JsonResponse({'messages': data})        



from django.utils.timezone import localtime


@login_required
def get_chat_messages(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    messages = chat.messages.order_by('timestamp')

    # Marquer les messages reçus comme lus
    messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    data = []
    for msg in messages:
        local_ts = localtime(msg.timestamp)
        data.append({
            'sender': msg.sender.username,
            'content': msg.content,
            'file_url': msg.file.url if msg.file else '',
            'file_description': msg.file_description,
            'file_type': mimetypes.guess_type(msg.file.url)[0] if msg.file else '',
            'timestamp': local_ts.strftime('%H:%M'),
            'full_date': local_ts.strftime('%Y-%m-%d'),
            'is_self': msg.sender == request.user,
            'is_read': msg.is_read
        })

    # Calcul de l’état de frappe
    typing = chat.is_user2_typing if request.user == chat.user1 else chat.is_user1_typing

    return JsonResponse({'messages': data, 'typing': typing})
import json

@csrf_exempt
@login_required
def typing_status(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)

    try:
        data = json.loads(request.body)
        typing = data.get('typing', True)
    except:
        typing = True

    if chat.user1 == request.user:
        chat.is_user1_typing = typing
    else:
        chat.is_user2_typing = typing

    chat.save()
    return JsonResponse({'status': 'ok'}) 
    
  

@login_required
def create_snippet(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        html = request.POST.get("html_code")
        css = request.POST.get("css_code")
        js = request.POST.get("js_code")
        language = request.POST.get("language")
        difficulty = request.POST.get("difficulty")
        tags = request.POST.get("tags")
        visibility = request.POST.get("visibility")
        license_value = request.POST.get("license")
        is_draft = 'save_draft' in request.POST

        snippet = Snippet.objects.create(
            title=title,
            description=description,
            html_code=html,
            css_code=css,
            js_code=js,
            language=language,
            difficulty=difficulty,
            tags=tags,
            visibility=visibility,
            license=license_value,
            is_draft=is_draft,
            author=request.user
        )
        return redirect("list")

    return render(request, "formsniper.html") 
    
                                          
from django.core.paginator import Paginator

def snippet_list(request):
    lang = request.GET.get("lang", "all")
    sort = request.GET.get("sort", "newest")

    snippets = Snippet.objects.filter(is_draft=False)

    if lang != "all":
        snippets = snippets.filter(language=lang)

    if sort == "views":
        snippets = snippets.order_by("-views")
    elif sort == "likes":
        snippets = snippets.order_by("-likes")
    elif sort == "popular":
        snippets = snippets.order_by("-likes", "-views")
    else:  # newest
        snippets = snippets.order_by("-created_at")

    paginator = Paginator(snippets, 6)
    page = request.GET.get("page")
    snippets_page = paginator.get_page(page)

    return render(request, "sniper.html", {
        "snippets": snippets_page,
        "page_obj": snippets_page,
        "current_page": snippets_page.number,
        "total_pages": paginator.num_pages,
    })      

from django.shortcuts import render, get_object_or_404
from .models import Snippet

def snippet_detail(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)
    return render(request, "snippet_detail.html", {"snippet": snippet})
        
            
from django.db.models import F

def snippet_list(request):
    snippets = Snippet.objects.all().order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        snippets = snippets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    language = request.GET.get('language')
    if language:
        snippets = snippets.filter(language=language)

    difficulty = request.GET.get('difficulty')
    if difficulty:
        snippets = snippets.filter(difficulty=difficulty)

    paginator = Paginator(snippets, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sniper.html', {
        'snippets': page_obj.object_list,
        'page_obj': page_obj
    })
    
    
# views.py
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

@login_required
@require_POST
def ajax_delete_snippet(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)
    if snippet.author != request.user:
        return HttpResponseForbidden("Not allowed")
    snippet.delete()
    return JsonResponse({"status": "ok"})  
    

from django.forms import ModelForm
from django import forms
from .models import Snippet

class SnippetQuickForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["title", "description", "language", "difficulty", "html_code", "css_code", "js_code"]

@login_required
@require_POST
def ajax_update_snippet(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)
    if snippet.author != request.user:
        return HttpResponseForbidden("Not allowed")

    form = SnippetQuickForm(request.POST, instance=snippet)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "ok"})

    print("Erreurs du formulaire :", form.errors)  # <== AJOUTE CECI
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    
    
@require_POST
@login_required
def like_snippet(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)

    # Ex: un système toggle like (sinon, juste incrémente `likes`)
    snippet.likes += 1
    snippet.save(update_fields=["likes"])
    return JsonResponse({"status": "ok", "likes": snippet.likes})    
    
