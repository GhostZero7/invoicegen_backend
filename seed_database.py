"""
Database Seeder Script
Populates the database with realistic test data including:
- 10 users (2 admins, 7 accountants, 1 regular user)
- Business profiles for each user
- 30+ clients
- 100+ invoices with items
- Products
- Payments
- Addresses
"""

import random
from datetime import datetime, timedelta, date
from decimal import Decimal
import uuid

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole, UserStatus
from app.db.models.business import BusinessProfile, BusinessType, PaymentTerms
from app.db.models.client import Client, ClientType, ClientStatus, ClientContact
from app.db.models.invoice import Invoice, InvoiceStatus, InvoiceItem, DiscountType
from app.db.models.product import Product
from app.db.models.payment import Payment, PaymentMethod, PaymentStatus
from app.db.models.address import Address, AddressType
from app.db.models.categories import Category
from app.auth.utils import hash_password

# Sample data
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris"
]

COMPANY_NAMES = [
    "Tech Solutions Inc", "Global Consulting Group", "Digital Marketing Pro",
    "Creative Design Studio", "Financial Services Corp", "Healthcare Partners LLC",
    "Construction Builders Co", "Retail Innovations", "Food & Beverage Enterprises",
    "Transportation Logistics", "Real Estate Holdings", "Manufacturing Systems",
    "Education Services", "Legal Associates", "Engineering Solutions",
    "Media Productions", "Software Development Inc", "Cloud Services Ltd",
    "Data Analytics Corp", "Cybersecurity Experts", "Mobile Apps Studio",
    "E-commerce Platform", "Green Energy Solutions", "Fitness & Wellness",
    "Travel & Tourism Co", "Insurance Brokers", "Accounting Firm",
    "Architecture Design", "Interior Decorators", "Event Planning Services"
]

PRODUCT_NAMES = [
    "Web Development", "Mobile App Development", "UI/UX Design", "SEO Optimization",
    "Content Writing", "Social Media Management", "Brand Strategy", "Logo Design",
    "Video Production", "Photography Services", "Consulting Hours", "Training Session",
    "Software License", "Cloud Hosting", "Database Management", "API Integration",
    "Security Audit", "Performance Optimization", "Technical Support", "Maintenance Package"
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle"
]

STATES = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "NC", "WA"]

STREETS = [
    "Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine Rd", "Elm St",
    "Washington Blvd", "Park Ave", "Broadway", "Market St", "Church St", "Spring St"
]


def random_date(start_days_ago: int, end_days_ago: int = 0) -> date:
    """Generate a random date between start_days_ago and end_days_ago"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).date()


def random_datetime(start_days_ago: int, end_days_ago: int = 0) -> datetime:
    """Generate a random datetime between start_days_ago and end_days_ago"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def create_users(db: Session) -> list[User]:
    """Create 10 users: 2 admins, 7 accountants, 1 regular user"""
    users = []
    
    # Create 2 admins
    for i in range(2):
        user = User(
            id=str(uuid.uuid4()),
            email=f"admin{i+1}@invoicegen.com",
            password_hash=hash_password("Admin123!"),
            first_name=random.choice(FIRST_NAMES),
            last_name=random.choice(LAST_NAMES),
            phone=f"+1{random.randint(2000000000, 9999999999)}",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            email_verified=True,
            created_at=random_datetime(180, 150),
            updated_at=datetime.utcnow()
        )
        users.append(user)
        db.add(user)
    
    # Create 7 accountants
    for i in range(7):
        user = User(
            id=str(uuid.uuid4()),
            email=f"accountant{i+1}@invoicegen.com",
            password_hash=hash_password("Account123!"),
            first_name=random.choice(FIRST_NAMES),
            last_name=random.choice(LAST_NAMES),
            phone=f"+1{random.randint(2000000000, 9999999999)}",
            role=UserRole.ACCOUNTANT,
            status=UserStatus.ACTIVE,
            email_verified=True,
            created_at=random_datetime(150, 100),
            updated_at=datetime.utcnow()
        )
        users.append(user)
        db.add(user)
    
    # Create 1 regular user
    user = User(
        id=str(uuid.uuid4()),
        email="user@invoicegen.com",
        password_hash=hash_password("User123!"),
        first_name=random.choice(FIRST_NAMES),
        last_name=random.choice(LAST_NAMES),
        phone=f"+1{random.randint(2000000000, 9999999999)}",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        email_verified=True,
        created_at=random_datetime(100, 80),
        updated_at=datetime.utcnow()
    )
    users.append(user)
    db.add(user)
    
    db.commit()
    print(f"✓ Created {len(users)} users")
    return users


def create_business_profiles(db: Session, users: list[User]) -> list[BusinessProfile]:
    """Create business profiles for each user"""
    businesses = []
    
    for user in users:
        business = BusinessProfile(
            id=str(uuid.uuid4()),
            user_id=user.id,
            business_name=f"{user.first_name} {user.last_name} {random.choice(['LLC', 'Inc', 'Corp', 'Co'])}",
            business_type=random.choice(list(BusinessType)),
            tax_id=f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
            email=user.email,
            phone=user.phone,
            currency="USD",
            invoice_prefix="INV",
            quote_prefix="QUO",
            next_invoice_number=random.randint(1000, 2000),
            next_quote_number=random.randint(100, 500),
            payment_terms_default=random.choice(list(PaymentTerms)),
            is_active=True,
            created_at=user.created_at.date() if isinstance(user.created_at, datetime) else user.created_at,
            updated_at=datetime.utcnow().date()
        )
        businesses.append(business)
        db.add(business)
        
        # Add business address
        address = Address(
            id=str(uuid.uuid4()),
            addressable_type="business_profile",
            addressable_id=business.id,
            address_type=AddressType.BUSINESS,
            street_line_1=f"{random.randint(100, 9999)} {random.choice(STREETS)}",
            city=random.choice(CITIES),
            state_province=random.choice(STATES),
            postal_code=f"{random.randint(10000, 99999)}",
            country="US",
            is_default=True
        )
        db.add(address)
    
    db.commit()
    print(f"✓ Created {len(businesses)} business profiles with addresses")
    return businesses


def create_categories(db: Session, businesses: list[BusinessProfile]) -> list[Category]:
    """Create categories for businesses"""
    categories = []
    category_names = ["Consulting", "Development", "Design", "Marketing", "Support", "Training"]
    
    from app.db.models.categories import CategoryType
    
    for business in businesses[:5]:  # Create categories for first 5 businesses
        for cat_name in category_names:
            category = Category(
                id=str(uuid.uuid4()),
                business_id=business.id,
                name=cat_name,
                description=f"{cat_name} services and products",
                color=f"#{random.randint(0, 0xFFFFFF):06x}",
                category_type=CategoryType.INVOICE,
                is_active=True
            )
            categories.append(category)
            db.add(category)
    
    db.commit()
    print(f"✓ Created {len(categories)} categories")
    return categories


def create_products(db: Session, businesses: list[BusinessProfile], categories: list[Category]) -> list[Product]:
    """Create products for businesses"""
    products = []
    
    for business in businesses:
        business_categories = [c for c in categories if c.business_id == business.id]
        num_products = random.randint(5, 15)
        for i in range(num_products):
            product = Product(
                id=str(uuid.uuid4()),
                business_id=business.id,
                sku=f"SKU-{random.randint(10000, 99999)}",
                name=random.choice(PRODUCT_NAMES),
                description=f"Professional {random.choice(PRODUCT_NAMES).lower()} service",
                unit_price=round(random.uniform(50, 500), 2),
                cost_price=round(random.uniform(20, 200), 2),
                unit_of_measure=random.choice(["hour", "unit", "day", "project"]),
                tax_rate=random.choice([0, 5, 8, 10]),
                is_taxable=True,
                track_inventory=random.choice([True, False]),
                quantity_in_stock=random.randint(0, 100) if random.choice([True, False]) else 0,
                is_active=True,
                created_at=random_date(120, 30),
                updated_at=datetime.utcnow().date()
            )
            products.append(product)
            db.add(product)
    
    db.commit()
    print(f"✓ Created {len(products)} products")
    return products


def create_clients(db: Session, businesses: list[BusinessProfile]) -> list[Client]:
    """Create 30+ clients"""
    clients = []
    
    for business in businesses:
        num_clients = random.randint(3, 8)
        for i in range(num_clients):
            is_company = random.choice([True, False])
            
            if is_company:
                company_name = random.choice(COMPANY_NAMES)
                first_name = None
                last_name = None
                email = f"contact@{company_name.lower().replace(' ', '')}.com"
            else:
                company_name = None
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                email = f"{first_name.lower()}.{last_name.lower()}@email.com"
            
            client = Client(
                id=str(uuid.uuid4()),
                business_id=business.id,
                client_type=ClientType.COMPANY if is_company else ClientType.INDIVIDUAL,
                company_name=company_name,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=f"+1{random.randint(2000000000, 9999999999)}",
                mobile=f"+1{random.randint(2000000000, 9999999999)}",
                payment_terms=random.choice(["net_15", "net_30", "net_60"]),
                currency="USD",
                status=ClientStatus.ACTIVE,
                created_at=random_date(150, 30),
                updated_at=datetime.utcnow().date()
            )
            clients.append(client)
            db.add(client)
            
            # Add client address
            address = Address(
                id=str(uuid.uuid4()),
                addressable_type="client",
                addressable_id=client.id,
                address_type=AddressType.BILLING,
                street_line_1=f"{random.randint(100, 9999)} {random.choice(STREETS)}",
                city=random.choice(CITIES),
                state_province=random.choice(STATES),
                postal_code=f"{random.randint(10000, 99999)}",
                country="US",
                is_default=True
            )
            db.add(address)
            
            # Add contact person for companies
            if is_company:
                contact = ClientContact(
                    id=str(uuid.uuid4()),
                    client_id=client.id,
                    first_name=random.choice(FIRST_NAMES),
                    last_name=random.choice(LAST_NAMES),
                    email=f"contact@{company_name.lower().replace(' ', '')}.com",
                    phone=f"+1{random.randint(2000000000, 9999999999)}",
                    position=random.choice(["CEO", "CFO", "Manager", "Director", "Accountant"]),
                    is_primary=True
                )
                db.add(contact)
    
    db.commit()
    print(f"✓ Created {len(clients)} clients with addresses and contacts")
    return clients


def create_invoices(db: Session, businesses: list[BusinessProfile], clients: list[Client], 
                   products: list[Product], users: list[User], categories: list[Category]) -> list[Invoice]:
    """Create 100+ invoices with items"""
    invoices = []
    
    for business in businesses:
        business_clients = [c for c in clients if c.business_id == business.id]
        business_products = [p for p in products if p.business_id == business.id]
        business_categories = [c for c in categories if c.business_id == business.id]
        
        if not business_clients or not business_products:
            continue
        
        num_invoices = random.randint(10, 15)
        
        for i in range(num_invoices):
            invoice_date = random_date(180, 0)
            due_date = invoice_date + timedelta(days=random.choice([15, 30, 60]))
            
            status = random.choices(
                list(InvoiceStatus),
                weights=[5, 20, 10, 40, 15, 5, 5]  # More paid invoices
            )[0]
            
            invoice = Invoice(
                id=str(uuid.uuid4()),
                business_id=business.id,
                client_id=random.choice(business_clients).id,
                category_id=random.choice(business_categories).id if business_categories else None,
                invoice_number=f"{business.invoice_prefix}-{business.next_invoice_number + i}",
                reference_number=f"REF-{random.randint(10000, 99999)}" if random.choice([True, False]) else None,
                status=status,
                invoice_date=invoice_date,
                due_date=due_date,
                payment_terms=random.choice(list(PaymentTerms)),
                subtotal=0,  # Will calculate
                discount_type=random.choice([None, DiscountType.PERCENTAGE, DiscountType.FIXED]),
                discount_value=random.uniform(0, 20) if random.choice([True, False]) else 0,
                discount_amount=0,  # Will calculate
                tax_amount=0,  # Will calculate
                shipping_amount=round(random.uniform(0, 50), 2) if random.choice([True, False]) else 0,
                total_amount=0,  # Will calculate
                amount_paid=0,  # Will set later
                amount_due=0,  # Will calculate
                currency="USD",
                notes=f"Thank you for your business!" if random.choice([True, False]) else None,
                created_by=users[0].id,  # First user
                created_at=random_datetime(180, 0),
                updated_at=datetime.utcnow()
            )
            
            if status == InvoiceStatus.SENT:
                invoice.sent_at = random_datetime(180, 0)
            elif status == InvoiceStatus.VIEWED:
                invoice.sent_at = random_datetime(180, 0)
                invoice.viewed_at = random_datetime(170, 0)
            elif status == InvoiceStatus.PAID:
                invoice.sent_at = random_datetime(180, 0)
                invoice.viewed_at = random_datetime(170, 0)
                invoice.paid_at = random_datetime(160, 0)
            
            db.add(invoice)
            invoices.append(invoice)
            
            # Add invoice items
            num_items = random.randint(1, 5)
            subtotal = 0
            tax_total = 0
            
            for j in range(num_items):
                product = random.choice(business_products)
                quantity = random.randint(1, 10)
                unit_price = product.unit_price
                line_subtotal = quantity * unit_price
                
                item_discount_value = 0
                item_discount_amount = 0
                if random.choice([True, False]):
                    item_discount_value = random.uniform(5, 15)
                    item_discount_amount = round(line_subtotal * (item_discount_value / 100), 2)
                
                line_after_discount = line_subtotal - item_discount_amount
                item_tax_amount = round(line_after_discount * (product.tax_rate / 100), 2)
                line_total = line_after_discount + item_tax_amount
                
                item = InvoiceItem(
                    id=str(uuid.uuid4()),
                    invoice_id=invoice.id,
                    product_id=product.id,
                    description=product.name,
                    quantity=quantity,
                    unit_price=unit_price,
                    unit_of_measure=product.unit_of_measure,
                    tax_rate=product.tax_rate,
                    tax_amount=item_tax_amount,
                    discount_type=DiscountType.PERCENTAGE if item_discount_value > 0 else None,
                    discount_value=item_discount_value,
                    discount_amount=item_discount_amount,
                    line_total=line_total,
                    sort_order=j
                )
                db.add(item)
                
                subtotal += line_subtotal
                tax_total += item_tax_amount
            
            # Calculate invoice totals
            invoice.subtotal = round(subtotal, 2)
            
            if invoice.discount_type == DiscountType.PERCENTAGE:
                invoice.discount_amount = round(subtotal * (invoice.discount_value / 100), 2)
            elif invoice.discount_type == DiscountType.FIXED:
                invoice.discount_amount = round(invoice.discount_value, 2)
            
            invoice.tax_amount = round(tax_total, 2)
            invoice.total_amount = round(
                subtotal - invoice.discount_amount + invoice.tax_amount + invoice.shipping_amount, 2
            )
            invoice.amount_due = invoice.total_amount
    
    db.commit()
    print(f"✓ Created {len(invoices)} invoices with items")
    return invoices


def create_payments(db: Session, invoices: list[Invoice], users: list[User]):
    """Create payments for paid invoices"""
    payments = []
    payment_counter = 1000
    
    for invoice in invoices:
        if invoice.status == InvoiceStatus.PAID:
            # Full payment
            payment = Payment(
                id=str(uuid.uuid4()),
                invoice_id=invoice.id,
                payment_number=f"PAY-{payment_counter}",
                payment_date=invoice.paid_at.date() if invoice.paid_at else datetime.utcnow().date(),
                amount=invoice.total_amount,
                payment_method=random.choice(list(PaymentMethod)),
                transaction_id=f"TXN-{random.randint(100000, 999999)}",
                status=PaymentStatus.COMPLETED,
                created_by=users[0].id,
                created_at=invoice.paid_at if invoice.paid_at else datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            invoice.amount_paid = invoice.total_amount
            invoice.amount_due = 0
            payments.append(payment)
            db.add(payment)
            payment_counter += 1
        
        elif random.choice([True, False]) and invoice.status in [InvoiceStatus.SENT, InvoiceStatus.VIEWED]:
            # Partial payment
            partial_amount = round(invoice.total_amount * random.uniform(0.3, 0.7), 2)
            payment = Payment(
                id=str(uuid.uuid4()),
                invoice_id=invoice.id,
                payment_number=f"PAY-{payment_counter}",
                payment_date=random_date(90, 0),
                amount=partial_amount,
                payment_method=random.choice(list(PaymentMethod)),
                transaction_id=f"TXN-{random.randint(100000, 999999)}",
                status=PaymentStatus.COMPLETED,
                created_by=users[0].id,
                created_at=random_datetime(90, 0),
                updated_at=datetime.utcnow()
            )
            invoice.amount_paid = partial_amount
            invoice.amount_due = invoice.total_amount - partial_amount
            payments.append(payment)
            db.add(payment)
            payment_counter += 1
    
    db.commit()
    print(f"✓ Created {len(payments)} payments")
    return payments


def seed_database():
    """Main seeding function"""
    print("\n🌱 Starting database seeding...\n")
    
    db = SessionLocal()
    
    try:
        # Create all data
        users = create_users(db)
        businesses = create_business_profiles(db, users)
        categories = create_categories(db, businesses)
        products = create_products(db, businesses, categories)
        clients = create_clients(db, businesses)
        invoices = create_invoices(db, businesses, clients, products, users, categories)
        payments = create_payments(db, invoices, users)
        
        print("\n✅ Database seeding completed successfully!")
        print(f"\nSummary:")
        print(f"  - Users: {len(users)} (2 admins, 7 accountants, 1 user)")
        print(f"  - Business Profiles: {len(businesses)}")
        print(f"  - Categories: {len(categories)}")
        print(f"  - Products: {len(products)}")
        print(f"  - Clients: {len(clients)}")
        print(f"  - Invoices: {len(invoices)}")
        print(f"  - Payments: {len(payments)}")
        print(f"\nLogin credentials:")
        print(f"  Admin: admin1@invoicegen.com / Admin123!")
        print(f"  Accountant: accountant1@invoicegen.com / Account123!")
        print(f"  User: user@invoicegen.com / User123!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
