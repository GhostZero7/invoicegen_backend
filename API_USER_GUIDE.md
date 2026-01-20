# Invoice Generator API - User Guide

> **A simple guide to understanding what you can do with the Invoice Generator API**

---

## 🎯 What Can You Do?

This API allows you to build invoicing applications with features like:

- **User Accounts** - Sign up, log in, and manage user profiles
- **Multiple Businesses** - Manage multiple business profiles under one account
- **Client Management** - Keep track of your customers
- **Product Catalog** - Maintain a list of products/services you sell
- **Invoice Creation** - Generate professional invoices
- **Payment Tracking** - Record and track payments
- **Categories** - Organize your invoices and expenses
- **Subscription Plans** - Different tiers with various limits

---

## 👤 User Accounts

### What You Can Do

**Sign Up & Login**
- Create a new account with email and password
- Log in to get access to your data
- Verify your email address with a code sent to your inbox
- Reset your password if you forget it

**Profile Management**
- Update your name, phone number, and profile picture
- Change your password
- Enable two-factor authentication for extra security

**Account Types**
- **Regular User** - Standard account for business owners
- **Admin** - Special access to manage waitlist and view all data

### Important Notes

- You'll receive a verification email when you sign up
- Your account must be verified before you can use it
- Keep your password secure - it's encrypted in our system

---

## 🏢 Business Profiles

### What You Can Do

**Create Multiple Businesses**
- Set up different business profiles (e.g., one for consulting, one for retail)
- Each business has its own:
  - Business name and contact information
  - Tax ID and registration details
  - Logo and branding
  - Invoice numbering system
  - Default payment terms

**Manage Business Settings**
- Choose your currency (USD, EUR, etc.)
- Set your timezone
- Customize invoice prefixes (e.g., "INV", "ACME")
- Add default payment instructions

### Plan Limits

Different subscription plans allow different numbers of businesses:
- **Basic Plan** - Limited number of businesses
- **Premium Plan** - More businesses allowed
- **Enterprise Plan** - Unlimited businesses

---

## 👥 Client Management

### What You Can Do

**Add Clients**
- Store client information (name, email, phone)
- Track both individual clients and companies
- Add tax IDs and payment terms for each client
- Set credit limits if needed

**Organize Clients**
- Mark clients as active, inactive, or archived
- Add notes about each client
- Filter clients by business, status, or type

**Client Types**
- **Individual** - For personal clients
- **Company** - For business clients

### Why This Matters

Having client information stored makes it easy to:
- Quickly create invoices without re-entering details
- Track which clients owe you money
- See your payment history with each client

---

## 📦 Products & Services

### What You Can Do

**Build Your Catalog**
- Add products or services you offer
- Set prices and costs for each item
- Include descriptions and images
- Assign SKU codes for tracking

**Inventory Management** (Optional)
- Track stock quantities
- Get alerts when stock is low
- Update inventory when items are sold
- View low-stock items at a glance

**Product Details**
- Unit price (what you charge)
- Cost price (what it costs you)
- Tax rate (if taxable)
- Unit of measure (hours, units, kg, etc.)

### Smart Features

- **Duplicate Products** - Copy existing products to create similar ones
- **Stock Operations** - Add, subtract, or set stock levels
- **Active/Inactive** - Hide products without deleting them

---

## 🗂️ Categories

### What You Can Do

**Organize Your Data**
- Create categories for invoices (e.g., "Consulting", "Products", "Services")
- Create categories for expenses (e.g., "Office Supplies", "Travel")
- Build hierarchies with parent and child categories

**Customize Categories**
- Choose colors for visual organization
- Add icons for quick recognition
- Reorder categories by dragging

**Category Types**
- **Invoice Categories** - For organizing invoices
- **Expense Categories** - For organizing expenses

### Example Structure

```
Consulting Services (Parent)
  ├── Web Development
  ├── Mobile Development
  └── UI/UX Design

Products (Parent)
  ├── Software Licenses
  └── Hardware
```

---

## 🧾 Invoices

### What You Can Do

**Create Invoices**
- Select a client and business
- Add multiple line items (products/services)
- Apply discounts (percentage or fixed amount)
- Add tax automatically
- Include shipping costs
- Add notes and payment instructions

**Invoice Lifecycle**
1. **Draft** - Work in progress, not sent yet
2. **Sent** - Sent to client
3. **Viewed** - Client has opened it
4. **Paid** - Payment received
5. **Partially Paid** - Some payment received
6. **Overdue** - Past due date
7. **Cancelled** - Cancelled invoice
8. **Refunded** - Payment refunded

**Manage Invoices**
- View all invoices for a business
- Filter by status, client, or date
- Mark as sent, paid, or cancelled
- Track payment status

**Automatic Calculations**
- Subtotal calculated from line items
- Discounts applied automatically
- Tax calculated per item or total
- Final total computed for you

### Invoice Numbers

Each business has its own invoice numbering:
- Custom prefix (e.g., "INV", "ACME")
- Auto-incrementing numbers (e.g., INV-00001, INV-00002)
- Never duplicates

### Plan Limits

Different plans have monthly invoice limits:
- **Basic** - Limited invoices per month
- **Premium** - More invoices per month
- **Enterprise** - Unlimited invoices

---

## 💰 Payments

### What You Can Do

**Record Payments**
- Link payments to specific invoices
- Record payment date and amount
- Choose payment method (cash, card, bank transfer, etc.)
- Add transaction IDs and reference numbers
- Include notes about the payment

**Payment Methods**
- Cash
- Check
- Bank Transfer
- Credit Card
- Debit Card
- PayPal
- Stripe
- Other

**Automatic Updates**
- Invoice amounts update automatically when you add payments
- Invoices marked as "Paid" when fully paid
- Partial payments tracked accurately

**Payment Management**
- View all payments for an invoice
- Edit payment details if needed
- Delete payments (invoice amounts adjust automatically)
- Process refunds

### Smart Features

When you add a payment:
- Invoice's "Amount Paid" increases
- Invoice's "Amount Due" decreases
- Invoice status changes to "Paid" if fully paid
- Payment number generated automatically

---

## 💳 Billing & Subscriptions

### What You Can Do

**View Available Plans**
- See all subscription tiers
- Compare features and pricing
- Check monthly vs. yearly pricing

**Manage Your Subscription**
- View your current plan
- See your billing period
- Check usage limits
- Know when your subscription renews

### Plan Features

Each plan includes:
- Maximum invoices per month
- Maximum number of businesses
- List of included features
- Monthly and yearly pricing options

### Subscription Status
- **Active** - Currently subscribed
- **Cancelled** - Will expire at period end
- **Expired** - Needs renewal

---

## 📋 Waitlist

### For Public Users

**Join the Waitlist**
- Sign up with your email
- Provide your name and company (optional)
- Add a message about your needs
- See your position in line

**Check Your Status**
- Look up your waitlist entry by email
- See if you've been notified
- Track your position

### For Administrators

**Manage Waitlist**
- View all waitlist entries
- Filter by priority, status, or date
- Mark entries as notified or converted
- Add internal notes
- Set priority levels (Normal, High, VIP)
- Bulk update entries

**Analytics**
- Total signups
- Conversion rate
- Recent signups (last 7 days)
- Notified vs. not notified

---

## 🔐 Security Features

### Authentication
- **JWT Tokens** - Secure token-based authentication
- **Password Hashing** - Passwords are never stored in plain text
- **Email Verification** - Confirm email ownership
- **Two-Factor Authentication** - Optional extra security layer

### Authorization
- **User-Based Access** - You can only see your own data
- **Business Ownership** - Only business owners can modify their businesses
- **Admin Controls** - Special features for administrators

### Data Protection
- All sensitive data is encrypted
- Secure password reset process
- Session management with token expiration

---

## 📊 Common Workflows

### Creating Your First Invoice

1. **Set Up Your Business**
   - Create a business profile
   - Add your logo and contact info
   - Set invoice prefix and payment terms

2. **Add a Client**
   - Enter client details
   - Set payment terms if different from default

3. **Add Products/Services** (Optional)
   - Create items you frequently invoice
   - Set prices and tax rates

4. **Create the Invoice**
   - Select business and client
   - Add line items (from products or custom)
   - Apply discounts if needed
   - Review totals
   - Add notes and payment instructions

5. **Send the Invoice**
   - Mark as "Sent"
   - System records when it was sent

6. **Record Payment**
   - When paid, create a payment record
   - Invoice automatically updates to "Paid"

### Managing Multiple Businesses

1. **Create Business Profiles**
   - One for each business entity
   - Each has separate settings

2. **Organize by Business**
   - Clients belong to specific businesses
   - Products belong to specific businesses
   - Invoices are business-specific

3. **Switch Between Businesses**
   - Filter data by business
   - Each business has its own invoice numbering

### Tracking Inventory

1. **Enable Inventory Tracking**
   - Turn on for products you want to track
   - Set initial stock quantity
   - Set low-stock threshold

2. **Monitor Stock Levels**
   - View current stock
   - Get low-stock alerts
   - See which items need reordering

3. **Update Stock**
   - Add stock when you receive inventory
   - Subtract when you sell items
   - Set exact quantities when doing counts

---

## 🎨 Customization Options

### Business Branding
- Upload your logo
- Set invoice prefix
- Customize payment instructions
- Add default notes to invoices

### Invoice Customization
- Custom invoice numbers
- Flexible payment terms
- Discount options (percentage or fixed)
- Tax rates per item
- Shipping costs
- Footer text

### Category Organization
- Custom colors for visual coding
- Icons for quick identification
- Hierarchical structure
- Custom sort order

---

## 📈 Filtering & Searching

### Find What You Need Quickly

**Invoices**
- Filter by business
- Filter by client
- Filter by status (draft, sent, paid, etc.)
- Paginate through results

**Clients**
- Filter by business
- Filter by status (active, inactive, archived)
- Filter by type (individual or company)
- Search by name or email

**Products**
- Filter by business
- Search by name or SKU
- Show only active products
- Show only low-stock items

**Payments**
- Filter by invoice
- Filter by status
- Filter by date range

**Categories**
- Filter by business
- Filter by type (invoice or expense)
- Show only active categories
- Show only root categories (no parents)

---

## ⚡ Performance Features

### Caching
- Invoice lists are cached for faster loading
- Cache refreshes every 5 minutes
- Reduces database load

### Optimizations
- Efficient database queries
- Bulk operations where possible
- Pagination for large datasets

---

## 🚨 Error Messages You Might See

### Authentication Errors
- **"Not authenticated"** - You need to log in first
- **"Invalid OTP"** - The verification code is wrong or expired
- **"Password not match"** - Wrong password entered

### Authorization Errors
- **"Access denied. Admin privileges required."** - This feature is for admins only
- **"Business not found"** - You don't own this business or it doesn't exist

### Validation Errors
- **"User with this email already exists"** - Email is already registered
- **"Product with this SKU already exists"** - SKU must be unique
- **"Category with this name already exists"** - Name must be unique in context

### Billing Limit Errors
- **"Maximum business profiles reached for your plan"** - Upgrade to create more businesses
- **"Monthly invoice limit reached for your plan"** - Upgrade to create more invoices this month

### Business Logic Errors
- **"Cannot delete category with active subcategories"** - Remove subcategories first
- **"This would create a circular reference"** - Can't make a category its own parent
- **"Account is not active"** - Your account has been suspended

---

## 💡 Tips & Best Practices

### Getting Started
1. **Verify your email** - Do this first to unlock all features
2. **Create your business profile** - Set up your company information
3. **Add a few clients** - Start with your most frequent customers
4. **Create product templates** - For items you invoice regularly
5. **Send your first invoice** - Test the complete workflow

### Organization
- **Use categories** - Makes reporting and organization easier
- **Set default payment terms** - Saves time on each invoice
- **Add product descriptions** - Helps clients understand what they're paying for
- **Include payment instructions** - Makes it easier for clients to pay

### Efficiency
- **Create product templates** - Reuse common items instead of typing each time
- **Use the duplicate feature** - Copy similar products or invoices
- **Set up inventory tracking** - Only for products you need to track
- **Leverage filters** - Find what you need quickly

### Financial Management
- **Record payments promptly** - Keep accurate records
- **Review overdue invoices** - Follow up on late payments
- **Track low stock** - Reorder before you run out
- **Monitor your plan limits** - Upgrade before you hit limits

---

## 🆘 Common Questions

**Q: Can I have multiple businesses under one account?**  
A: Yes! The number depends on your subscription plan.

**Q: What happens if I reach my monthly invoice limit?**  
A: You'll need to upgrade your plan or wait until next month.

**Q: Can I delete an invoice?**  
A: Yes, but it's better to cancel it to maintain records.

**Q: How do I handle partial payments?**  
A: Just record the partial amount - the system tracks it automatically.

**Q: Can I customize my invoice numbers?**  
A: Yes, set a custom prefix for each business. Numbers auto-increment.

**Q: What if I forget my password?**  
A: Use the forgot password feature to reset it via email.

**Q: Can I track inventory for some products but not others?**  
A: Yes, enable inventory tracking per product.

**Q: How do categories work with subcategories?**  
A: Create parent categories, then assign children to them for hierarchy.

**Q: Can I refund a payment?**  
A: Yes, use the refund feature - it updates the invoice automatically.

**Q: Is my data secure?**  
A: Yes, we use encryption, secure authentication, and industry best practices.

---

## 📞 Support

For technical questions or issues:
- Check this guide first
- Review the technical documentation for developers
- Contact your development team
- Report bugs through your issue tracking system

---

**Last Updated:** January 20, 2026  
**Version:** 1.0
