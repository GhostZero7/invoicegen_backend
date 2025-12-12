from .user import UserMutation
# from .business import BusinessMutation
from .client import ClientMutation
from .invoice import InvoiceMutation
from .payment import PaymentMutation
from app.graphql.mutations.business import BusinessMutation

__all__ = [
    "UserMutation",
    "BusinessMutation",
    "ClientMutation",
    "InvoiceMutation",
    "PaymentMutation",
]
