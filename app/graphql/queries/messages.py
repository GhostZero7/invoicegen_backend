import strawberry

from app.graphql.types.messages import Message, MessageInput




@strawberry.type
class MessageQuery:
    @strawberry.field
    def get_messages(self, info: strawberry.Info,
        skip: int = 0,
        limit: int = 50,
        order_by: str = "created_at",
        order_desc: bool = True, )-> Message:
        """
        Get list of messages
        """
        return Message(id="", ai_response="Helllo How can help you", user_message="hi")