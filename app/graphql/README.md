# GraphQL API with Strawberry

This implementation uses Strawberry GraphQL with a schema-first approach for the InvoiceGen backend.

## Features

- **Schema-First Design**: GraphQL schemas defined in `.gql` files
- **Type Safety**: Full type safety with Strawberry types
- **Authentication**: JWT-based authentication with optional auth support
- **User Management**: Complete CRUD operations for users
- **Two-Factor Authentication**: TOTP-based 2FA support

## Structure

```
app/graphql/
├── schema/           # GraphQL schema definitions (.gql files)
│   └── user.gql     # User type definitions
├── types/           # Strawberry type definitions
│   └── user.py      # User types and inputs
├── queries/         # Query resolvers
│   └── user.py      # User queries
├── mutations/       # Mutation resolvers
│   └── user.py      # User mutations
├── context.py       # GraphQL context provider
├── schema.py        # Root schema combining queries and mutations
└── README.md        # This file
```

## Endpoints

- **GraphQL Playground**: `http://localhost:8000/graphql`
- **GraphQL API**: `POST http://localhost:8000/graphql`

## User Queries

### Get Current User
```graphql
query {
  me {
    id
    email
    firstName
    lastName
    role
    status
  }
}
```

### Get User by ID
```graphql
query {
  user(id: "user-id-here") {
    id
    email
    firstName
    lastName
  }
}
```

### List Users
```graphql
query {
  users(skip: 0, limit: 10, role: ADMIN, status: ACTIVE) {
    id
    email
    firstName
    lastName
    role
    status
  }
}
```

## User Mutations

### Create User
```graphql
mutation {
  createUser(input: {
    email: "user@example.com"
    password: "securepassword"
    firstName: "John"
    lastName: "Doe"
    phone: "+1234567890"
    role: USER
  }) {
    id
    email
    firstName
    lastName
  }
}
```

### Update User
```graphql
mutation {
  updateUser(
    id: "user-id-here"
    input: {
      firstName: "Jane"
      lastName: "Smith"
      status: ACTIVE
    }
  ) {
    id
    firstName
    lastName
  }
}
```

### Update Password
```graphql
mutation {
  updatePassword(input: {
    currentPassword: "oldpassword"
    newPassword: "newpassword"
  })
}
```

### Delete User
```graphql
mutation {
  deleteUser(id: "user-id-here")
}
```

### Enable Two-Factor Authentication
```graphql
mutation {
  enableTwoFactor
}
```

### Disable Two-Factor Authentication
```graphql
mutation {
  disableTwoFactor(code: "123456")
}
```

## Authentication

To authenticate requests, include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Some queries (like `me`) require authentication, while others (like `users`) may work without it depending on your permissions setup.

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

Or with uv:

```bash
uv pip install -r requirements.txt
```

## Running the Server

```bash
fastapi run app.main:app
```

Or with uvicorn:

```bash
uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/graphql` to access the GraphQL Playground.

## Next Steps

1. Add more models (Business, Invoice, Client, etc.)
2. Implement DataLoaders for N+1 query optimization
3. Add field-level permissions
4. Implement subscriptions for real-time updates
5. Add pagination with Relay-style connections
6. Implement file uploads for avatars
