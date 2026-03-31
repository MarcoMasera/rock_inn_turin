from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import ChatReply


class ChannelConnector(ABC):
    @abstractmethod
    async def send_reply(self, reply: ChatReply) -> None:
        """Invia risposta verso canale esterno."""
