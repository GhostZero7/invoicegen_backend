import strawberry


from typing import Optional
from enum import Enum



@strawberry.type
class Message:
    id: strawberry.ID
    ai_response: str
    user_message: str
    # attachments: Optional[list]


@strawberry.input
class MessageInput:
    user_message: str
    # attachments: Optional[list]