from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.connectors.pms_stubs import AirbnbConnector, BookingConnector
from app.connectors.whatsapp_connector import WhatsAppBusinessConnector
from app.models import Channel, ChatMessage, ChatReply, PropertyRegistrationRequest
from app.services.chatbot_service import ChatbotService
from app.services.property_repository import PropertyRepository

app = FastAPI(title="Hospitality Chatbot API", version="0.1.0")

repository = PropertyRepository()
chatbot_service = ChatbotService(repository=repository)
connectors = {
    Channel.whatsapp_business: WhatsAppBusinessConnector(),
    Channel.airbnb: AirbnbConnector(),
    Channel.booking: BookingConnector(),
}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/properties/register", response_model=PropertyRegistrationRequest)
def register_property(payload: PropertyRegistrationRequest) -> PropertyRegistrationRequest:
    return repository.upsert(payload)


@app.post("/chat/incoming", response_model=ChatReply)
async def chat_incoming(message: ChatMessage) -> ChatReply:
    reply = chatbot_service.reply(message)

    connector = connectors.get(message.channel)
    if not connector:
        raise HTTPException(status_code=400, detail="Canale non supportato")

    await connector.send_reply(reply)
    return reply
