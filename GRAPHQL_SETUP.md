# GraphQL Setup Guide

## Installation Steps

### 1. Activate Virtual Environment

Before installing dependencies, make sure your virtual environment is active.

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

The GraphQL implementation requires these additional packages:
- `strawberry-graphql[fastapi]` - GraphQL library for Python
- `pyotp` - For two-factor authentication

**Using uv (recommended):**
```bash
uv pip install -r requirements.txt
```

Or install individually:
```bash
uv pip install strawberry-graphql[fastapi]==0.245.2 pyotp==2.9.0
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### 3. Fix python-jose Compatibility (Python 3.14)

The requirements.txt has been updated to use `python-jose[cryptography]==3.3.0` which is compatible with Python 3.14. If you had the old version installed:

```bash
uv pip uninstall python-jose
uv pip install python-jose[cryptography]==3.3.0
```

### 4. Run the Server

```bash
fastapi run app.main:app
```

Or with uvicorn for development:
```bash
uvicorn app.main:app --reload
```

### 5. Access GraphQL Playground

Open your browser and navigate to:
```
http://localhost:8000/graphql
```

You should see the GraphQL Playground interface where you can test queries and mutations.

## Quick Test

Try this query in the GraphQL Playground:

```graphql
query {
  users(limit: 5) {
    id
    email
    firstName
    lastName
    role
  }
}
```

## What Was Implemented

### Schema-First Approach
- GraphQL schema defined in `app/graphql/schema/user.gql`
- Type-safe Strawberry types in `app/graphql/types/user.py`

### User Queries
- `me` - Get current authenticated user
- `user(id)` - Get user by ID
- `users(skip, limit, role, status)` - List users with filters

### User Mutations
- `createUser` - Create new user
- `updateUser` - Update user information
- `updatePassword` - Change password
- `deleteUser` - Soft delete user
- `verifyEmail` - Verify email address
- `enableTwoFactor` - Enable 2FA
- `disableTwoFactor` - Disable 2FA

### Features
- JWT authentication support
- Optional authentication (some queries work without auth)
- Full CRUD operations
- Two-factor authentication with TOTP
- Type safety with Strawberry
- Database integration with SQLAlchemy

## Project Structure

```
app/graphql/
├── schema/
│   └── user.gql          # GraphQL schema definition
├── types/
│   └── user.py           # Strawberry types
├── queries/
│   └── user.py           # Query resolvers
├── mutations/
│   └── user.py           # Mutation resolvers
├── context.py            # GraphQL context
├── schema.py             # Root schema
├── README.md             # Documentation
└── examples.md           # Usage examples
```

## Next Steps

1. **Test the API**: Use the examples in `app/graphql/examples.md`
2. **Add More Models**: Implement GraphQL for Invoice, Client, Business, etc.
3. **Add Permissions**: Implement field-level authorization
4. **Optimize Queries**: Add DataLoaders to prevent N+1 queries
5. **Add Subscriptions**: Real-time updates with WebSocket

## Troubleshooting

### Issue: "python-jose" syntax error
**Solution**: Reinstall with cryptography support:
```bash
pip install python-jose[cryptography]==3.3.0
```

### Issue: Pydantic V2 warnings about "orm_mode"
**Solution**: Already fixed - all schemas now use `from_attributes = True`

### Issue: Import errors
**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database connection errors
**Solution**: Check your `.env` file has correct database credentials

## Documentation

- Full API documentation: `app/graphql/README.md`
- Usage examples: `app/graphql/examples.md`
- Strawberry docs: https://strawberry.rocks/
