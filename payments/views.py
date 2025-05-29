import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import uuid
from .models import Transaction
from django.shortcuts import redirect, render


@csrf_exempt
def paiement_cinetpay(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')  # facultatif si tu veux l'enregistrer
        operator = request.POST.get('operator')          # idem

        if not amount:
            return JsonResponse({"error": "Montant manquant"}, status=400)

        # Génère un ID de transaction unique
        transaction_id = str(uuid.uuid4()).replace("-", "")[:20]

        data = {
            "apikey": settings.CINETPAY_API_KEY,
            "site_id": settings.CINETPAY_SITE_ID,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": "XAF",
            "description": "Paiement en ligne",
            "notify_url": "http://127.0.0.1:8000/payments/notification/",
            "return_url": "http://127.0.0.1:8000/payments/succes/",
            "channels": "ALL"
        }

        try:
            response = requests.post('https://api-checkout.cinetpay.com/v2/payment', json=data)
            res_json = response.json()
        except Exception as e:
            return JsonResponse({"error": "Erreur de communication avec CinetPay"}, status=500)

        if res_json.get("code") == "201":
            # Enregistrement en base de données
            Transaction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                transaction_id=transaction_id,
                amount=amount,
                currency="XAF",
                status="PENDING",
                phone_number=phone_number,
                operator=operator
            )
            return JsonResponse({"payment_url": res_json["data"]["payment_url"]})
        else:
            return JsonResponse({"error": res_json.get("message", "Erreur lors de la création du paiement")})

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def cinetpay_notification(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        if not transaction_id:
            return JsonResponse({"error": "transaction_id manquant"}, status=400)

        url = 'https://api-checkout.cinetpay.com/v2/payment/check'
        data = {
            "apikey": settings.CINETPAY_API_KEY,
            "site_id": settings.CINETPAY_SITE_ID,
            "transaction_id": transaction_id
        }

        try:
            response = requests.post(url, json=data)
            res_json = response.json()
        except Exception as e:
            return JsonResponse({"error": "Erreur lors de la requête CinetPay"}, status=500)

        if res_json.get("code") == "00":
            tx_id = res_json["data"].get("transaction_id")
            transaction = Transaction.objects.filter(transaction_id=tx_id).first()
            if transaction:
                transaction.status = "SUCCESS"
                transaction.save()
        else:
            tx_id = res_json["data"].get("transaction_id")
            transaction = Transaction.objects.filter(transaction_id=tx_id).first()
            if transaction:
                transaction.status = "FAILED"
                transaction.save()

        return JsonResponse({"message": "Notification traitée"})

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    

def paiement_succes(request):
    return render(request, 'paiement_succes.html')     
    
def paiement(request):
    return render(request, 'payment.html')     
    
            

                