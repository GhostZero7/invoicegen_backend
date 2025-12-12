# InvoiceGen Backend

A comprehensive invoicing and financial management system built with FastAPI, GraphQL (Strawberry), and PostgreSQL. This backend provides both REST and GraphQL APIs for managing invoices, clients, payments, and business operations.

## 🚀 Features

### Core Functionality
- **User Management**: Multi-role authentication (Admin, Accountant, User)
- **Business Profiles**: Multi-tenant support with business-specific settings
- **Client Management**: Individual and company clients with contacts
- **Invoice System**: Complete invoice lifecycle management
- **Payment Tracking**: Multiple payment methods and status tracking
- **Product Catalog**: Inventory and service management
- **Categories**: Organize invoices, products, and expenses

### Technical Features
- **Dual API**: REST (FastAPI) and GraphQL (Strawberry)
- **JWT Authentication**: Secure token-based authentication
- **Two-Factor Authentication**: TOTP-based 2FA support
- **Database Migrations**: Alembic for schema management
- **Type Safety**: Full Pydantic validation and SQLAlchemy ORM
- **CORS Support**: Configurable cross-origin resource sharing

## 📋 Prerequisites

- Python 3.14+
- PostgreSQL 12+
- uv (Python package manager) or pip

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd invoicegen_backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies

Using uv (recommended):
```bash
pip install uv
```

Using pip:
```bash
uv sync
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/invoicegen

# JWT Configuration
JWT_SECRET=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
ENVIRONMENT=development
```

### 5. Database Setup

Run migrations:
```bash
alembic upgrade head
```

Or create tables directly:
```bash
python create_tables.py
```

### 6. Seed Database (Optional)

Populate with test data:
```bash
python seed_database.py
```

This creates:
- 10 users (2 admins, 7 accountants, 1 user)
- 10 business profiles
- 40+ clients
- 100+ invoices with items
- 60+ payments
- Products, categories, and addresses

## 🚀 Running the Application

### Development Server

```bash
fastapi dev
```

Or with uvicorn:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Production Server

```bash
fastapi run app.main:app
```

Or:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

### REST API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### GraphQL API

- **GraphiQL Interface**: http://localhost:8000/graphql
- **GraphQL Endpoint**: POST http://localhost:8000/graphql

## 🔐 Authentication

### Login

**REST API:**
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "admin1@invoicegen.com",
  "password": "Admin123!"
}
```

**GraphQL:**
```graphql
mutation {
  login(email: "admin1@invoicegen.com", password: "Admin123!") {
    accessToken
    user {
      id
      email
      role
    }
  }
}
```

### Using the Token

Add to request headers:
```
Authorization: Bearer <your-jwt-token>
```

### Default Credentials (After Seeding)

- **Admin**: `admin1@invoicegen.com` / `Admin123!`
- **Accountant**: `accountant1@invoicegen.com` / `Account123!`
- **User**: `user@invoicegen.com` / `User123!`

## 📖 GraphQL Examples

### Query Users

```graphql
query {
  users(limit: 10, role: ADMIN) {
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

### Create User

```graphql
mutation {
  createUser(input: {
    email: "newuser@example.com"
    password: "SecurePass123!"
    firstName: "John"
    lastName: "Doe"
    role: USER
  }) {
    id
    email
    firstName
    lastName
  }
}
```

### Get Current User

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

More examples in [`app/graphql/examples.md`](app/graphql/examples.md)

## 🏗️ Project Structure

```
invoicegen_backend/
├── app/
│   ├── alembic/              # Database migrations
│   ├── api/                  # REST API endpoints
│   ├── auth/                 # Authentication logic
│   │   ├── router.py         # Auth endpoints
│   │   ├── schemas.py        # Auth schemas
│   │   └── utils.py          # Password hashing, JWT
│   ├── core/                 # Core configuration
│   │   ├── config.py         # Settings
│   │   └── deps.py           # Dependencies (DB, auth)
│   ├── db/                   # Database layer
│   │   ├── models/           # SQLAlchemy models
│   │   ├── database.py       # DB connection
│   │   └── session.py        # Session management
│   ├── graphql/              # GraphQL API
│   │   ├── schema/           # GraphQL schemas (.gql)
│   │   ├── types/            # Strawberry types
│   │   ├── queries/          # Query resolvers
│   │   ├── mutations/        # Mutation resolvers
│   │   ├── context.py        # GraphQL context
│   │   └── schema.py         # Root schema
│   ├── invoices/             # Invoice module
│   ├── routers/              # REST routers
│   └── main.py               # Application entry
├── seed_database.py          # Database seeder
├── create_tables.py          # Table creation script
├── reset_db.py               # Database reset script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🗄️ Database Models

### Core Models

- **User**: System users with roles (Admin, Accountant, User)
- **BusinessProfile**: Business information and settings
- **Client**: Individual or company clients
- **Invoice**: Invoice records with status tracking
- **InvoiceItem**: Line items for invoices
- **Payment**: Payment records linked to invoices
- **Product**: Products and services catalog
- **Category**: Categorization for invoices and products
- **Address**: Polymorphic addresses for users, businesses, and clients

### Relationships

```
User (1) ──→ (N) BusinessProfile
BusinessProfile (1) ──→ (N) Client
BusinessProfile (1) ──→ (N) Invoice
BusinessProfile (1) ──→ (N) Product
Client (1) ──→ (N) Invoice
Invoice (1) ──→ (N) InvoiceItem
Invoice (1) ──→ (N) Payment
Product (1) ──→ (N) InvoiceItem
```

## 🔧 Configuration

### Database

Edit `.env` file:
```env
DATABASE_URL=postgresql://username:password@host:port/database
```

### JWT Settings

```env
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### CORS

Edit `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing

### Manual Testing

Use the seeded data:
```bash
python seed_database.py
```

Then test via:
- GraphiQL: http://localhost:8000/graphql
- Swagger: http://localhost:8000/docs

### Reset Database

```bash
python reset_db.py
python seed_database.py
```

## 📦 Dependencies

### Core
- **FastAPI**: Modern web framework
- **Strawberry GraphQL**: GraphQL library for Python
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migrations
- **Pydantic**: Data validation

### Authentication
- **python-jose**: JWT tokens
- **passlib**: Password hashing
- **bcrypt**: Bcrypt hashing
- **pyotp**: Two-factor authentication

### Database
- **psycopg2-binary**: PostgreSQL adapter

## 🚨 Common Issues

### bcrypt Version Error

If you see bcrypt compatibility errors:
```bash
uv pip install bcrypt==4.0.1
```

### Database Connection Error

Check your `.env` file has correct credentials:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Import Errors

Make sure you're in the project root and virtual environment is activated:
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

## 📝 Additional Documentation

- [GraphQL Setup Guide](GRAPHQL_SETUP.md)
- [GraphQL Examples](app/graphql/examples.md)
- [GraphQL API Documentation](app/graphql/README.md)
- [Database Seeder Guide](SEEDER_README.md)

## 🛣️ Roadmap

- [ ] Email notifications for invoices
- [ ] PDF generation for invoices
- [ ] Recurring invoices
- [ ] Expense tracking
- [ ] Reports and analytics
- [ ] Multi-currency support
- [ ] Tax calculations
- [ ] Payment gateway integrations
- [ ] WebSocket subscriptions for real-time updates
- [ ] File uploads for attachments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Strawberry GraphQL for GraphQL support
- SQLAlchemy for the powerful ORM
