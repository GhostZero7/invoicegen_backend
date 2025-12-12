# API Documentation

Complete API reference for InvoiceGen Backend.

## Table of Contents

- [Authentication](#authentication)
- [REST API](#rest-api)
- [GraphQL API](#graphql-api)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

---

## Authentication

All authenticated endpoints require a JWT token in the Authorization header.

### Obtaining a Token

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Include in request headers:
```
Authorization: Bearer <access_token>
```

### Token Expiration

Tokens expire after 30 minutes (configurable in `.env`).

---

## REST API

### Base URL

```
http://localhost:8000
```

### Authentication Endpoints

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Invoice Endpoints

#### Create Invoice

```http
POST /invoices
Authorization: Bearer <token>
Content-Type: application/json

{
  "client_id": "client-uuid",
  "invoice_date": "2024-01-01",
  "due_date": "2024-01-31",
  "payment_terms": "net_30",
  "items": [
    {
      "description": "Web Development",
      "quantity": 10,
      "unit_price": 100.00,
      "tax_rate": 10
    }
  ],
  "notes": "Thank you for your business"
}
```

**Response:** `201 Created`
```json
{
  "id": "invoice-uuid",
  "invoice_number": "INV-1001",
  "status": "draft",
  "subtotal": 1000.00,
  "tax_amount": 100.00,
  "total_amount": 1100.00,
  "amount_due": 1100.00,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### List Invoices

```http
GET /invoices?skip=0&limit=10&status=paid
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "invoices": [
    {
      "id": "uuid",
      "invoice_number": "INV-1001",
      "client_id": "client-uuid",
      "status": "paid",
      "total_amount": 1100.00,
      "amount_due": 0.00,
      "invoice_date": "2024-01-01",
      "due_date": "2024-01-31"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

#### Get Invoice

```http
GET /invoices/{invoice_id}
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "invoice_number": "INV-1001",
  "client": {
    "id": "uuid",
    "email": "client@example.com",
    "company_name": "Acme Corp"
  },
  "items": [
    {
      "id": "uuid",
      "description": "Web Development",
      "quantity": 10,
      "unit_price": 100.00,
      "line_total": 1100.00
    }
  ],
  "subtotal": 1000.00,
  "tax_amount": 100.00,
  "total_amount": 1100.00,
  "amount_paid": 1100.00,
  "amount_due": 0.00,
  "status": "paid"
}
```

#### Update Invoice

```http
PUT /invoices/{invoice_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "sent",
  "notes": "Updated notes"
}
```

**Response:** `200 OK`

#### Delete Invoice

```http
DELETE /invoices/{invoice_id}
Authorization: Bearer <token>
```

**Response:** `204 No Content`

---

## GraphQL API

### Endpoint

```
POST http://localhost:8000/graphql
```

### Interactive Interface

```
http://localhost:8000/graphql
```

### Schema

#### Types

```graphql
type User {
  id: ID!
  email: String!
  firstName: String!
  lastName: String!
  phone: String
  role: UserRole!
  status: UserStatus!
  emailVerified: Boolean!
  twoFactorEnabled: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
}

enum UserRole {
  USER
  ADMIN
  ACCOUNTANT
}

enum UserStatus {
  ACTIVE
  SUSPENDED
  DELETED
}

type Invoice {
  id: ID!
  invoiceNumber: String!
  client: Client!
  status: InvoiceStatus!
  invoiceDate: Date!
  dueDate: Date!
  subtotal: Float!
  taxAmount: Float!
  totalAmount: Float!
  amountPaid: Float!
  amountDue: Float!
  items: [InvoiceItem!]!
  payments: [Payment!]!
}

type Client {
  id: ID!
  email: String!
  firstName: String
  lastName: String
  companyName: String
  clientType: ClientType!
  status: ClientStatus!
}
```

### Queries

#### Get Current User

```graphql
query {
  me {
    id
    email
    firstName
    lastName
    role
    businessProfiles {
      id
      businessName
    }
  }
}
```

#### List Users

```graphql
query {
  users(skip: 0, limit: 10, role: ADMIN, status: ACTIVE) {
    id
    email
    firstName
    lastName
    role
    status
    createdAt
  }
}
```

#### Get User by ID

```graphql
query {
  user(id: "user-uuid") {
    id
    email
    firstName
    lastName
    role
    businessProfiles {
      id
      businessName
      clients {
        id
        email
        companyName
      }
    }
  }
}
```

### Mutations

#### Create User

```graphql
mutation {
  createUser(input: {
    email: "newuser@example.com"
    password: "SecurePass123!"
    firstName: "Jane"
    lastName: "Smith"
    phone: "+1234567890"
    role: ACCOUNTANT
  }) {
    id
    email
    firstName
    lastName
    role
  }
}
```

#### Update User

```graphql
mutation {
  updateUser(
    id: "user-uuid"
    input: {
      firstName: "Updated"
      lastName: "Name"
      status: ACTIVE
    }
  ) {
    id
    firstName
    lastName
    status
    updatedAt
  }
}
```

#### Update Password

```graphql
mutation {
  updatePassword(input: {
    currentPassword: "OldPass123!"
    newPassword: "NewPass123!"
  })
}
```

#### Delete User

```graphql
mutation {
  deleteUser(id: "user-uuid")
}
```

#### Enable Two-Factor Authentication

```graphql
mutation {
  enableTwoFactor
}
```

**Returns:** TOTP secret for QR code generation

#### Disable Two-Factor Authentication

```graphql
mutation {
  disableTwoFactor(code: "123456")
}
```

### Variables

Use variables for dynamic values:

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    email
    firstName
    lastName
  }
}
```

**Variables:**
```json
{
  "input": {
    "email": "user@example.com",
    "password": "SecurePass123!",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

---

## Error Handling

### REST API Errors

#### 400 Bad Request

```json
{
  "detail": "Invalid input data"
}
```

#### 401 Unauthorized

```json
{
  "detail": "Not authenticated"
}
```

#### 403 Forbidden

```json
{
  "detail": "Insufficient permissions"
}
```

#### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

#### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

### GraphQL Errors

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

---

## Rate Limiting

Currently not implemented. Consider adding rate limiting for production:

- Authentication endpoints: 5 requests per minute
- API endpoints: 100 requests per minute
- GraphQL: 50 queries per minute

---

## Pagination

### REST API

Use `skip` and `limit` query parameters:

```http
GET /invoices?skip=0&limit=20
```

### GraphQL

Use `skip` and `limit` arguments:

```graphql
query {
  users(skip: 0, limit: 20) {
    id
    email
  }
}
```

---

## Filtering

### REST API

Use query parameters:

```http
GET /invoices?status=paid&client_id=uuid
```

### GraphQL

Use arguments:

```graphql
query {
  users(role: ADMIN, status: ACTIVE) {
    id
    email
  }
}
```

---

## Sorting

### REST API

Use `sort_by` and `order` parameters:

```http
GET /invoices?sort_by=created_at&order=desc
```

### GraphQL

Currently not implemented. Add to schema as needed.

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store JWT tokens securely** (httpOnly cookies recommended)
3. **Validate all input data**
4. **Use pagination for large datasets**
5. **Implement rate limiting**
6. **Log all authentication attempts**
7. **Use environment variables for secrets**
8. **Enable CORS only for trusted origins**
9. **Implement request timeouts**
10. **Monitor API usage and errors**

---

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: support@invoicegen.com
- Documentation: [repository-url]/docs
