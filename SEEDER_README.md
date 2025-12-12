# Database Seeder

This script populates your database with realistic test data for development and testing.

## What Gets Created

- **10 Users**:
  - 2 Admins
  - 7 Accountants
  - 1 Regular User

- **10 Business Profiles** (one per user)
- **30+ Categories** (for invoices and products)
- **80+ Products** (various services and items)
- **40+ Clients** (mix of individuals and companies)
- **100+ Invoices** with line items
- **60+ Payments** (for paid and partially paid invoices)
- **Addresses** for all businesses and clients
- **Client Contacts** for company clients

## Running the Seeder

### Prerequisites

Make sure your database is set up and migrations are run:

```bash
# Run migrations if needed
alembic upgrade head
```

### Run the Seeder

```bash
python seed_database.py
```

## Login Credentials

After seeding, you can log in with these accounts:

### Admin Accounts
```
Email: admin1@invoicegen.com
Password: Admin123!

Email: admin2@invoicegen.com
Password: Admin123!
```

### Accountant Accounts
```
Email: accountant1@invoicegen.com
Password: Account123!

Email: accountant2@invoicegen.com
Password: Account123!

... (accountant3 through accountant7)
```

### Regular User
```
Email: user@invoicegen.com
Password: User123!
```

## Data Distribution

### Invoice Statuses
- **Draft**: ~5%
- **Sent**: ~20%
- **Viewed**: ~10%
- **Paid**: ~40% (most common)
- **Overdue**: ~15%
- **Cancelled**: ~5%
- **Refunded**: ~5%

### Client Types
- **Companies**: ~50%
- **Individuals**: ~50%

### Invoice Items
- Each invoice has 1-5 line items
- Random products from the business's catalog
- Realistic pricing and quantities
- Tax calculations
- Optional discounts

### Payments
- All "Paid" invoices have full payments
- Some "Sent" and "Viewed" invoices have partial payments
- Various payment methods (cash, check, bank transfer, credit card, etc.)

## Resetting the Database

If you want to start fresh:

```bash
# Option 1: Use the reset script
python reset_db.py

# Option 2: Drop and recreate tables
python create_tables.py

# Then run the seeder again
python seed_database.py
```

## GraphQL Testing

After seeding, you can test GraphQL queries:

```graphql
# Get all users
query {
  users(limit: 10) {
    id
    email
    firstName
    lastName
    role
    status
  }
}

# Login as admin
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

## Customization

You can modify the seeder to create more or less data:

```python
# In seed_database.py

# Change number of invoices per business
num_invoices = random.randint(10, 15)  # Change these numbers

# Change number of clients per business
num_clients = random.randint(3, 8)  # Change these numbers

# Change number of products per business
num_products = random.randint(5, 15)  # Change these numbers
```

## Troubleshooting

### Import Errors
Make sure you're in the project root directory and your virtual environment is activated:
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run seeder
python seed_database.py
```

### Database Connection Errors
Check your `.env` file has the correct database credentials:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Duplicate Key Errors
If you run the seeder multiple times, you might get duplicate key errors. Reset the database first:
```bash
python reset_db.py
python seed_database.py
```

## Notes

- All dates are randomized within the last 180 days
- Email addresses are generated based on names (not real emails)
- Phone numbers are randomly generated US format
- All monetary amounts are in USD
- Tax rates vary between 0%, 5%, 8%, and 10%
- Invoice numbers follow the format: INV-1000, INV-1001, etc.
- Payment numbers follow the format: PAY-1000, PAY-1001, etc.
