from __future__ import annotations

import os

import httpx

from app.connectors.base import ChannelConnector
from app.models import ChatReply


class WhatsAppBusinessConnector(ChannelConnector):
    """Bozza connector per WhatsApp Cloud API (Meta)."""

    def __init__(self) -> None:
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.token = os.getenv("WHATSAPP_TOKEN", "")

    async def send_reply(self, reply: ChatReply) -> None:
        if not self.phone_number_id or not self.token:
            # In sviluppo: non fallire se le credenziali non sono configurate.
            print(f"[WHATSAPP-DRYRUN] A {reply.sender_id}: {reply.reply}")
            return

        url = f"https://graph.facebook.com/v22.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": reply.sender_id,
            "type": "text",
            "text": {"body": reply.reply},
        }
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
