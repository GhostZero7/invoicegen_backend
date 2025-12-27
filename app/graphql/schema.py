import strawberry
from app.graphql.queries.user import UserQuery
from app.graphql.queries.business import BusinessQuery
from app.graphql.queries.client import ClientQuery
from app.graphql.queries.invoice import InvoiceQuery
from app.graphql.queries.payment import PaymentQuery
from app.graphql.queries.product import ProductQuery
from app.graphql.queries.category import CategoryQuery
from app.graphql.queries.waitlist import WaitlistQuery
from app.graphql.queries.billing import BillingQuery
from app.graphql.mutations.user import UserMutation
from app.graphql.mutations.business import BusinessMutation
from app.graphql.mutations.client import ClientMutation
from app.graphql.mutations.invoice import InvoiceMutation
from app.graphql.mutations.payment import PaymentMutation
from app.graphql.mutations.product import ProductMutation
from app.graphql.mutations.category import CategoryMutation
from app.graphql.mutations.waitlist import WaitlistMutation
from app.graphql.mutations.auth import AuthMutation
@strawberry.type
class Query(UserQuery, BusinessQuery, ClientQuery, InvoiceQuery, PaymentQuery, ProductQuery, CategoryQuery, WaitlistQuery, BillingQuery):
    """Root Query combining all query types"""
    pass

@strawberry.type
class Mutation(UserMutation, BusinessMutation, ClientMutation, InvoiceMutation, PaymentMutation, ProductMutation, CategoryMutation, WaitlistMutation, AuthMutation):
    """Root Mutation combining all mutation types"""
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
