from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow
import marshmallow_dataclass


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Chat:
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    type: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Message:
    message_id: int
    chat: Chat
    msg_from: MessageFrom = field(metadata={'data_key': 'from'})
    text: Optional[str]
    date: int

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Optional[Message]
    edited_message: Optional[Message]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


GET_UPDATES_RESPONSE_SCHEMA = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
SEND_MESSAGE_RESPONSE_SCHEMA = marshmallow_dataclass.class_schema(SendMessageResponse)()
