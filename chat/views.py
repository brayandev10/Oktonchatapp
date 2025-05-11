from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Room, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



@login_required
# Page d'accueil affichant les salles
def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})
        
def index(request):
    return render(request, 'sniper.html')

# Vue de la room (page de chat)


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
# Vérifie si la room existe ou la crée
def checkview(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        username = request.user.username  # plus besoin de le saisir

        if not room_name:
            return JsonResponse({'error': 'Nom du groupe requis'}, status=400)

        room, created = Room.objects.get_or_create(name=room_name)
        return redirect(f'/{room.name}/')
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
# Envoi de message (avec ou sans fichier)

@login_required
@csrf_exempt
def send(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        room_id = request.POST.get('room_id')
        file = request.FILES.get('file')

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Utilisateur non authentifié'}, status=401)

        if not room_id:
            return JsonResponse({'error': 'Champs manquants'}, status=400)

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room introuvable'}, status=404)

        Message.objects.create(
            value=message,
            user=request.user.username,
            room=room,
            file=file
        )
        return JsonResponse({'status': 'Message envoyé'})

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    
# Récupération des messages d'une salle
def getMessages(request, room):
    try:
        room_obj = Room.objects.get(name=room)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Salle non trouvée'}, status=404)

    messages = Message.objects.filter(room=room_obj).order_by('date')

    data = [{
        'user': m.user,
        'value': m.value,
        'date': m.date.isoformat(),
        'read': m.read,
        'file_url': m.file.url if m.file else '',
        'file_name': m.file.name.split('/')[-1] if m.file else '',
        'file_size': m.file.size if m.file else 0,
    } for m in messages]

    return JsonResponse({'messages': data})

import re

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

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
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register')

        # Création de l'utilisateur
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request, 'register.html')
    
    

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



                      