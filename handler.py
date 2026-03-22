import os
from twilio.rest import Client
from states import get_state, set_state, get_data, set_data, reset
from dotenv import load_dotenv

load_dotenv()

NOM = "Bros Burger Dakar"
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

PHOTOS = {
    "bienvenue": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80",
    "menu":      "https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&q=80",
    "classic":   "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=800&q=80",
    "smash":     "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=800&q=80",
    "chicken":   "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=800&q=80",
    "frites":    "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=800&q=80",
    "boisson":   "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=800&q=80",
}

def send_image(to, url, caption=""):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        from_=FROM_NUMBER,
        to=to,
        media_url=[url],
        body=caption
    )

def handle_message(phone, text):
    state = get_state(phone)
    t = text.lower().strip()

    # Reset global depuis n'importe ou
    if t in ["menu", "0", "retour", "accueil", "restart", "bonjour", "salut", "hi", "hello"]:
        reset(phone)
        # Image d'abord, texte ensuite
        send_image(phone, PHOTOS["bienvenue"], f"Bienvenue chez {NOM}")
        set_state(phone, "menu")
        return (
            "Que souhaitez-vous faire ?\n\n"
            "1 - Commander\n"
            "2 - Reserver une table\n"
            "3 - Voir le menu complet\n"
            "4 - Horaires et infos\n\n"
            "Tapez le numero de votre choix."
        )

    # ── STATE : START ──────────────────────────────────────────
    if state == "start":
        reset(phone)
        send_image(phone, PHOTOS["bienvenue"], f"Bienvenue chez {NOM}")
        set_state(phone, "menu")
        return (
            "Que souhaitez-vous faire ?\n\n"
            "1 - Commander\n"
            "2 - Reserver une table\n"
            "3 - Voir le menu complet\n"
            "4 - Horaires et infos\n\n"
            "Tapez le numero de votre choix."
        )

    # ── STATE : MENU ───────────────────────────────────────────
    elif state == "menu":
        if t == "1":
            set_state(phone, "commande_categorie")
            send_image(phone, PHOTOS["menu"], "Notre selection")
            return (
                "Choisissez une categorie :\n\n"
                "1 - Classic Burger  —  3 500 FCFA\n"
                "2 - Smash Burger    —  4 000 FCFA\n"
                "3 - Chicken Burger  —  3 500 FCFA\n"
                "4 - Frites et Sides —  1 000 FCFA\n"
                "5 - Boissons        —    500 FCFA\n\n"
                "Tapez le numero."
            )
        elif t == "2":
            set_state(phone, "resa_date")
            return (
                "Parfait, on prepare votre reservation.\n\n"
                "Pour quelle date ?\n"
                "Exemple : Samedi 22 mars"
            )
        elif t == "3":
            send_image(phone, PHOTOS["menu"], "Menu complet")
            return (
                "BURGERS\n"
                "- Classic Burger : 3 500 FCFA\n"
                "- Smash Burger   : 4 000 FCFA\n"
                "- Chicken Burger : 3 500 FCFA\n\n"
                "ACCOMPAGNEMENTS\n"
                "- Frites maison  : 1 000 FCFA\n"
                "- Onion rings    : 1 200 FCFA\n"
                "- Coleslaw       :   800 FCFA\n\n"
                "BOISSONS\n"
                "- Jus naturel    :   800 FCFA\n"
                "- Soda           :   500 FCFA\n"
                "- Eau            :   300 FCFA\n\n"
                "Tapez 1 pour commander\n"
                "ou 0 pour le menu principal."
            )
        elif t == "4":
            return (
                f"{NOM}\n"
                "---------------------------\n"
                "Horaires : Lun-Dim 11h - 23h\n"
                "Livraison sur tout Dakar\n"
                "Temps : 30 a 45 minutes\n"
                "---------------------------\n"
                "Tapez 0 pour revenir au menu."
            )
        else:
            return (
                "Tapez un numero valide :\n"
                "1 - Commander\n"
                "2 - Reserver\n"
                "3 - Voir le menu\n"
                "4 - Infos et horaires"
            )

    # ── STATE : COMMANDE categorie ─────────────────────────────
    elif state == "commande_categorie":
        cats = {
            "1": ("Classic Burger", "3 500", "classic"),
            "2": ("Smash Burger",   "4 000", "smash"),
            "3": ("Chicken Burger", "3 500", "chicken"),
            "4": ("Frites et Sides","1 000", "frites"),
            "5": ("Boisson",        "500",   "boisson"),
        }
        if t in cats:
            nom_cat, prix, photo_key = cats[t]
            set_data(phone, "categorie", f"{nom_cat} - {prix} FCFA")
            set_state(phone, "commande_quantite")
            send_image(phone, PHOTOS[photo_key], nom_cat)
            return (
                f"Vous avez choisi : {nom_cat}\n"
                f"Prix unitaire    : {prix} FCFA\n\n"
                "Combien en voulez-vous ?\n"
                "Exemple : 2"
            )
        else:
            return "Tapez un numero de 1 a 5 pour choisir."

    # ── STATE : COMMANDE quantite ──────────────────────────────
    elif state == "commande_quantite":
        set_data(phone, "quantite", text)
        set_state(phone, "commande_details")
        return (
            "Des precisions sur votre commande ?\n"
            "(sans oignons, extra sauce, etc.)\n\n"
            "Ou tapez NON si rien a ajouter."
        )

    # ── STATE : COMMANDE details ───────────────────────────────
    elif state == "commande_details":
        if t == "non":
            set_data(phone, "details", "Aucune precision")
        else:
            set_data(phone, "details", text)
        set_state(phone, "commande_adresse")
        return (
            "Votre adresse de livraison ?\n\n"
            "Indiquez : quartier, rue,\n"
            "et un point de repere."
        )

    # ── STATE : COMMANDE adresse ───────────────────────────────
    elif state == "commande_adresse":
        set_data(phone, "adresse", text)
        set_state(phone, "commande_nom")
        return "Votre prenom pour la commande ?"

    # ── STATE : COMMANDE nom ───────────────────────────────────
    elif state == "commande_nom":
        set_data(phone, "nom", text)
        data = get_data(phone)
        reset(phone)
        return (
            "Commande confirmee !\n"
            "==========================\n"
            f"Nom      : {data.get('nom')}\n"
            f"Article  : {data.get('categorie')}\n"
            f"Quantite : {data.get('quantite')}\n"
            f"Details  : {data.get('details')}\n"
            f"Adresse  : {data.get('adresse')}\n"
            "==========================\n"
            "Temps estime : 30 a 45 min\n"
            "On vous contacte si besoin.\n\n"
            "Tapez 0 pour un nouvel ordre."
        )

    # ── STATE : RESERVATION date ───────────────────────────────
    elif state == "resa_date":
        set_data(phone, "date", text)
        set_state(phone, "resa_heure")
        return (
            "A quelle heure arriverez-vous ?\n"
            "Exemple : 20h00"
        )

    # ── STATE : RESERVATION heure ──────────────────────────────
    elif state == "resa_heure":
        set_data(phone, "heure", text)
        set_state(phone, "resa_personnes")
        return (
            "Combien de personnes serez-vous ?\n"
            "Exemple : 2"
        )

    # ── STATE : RESERVATION personnes ─────────────────────────
    elif state == "resa_personnes":
        set_data(phone, "personnes", text)
        set_state(phone, "resa_nom")
        return (
            f"Table pour {text} personnes notee.\n\n"
            "Votre nom pour la reservation ?"
        )

    # ── STATE : RESERVATION nom ────────────────────────────────
    elif state == "resa_nom":
        set_data(phone, "nom", text)
        data = get_data(phone)
        reset(phone)
        return (
            "Reservation confirmee !\n"
            "==========================\n"
            f"Nom       : {data.get('nom')}\n"
            f"Date      : {data.get('date')}\n"
            f"Heure     : {data.get('heure')}\n"
            f"Personnes : {data.get('personnes')}\n"
            "==========================\n"
            "Nous vous attendons avec plaisir.\n\n"
            "Tapez 0 pour revenir au menu."
        )

    # ── FALLBACK ───────────────────────────────────────────────
    else:
        reset(phone)
        send_image(phone, PHOTOS["bienvenue"], f"Bienvenue chez {NOM}")
        set_state(phone, "menu")
        return (
            "Que souhaitez-vous faire ?\n\n"
            "1 - Commander\n"
            "2 - Reserver une table\n"
            "3 - Voir le menu complet\n"
            "4 - Horaires et infos"
        )
