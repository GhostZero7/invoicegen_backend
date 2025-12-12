# GraphQL Examples

## Testing with cURL

### Create a User
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createUser(input: { email: \"test@example.com\", password: \"password123\", firstName: \"Test\", lastName: \"User\" }) { id email firstName lastName } }"
  }'
```

### Get Current User (with auth)
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "query": "query { me { id email firstName lastName role } }"
  }'
```

### List Users
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { users(limit: 5) { id email firstName lastName role status } }"
  }'
```

## Testing with Python

```python
import requests

# GraphQL endpoint
url = "http://localhost:8000/graphql"

# Create user mutation
create_user_query = """
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    email
    firstName
    lastName
    role
  }
}
"""

variables = {
    "input": {
        "email": "john@example.com",
        "password": "securepass123",
        "firstName": "John",
        "lastName": "Doe",
        "phone": "+1234567890"
    }
}

response = requests.post(
    url,
    json={"query": create_user_query, "variables": variables}
)

print(response.json())

# Query users
query_users = """
query {
  users(limit: 10, status: ACTIVE) {
    id
    email
    firstName
    lastName
    role
    status
    createdAt
  }
}
"""

response = requests.post(url, json={"query": query_users})
print(response.json())
```

## Testing with JavaScript/TypeScript

```typescript
// Using fetch
const createUser = async () => {
  const query = `
    mutation CreateUser($input: CreateUserInput!) {
      createUser(input: $input) {
        id
        email
        firstName
        lastName
      }
    }
  `;

  const variables = {
    input: {
      email: "jane@example.com",
      password: "password123",
      firstName: "Jane",
      lastName: "Smith"
    }
  };

  const response = await fetch("http://localhost:8000/graphql", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables })
  });

  const data = await response.json();
  console.log(data);
};

// Using Apollo Client
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql',
  cache: new InMemoryCache(),
});

const GET_USERS = gql`
  query GetUsers {
    users(limit: 10) {
      id
      email
      firstName
      lastName
      role
    }
  }
`;

client.query({ query: GET_USERS })
  .then(result => console.log(result.data));
```

## Complex Queries

### Get User with Filtering
```graphql
query GetAdminUsers {
  users(role: ADMIN, status: ACTIVE, limit: 20) {
    id
    email
    firstName
    lastName
    role
    status
    emailVerified
    twoFactorEnabled
    lastLoginAt
    createdAt
  }
}
```

### Update User with Multiple Fields
```graphql
mutation UpdateUserProfile {
  updateUser(
    id: "user-id-here"
    input: {
      firstName: "Updated"
      lastName: "Name"
      phone: "+9876543210"
      avatarUrl: "https://example.com/avatar.jpg"
    }
  ) {
    id
    firstName
    lastName
    phone
    avatarUrl
    updatedAt
  }
}
```

### Enable 2FA and Get Secret
```graphql
mutation Enable2FA {
  enableTwoFactor
}
```

This returns a TOTP secret that can be used to generate QR codes for authenticator apps.

## Error Handling

GraphQL errors are returned in the response:

```json
{
  "data": null,
  "errors": [
    {
      "message": "User with this email already exists",
      "locations": [{"line": 2, "column": 3}],
      "path": ["createUser"]
    }
  ]
}
```

## Using Variables

Always use variables for dynamic values:

```graphql
# Query
mutation CreateUser($email: String!, $password: String!, $firstName: String!, $lastName: String!) {
  createUser(input: {
    email: $email
    password: $password
    firstName: $firstName
    lastName: $lastName
  }) {
    id
    email
  }
}

# Variables (sent separately)
{
  "email": "user@example.com",
  "password": "securepass",
  "firstName": "John",
  "lastName": "Doe"
}
```


## Business Profile Operations

### Create Business Profile
```graphql
mutation CreateBusiness {
  createBusiness(input: {
    businessName: "Acme Corp"
    businessType: LLC
    email: "billing@acme.com"
    phone: "+1234567890"
    taxId: "12-3456789"
    currency: "USD"
    invoicePrefix: "INV"
  }) {
    id
    businessName
    businessType
    email
    invoicePrefix
    nextInvoiceNumber
    createdAt
  }
}
```

### Get My Businesses
```graphql
query MyBusinesses {
  myBusinesses {
    id
    businessName
    businessType
    email
    phone
    currency
    invoicePrefix
    nextInvoiceNumber
    isActive
  }
}
```

### Update Business Profile
```graphql
mutation UpdateBusiness {
  updateBusiness(
    id: "business-id"
    input: {
      website: "https://acme.com"
      logoUrl: "https://acme.com/logo.png"
      paymentTermsDefault: NET_30
      paymentInstructions: "Wire transfer to account 123456"
    }
  ) {
    id
    businessName
    website
    logoUrl
    paymentTermsDefault
    updatedAt
  }
}
```

## Client Operations

### Create Client
```graphql
mutation CreateClient {
  createClient(input: {
    businessId: "business-id"
    clientType: COMPANY
    companyName: "Tech Solutions Inc"
    email: "contact@techsolutions.com"
    phone: "+1987654321"
    taxId: "98-7654321"
    paymentTerms: "net_30"
    currency: "USD"
  }) {
    id
    companyName
    email
    clientType
    status
    createdAt
  }
}
```

### Create Individual Client
```graphql
mutation CreateIndividualClient {
  createClient(input: {
    businessId: "business-id"
    clientType: INDIVIDUAL
    firstName: "John"
    lastName: "Smith"
    email: "john.smith@email.com"
    mobile: "+1555123456"
  }) {
    id
    firstName
    lastName
    email
    clientType
    status
  }
}
```

### List Clients
```graphql
query ListClients {
  clients(
    businessId: "business-id"
    status: ACTIVE
    limit: 20
  ) {
    id
    clientType
    companyName
    firstName
    lastName
    email
    phone
    status
    currency
  }
}
```

### Update Client
```graphql
mutation UpdateClient {
  updateClient(
    id: "client-id"
    input: {
      phone: "+1999888777"
      website: "https://techsolutions.com"
      creditLimit: 50000.00
      notes: "Preferred customer - priority support"
    }
  ) {
    id
    phone
    website
    creditLimit
    notes
    updatedAt
  }
}
```

## Invoice Operations

### Create Invoice with Items
```graphql
mutation CreateInvoice {
  createInvoice(input: {
    businessId: "business-id"
    clientId: "client-id"
    invoiceDate: "2024-01-15"
    dueDate: "2024-02-15"
    paymentTerms: "net_30"
    items: [
      {
        description: "Web Development Services"
        quantity: 40
        unitPrice: 150.00
        unitOfMeasure: "hours"
        taxRate: 10.0
      }
      {
        description: "Hosting Services"
        quantity: 1
        unitPrice: 500.00
        unitOfMeasure: "month"
        taxRate: 10.0
      }
    ]
    discountType: PERCENTAGE
    discountValue: 5.0
    shippingAmount: 0.0
    notes: "Thank you for your business!"
    paymentInstructions: "Wire transfer to account 123456"
  }) {
    id
    invoiceNumber
    status
    subtotal
    discountAmount
    taxAmount
    totalAmount
    amountDue
    createdAt
  }
}
```

### Get Invoice Details
```graphql
query GetInvoice {
  invoice(id: "invoice-id") {
    id
    invoiceNumber
    status
    invoiceDate
    dueDate
    paymentTerms
    subtotal
    discountType
    discountValue
    discountAmount
    taxAmount
    shippingAmount
    totalAmount
    amountPaid
    amountDue
    currency
    notes
    paymentInstructions
    sentAt
    paidAt
  }
}
```

### Get Invoice Items
```graphql
query GetInvoiceItems {
  invoiceItems(invoiceId: "invoice-id") {
    id
    description
    quantity
    unitPrice
    unitOfMeasure
    taxRate
    taxAmount
    discountAmount
    lineTotal
  }
}
```

### List Invoices with Filters
```graphql
query ListInvoices {
  invoices(
    businessId: "business-id"
    status: SENT
    limit: 10
  ) {
    id
    invoiceNumber
    status
    invoiceDate
    dueDate
    totalAmount
    amountPaid
    amountDue
    currency
    createdAt
  }
}
```

### Update Invoice
```graphql
mutation UpdateInvoice {
  updateInvoice(
    id: "invoice-id"
    input: {
      status: SENT
      notes: "Updated payment terms"
    }
  ) {
    id
    status
    notes
    updatedAt
  }
}
```

### Send Invoice
```graphql
mutation SendInvoice {
  sendInvoice(id: "invoice-id")
}
```

### Mark Invoice as Paid
```graphql
mutation MarkInvoiceAsPaid {
  markInvoiceAsPaid(id: "invoice-id")
}
```

### Cancel Invoice
```graphql
mutation CancelInvoice {
  cancelInvoice(id: "invoice-id")
}
```

## Payment Operations

### Create Payment
```graphql
mutation CreatePayment {
  createPayment(input: {
    invoiceId: "invoice-id"
    paymentDate: "2024-01-20"
    amount: 6545.00
    paymentMethod: BANK_TRANSFER
    transactionId: "TXN123456789"
    referenceNumber: "REF-2024-001"
    notes: "Payment received via wire transfer"
  }) {
    id
    paymentNumber
    paymentDate
    amount
    paymentMethod
    transactionId
    status
    createdAt
  }
}
```

### List Payments
```graphql
query ListPayments {
  payments(
    invoiceId: "invoice-id"
    status: COMPLETED
    limit: 10
  ) {
    id
    paymentNumber
    paymentDate
    amount
    paymentMethod
    transactionId
    referenceNumber
    status
    createdAt
  }
}
```

### Get Payment Details
```graphql
query GetPayment {
  payment(id: "payment-id") {
    id
    invoiceId
    paymentNumber
    paymentDate
    amount
    paymentMethod
    transactionId
    referenceNumber
    notes
    status
    createdAt
    updatedAt
  }
}
```

### Update Payment
```graphql
mutation UpdatePayment {
  updatePayment(
    id: "payment-id"
    input: {
      amount: 6600.00
      notes: "Corrected payment amount"
    }
  ) {
    id
    amount
    notes
    updatedAt
  }
}
```

### Refund Payment
```graphql
mutation RefundPayment {
  refundPayment(id: "payment-id")
}
```

## Complete Workflow Example

### 1. Create Business
```graphql
mutation {
  createBusiness(input: {
    businessName: "My Consulting LLC"
    businessType: LLC
    email: "billing@myconsulting.com"
    phone: "+1234567890"
    currency: "USD"
  }) {
    id
  }
}
```

### 2. Create Client
```graphql
mutation {
  createClient(input: {
    businessId: "business-id-from-step-1"
    clientType: COMPANY
    companyName: "Client Corp"
    email: "ap@clientcorp.com"
    phone: "+1987654321"
  }) {
    id
  }
}
```

### 3. Create Invoice
```graphql
mutation {
  createInvoice(input: {
    businessId: "business-id-from-step-1"
    clientId: "client-id-from-step-2"
    invoiceDate: "2024-01-15"
    dueDate: "2024-02-15"
    paymentTerms: "net_30"
    items: [
      {
        description: "Consulting Services"
        quantity: 20
        unitPrice: 200.00
        taxRate: 10.0
      }
    ]
  }) {
    id
    invoiceNumber
    totalAmount
  }
}
```

### 4. Send Invoice
```graphql
mutation {
  sendInvoice(id: "invoice-id-from-step-3")
}
```

### 5. Record Payment
```graphql
mutation {
  createPayment(input: {
    invoiceId: "invoice-id-from-step-3"
    paymentDate: "2024-02-01"
    amount: 4400.00
    paymentMethod: BANK_TRANSFER
  }) {
    id
    paymentNumber
  }
}
```

## Python Complete Example

```python
import requests
from datetime import date, timedelta

url = "http://localhost:8000/graphql"
headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}

# 1. Create business
create_business = """
mutation {
  createBusiness(input: {
    businessName: "Tech Consulting"
    businessType: LLC
    email: "billing@techconsulting.com"
    currency: "USD"
  }) {
    id
    invoicePrefix
  }
}
"""

response = requests.post(url, json={"query": create_business}, headers=headers)
business_id = response.json()["data"]["createBusiness"]["id"]

# 2. Create client
create_client = """
mutation CreateClient($businessId: ID!) {
  createClient(input: {
    businessId: $businessId
    clientType: COMPANY
    companyName: "Acme Inc"
    email: "billing@acme.com"
  }) {
    id
  }
}
"""

response = requests.post(
    url,
    json={"query": create_client, "variables": {"businessId": business_id}},
    headers=headers
)
client_id = response.json()["data"]["createClient"]["id"]

# 3. Create invoice
today = date.today()
due_date = today + timedelta(days=30)

create_invoice = """
mutation CreateInvoice($input: CreateInvoiceInput!) {
  createInvoice(input: $input) {
    id
    invoiceNumber
    totalAmount
  }
}
"""

variables = {
    "input": {
        "businessId": business_id,
        "clientId": client_id,
        "invoiceDate": today.isoformat(),
        "dueDate": due_date.isoformat(),
        "paymentTerms": "net_30",
        "items": [
            {
                "description": "Development Services",
                "quantity": 40,
                "unitPrice": 150.0,
                "taxRate": 10.0
            }
        ]
    }
}

response = requests.post(
    url,
    json={"query": create_invoice, "variables": variables},
    headers=headers
)
invoice_data = response.json()["data"]["createInvoice"]
print(f"Created invoice {invoice_data['invoiceNumber']} for ${invoice_data['totalAmount']}")
```
