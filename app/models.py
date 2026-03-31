from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Channel(str, Enum):
    whatsapp_business = "whatsapp_business"
    airbnb = "airbnb"
    booking = "booking"


class PropertyBaseInfo(BaseModel):
    property_id: str = Field(..., description="ID univoco della struttura")
    name: str = Field(..., description="Nome della struttura")
    address: str
    check_in_from: str
    check_out_until: str
    phone: Optional[str] = None
    email: Optional[str] = None
    amenities: List[str] = Field(default_factory=list)
    faq: Dict[str, str] = Field(
        default_factory=dict,
        description="Domanda -> risposta usata dal chatbot nelle risposte rapide",
    )


class PropertyRegistrationRequest(PropertyBaseInfo):
    pass


class ChatMessage(BaseModel):
    channel: Channel
    property_id: str
    sender_id: str
    text: str


class ChatReply(BaseModel):
    property_id: str
    sender_id: str
    reply: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
