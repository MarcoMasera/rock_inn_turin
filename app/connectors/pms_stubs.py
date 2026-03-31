from __future__ import annotations

from app.connectors.base import ChannelConnector
from app.models import ChatReply


class AirbnbConnector(ChannelConnector):
    async def send_reply(self, reply: ChatReply) -> None:
        print(f"[AIRBNB-STUB] A {reply.sender_id}: {reply.reply}")


class BookingConnector(ChannelConnector):
    async def send_reply(self, reply: ChatReply) -> None:
        print(f"[BOOKING-STUB] A {reply.sender_id}: {reply.reply}")
