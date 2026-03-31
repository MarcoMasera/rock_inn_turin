from __future__ import annotations

from app.models import ChatMessage, ChatReply
from app.services.property_repository import PropertyRepository


class ChatbotService:
    """Motore base: usa FAQ e fallback per risposte immediate.

    In una fase successiva qui puoi integrare LLM + retrieval
    (es. OpenAI + vector DB), mantenendo invariata la parte canali.
    """

    def __init__(self, repository: PropertyRepository) -> None:
        self.repository = repository

    def reply(self, message: ChatMessage) -> ChatReply:
        property_info = self.repository.get(message.property_id)
        if not property_info:
            return ChatReply(
                property_id=message.property_id,
                sender_id=message.sender_id,
                reply=(
                    "Non trovo ancora la struttura. "
                    "Completa prima la registrazione dei dati base."
                ),
            )

        normalized = message.text.strip().lower()
        for question, answer in property_info.faq.items():
            if question.lower() in normalized or normalized in question.lower():
                return ChatReply(
                    property_id=message.property_id,
                    sender_id=message.sender_id,
                    reply=answer,
                )

        fallback = (
            f"Ciao! Sono l'assistente di {property_info.name}. "
            f"Check-in dalle {property_info.check_in_from}, "
            f"check-out entro le {property_info.check_out_until}. "
            "Se vuoi, posso passarti un operatore."
        )
        return ChatReply(
            property_id=message.property_id,
            sender_id=message.sender_id,
            reply=fallback,
        )
