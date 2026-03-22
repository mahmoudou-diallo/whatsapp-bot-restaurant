Bot WhatsApp conversationnel pour restaurant. Un client envoie un message, le bot guide la commande ou la réservation jusqu'à la confirmation — sans intervention humaine.

Construit avec Flask + Twilio + ngrok. Testé en mars 2026 sur Twilio Sandbox depuis Ubuntu/WSL.

## Lancement

Deux terminaux en parallèle :

Terminal 1 — Flask
cd ~/whatsapp-bot && python3 app.py

Terminal 2 — ngrok
ngrok http 5000

Coller l'URL ngrok dans Twilio Console → Sandbox Settings → Webhook URL :
https://xxxx.ngrok-free.app/webhook

## Stack

- Python · Flask · Twilio WhatsApp API · ngrok · Ubuntu/WSL

## Fichiers

- app.py — serveur Flask, reçoit les webhooks Twilio
- handler.py — logique conversationnelle, machine à états
- states.py — sessions en mémoire par numéro de téléphone
- .env.example — template variables d'environnement

## Variables d'environnement

Copier .env.example en .env et remplir :
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+141........

## Auteur

Mahmoudou Diallo · linkedin.com/in/mahmoudou-diallo-qhse · matzodiallo02@gmail.com
