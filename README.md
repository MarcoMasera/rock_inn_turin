# Rock Inn Turin - Bozza chatbot multicanale

Ti propongo **Python** per iniziare: è rapido per prototipare integrazioni API (WhatsApp, Airbnb, Booking) e mantenere un'architettura pulita prima di scalare.

## Obiettivo di questa bozza

- Registrare i dati base della struttura (che fungono da "knowledge base" iniziale).
- Rispondere ai messaggi ospiti con logica FAQ + fallback.
- Inviare la risposta al canale corretto:
  - WhatsApp Business (bozza con Cloud API Meta)
  - Airbnb (stub)
  - Booking (stub)

## Avvio

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## Esempio 1: registrazione struttura

```bash
curl -X POST http://127.0.0.1:8000/properties/register \
  -H 'Content-Type: application/json' \
  -d '{
    "property_id": "torino_001",
    "name": "Rock Inn Torino Centro",
    "address": "Via Roma 10, Torino",
    "check_in_from": "15:00",
    "check_out_until": "10:30",
    "phone": "+390111234567",
    "email": "info@rockinn.example",
    "amenities": ["wifi", "colazione", "self check-in"],
    "faq": {
      "parcheggio": "Collaboriamo con il parcheggio X a 300m, tariffa convenzionata.",
      "animali": "Animali ammessi su richiesta con supplemento di 15€ a soggiorno."
    }
  }'
```

## Esempio 2: messaggio in ingresso da WhatsApp

```bash
curl -X POST http://127.0.0.1:8000/chat/incoming \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "whatsapp_business",
    "property_id": "torino_001",
    "sender_id": "393331112233",
    "text": "Ciao, avete parcheggio?"
  }'
```

Se non imposti le variabili `WHATSAPP_PHONE_NUMBER_ID` e `WHATSAPP_TOKEN`, la risposta viene stampata in console (`DRYRUN`).

## Prossimi passi consigliati

1. Sostituire la FAQ substring matching con retrieval semantico (embeddings + vector db).
2. Aggiungere autenticazione tenant (multi-struttura/multi-account).
3. Implementare webhook verifica Meta e gestione template messages.
4. Integrare i connettori reali Airbnb/Booking tramite channel manager o API ufficiali disponibili.
5. Tracciare conversazioni e handoff umano con stato ticket.
