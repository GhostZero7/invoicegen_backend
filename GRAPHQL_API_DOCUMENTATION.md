# GraphQL API Documentation - Frontend Integration Guide

> **Last Updated:** 2026-01-20  
> **Status:** ✅ Ready for Frontend Integration

This document provides comprehensive documentation for all GraphQL mutations and queries available in the Invoice Generator backend, ready for frontend integration.

---

## Table of Contents

- [Authentication](#authentication)
- [User Management](#user-management)
- [Business Profiles](#business-profiles)
- [Clients](#clients)
- [Products](#products)
- [Categories](#categories)
- [Invoices](#invoices)
- [Payments](#payments)
- [Billing & Subscriptions](#billing--subscriptions)
- [Waitlist](#waitlist)
- [Common Types & Enums](#common-types--enums)

---

## Authentication

### Mutations

#### `login`
**Description:** Authenticate a user and receive an access token.

**Input:**
```graphql
input LoginUserInput {
  email: String!
  password: String!
}
```

**Returns:** `Auth`
```graphql
type Auth {
  token: String!
  user: User
  message: String!
  is_verified: Boolean!
}
```

**Behavior:**
- If email is not verified, sends a verification email and returns `is_verified: false`
- If account is not active, throws an exception
- On success, returns JWT token and user data

**Example:**
```graphql
mutation Login {
  login(input: {
    email: "user@example.com"
    password: "securePassword123"
  }) {
    token
    message
    is_verified
    user {
      id
      email
      first_name
      last_name
    }
  }
}
```

---

#### `verifyEmail`
**Description:** Verify user email with OTP code.

**Input:**
- `email: String!`
- `otp_: String!`

**Returns:** `Boolean`

**Example:**
```graphql
mutation VerifyEmail {
  verifyEmail(email: "user@example.com", otp_: "123456")
}
```

---

#### `sendOTP`
**Description:** Resend OTP verification code to user's email.

**Input:**
- `email: String!`

**Returns:** `Auth`

**Example:**
```graphql
mutation SendOTP {
  sendOTP(email: "user@example.com") {
    message
    is_verified
  }
}
```

---

#### `forgotPassword`
**Description:** Initiate password reset process.

**Input:**
```graphql
input ForgotPasswordInput {
  email: String!
}
```

**Returns:** `ForgotPassword`

> ⚠️ **Note:** This mutation is currently not implemented (placeholder).

---

## User Management

### Queries

#### `me`
**Description:** Get current authenticated user's profile.

**Authentication:** Required

**Returns:** `User`

**Example:**
```graphql
query Me {
  me {
    id
    email
    first_name
    last_name
    phone
    avatar_url
    email_verified
    two_factor_enabled
    role
    status
    last_login_at
    created_at
  }
}
```

---

#### `user`
**Description:** Get user by ID.

**Input:**
- `id: ID!`

**Returns:** `User`

**Example:**
```graphql
query GetUser {
  user(id: "user-uuid") {
    id
    email
    first_name
    last_name
  }
}
```

---

#### `users`
**Description:** Get list of users with optional filters.

**Input:**
- `skip: Int = 0`
- `limit: Int = 10`
- `role: UserRole` (optional)
- `status: UserStatus` (optional)

**Returns:** `[User]`

**Example:**
```graphql
query ListUsers {
  users(skip: 0, limit: 20, role: ADMIN) {
    id
    email
    first_name
    last_name
    role
    status
  }
}
```

---

### Mutations

#### `createUser`
**Description:** Create a new user account.

**Input:**
```graphql
input CreateUserInput {
  email: String!
  password: String!
  first_name: String!
  last_name: String!
  phone: String
  role: UserRole
}
```

**Returns:** `User`

**Behavior:**
- Automatically sends verification email with OTP
- Password is hashed before storage
- Default role is "user" if not specified

**Example:**
```graphql
mutation CreateUser {
  createUser(input: {
    email: "newuser@example.com"
    password: "SecurePass123!"
    first_name: "John"
    last_name: "Doe"
    phone: "+1234567890"
  }) {
    id
    email
    first_name
    last_name
  }
}
```

---

#### `updateUser`
**Description:** Update user information.

**Input:**
```graphql
input UpdateUserInput {
  first_name: String
  last_name: String
  phone: String
  avatar_url: String
  role: UserRole
  status: UserStatus
}
```

**Returns:** `User`

**Example:**
```graphql
mutation UpdateUser {
  updateUser(id: "user-uuid", input: {
    first_name: "Jane"
    phone: "+9876543210"
  }) {
    id
    first_name
    phone
  }
}
```

---

#### `updatePassword`
**Description:** Update user password (requires current password).

**Authentication:** Required

**Input:**
```graphql
input UpdatePasswordInput {
  current_password: String!
  new_password: String!
}
```

**Returns:** `Boolean`

**Example:**
```graphql
mutation UpdatePassword {
  updatePassword(input: {
    current_password: "OldPass123"
    new_password: "NewSecurePass456!"
  })
}
```

---

#### `deleteUser`
**Description:** Soft delete a user (sets status to DELETED).

**Input:**
- `id: ID!`

**Returns:** `Boolean`

---

#### `enableTwoFactor`
**Description:** Enable two-factor authentication for current user.

**Authentication:** Required

**Returns:** `String` (TOTP secret for QR code generation)

**Example:**
```graphql
mutation EnableTwoFactor {
  enableTwoFactor
}
```

---

#### `disableTwoFactor`
**Description:** Disable two-factor authentication.

**Authentication:** Required

**Input:**
- `code: String!` (TOTP verification code)

**Returns:** `Boolean`

---

## Business Profiles

### Queries

#### `myBusinesses`
**Description:** Get all businesses owned by the current user.

**Authentication:** Required

**Returns:** `[BusinessProfile]`

**Example:**
```graphql
query MyBusinesses {
  myBusinesses {
    id
    business_name
    business_type
    email
    phone
    currency
    invoice_prefix
    next_invoice_number
    is_active
  }
}
```

---

#### `business`
**Description:** Get a specific business by ID.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `BusinessProfile`

**Example:**
```graphql
query GetBusiness {
  business(id: "business-uuid") {
    id
    business_name
    business_type
    tax_id
    email
    phone
    website
    logo_url
    currency
    timezone
    payment_terms_default
    payment_instructions
  }
}
```

---

#### `businesses`
**Description:** Get all businesses (paginated).

**Authentication:** Required

**Input:**
- `skip: Int = 0`
- `limit: Int = 10`

**Returns:** `[BusinessProfile]`

---

### Mutations

#### `createBusiness`
**Description:** Create a new business profile.

**Authentication:** Required

**Input:**
```graphql
input CreateBusinessInput {
  business_name: String!
  business_type: BusinessType!
  tax_id: String
  email: String!
  phone: String!
  currency: String
  invoice_prefix: String
}
```

**Returns:** `BusinessProfile`

**Billing Limits:** Checks if user can create more businesses based on their plan.

**Example:**
```graphql
mutation CreateBusiness {
  createBusiness(input: {
    business_name: "Acme Corp"
    business_type: COMPANY
    tax_id: "123-45-6789"
    email: "billing@acme.com"
    phone: "+1234567890"
    currency: "USD"
    invoice_prefix: "ACME"
  }) {
    id
    business_name
    invoice_prefix
    next_invoice_number
  }
}
```

---

#### `updateBusiness`
**Description:** Update an existing business profile.

**Authentication:** Required

**Input:**
```graphql
input UpdateBusinessInput {
  business_name: String
  business_type: BusinessType
  tax_id: String
  vat_number: String
  website: String
  phone: String
  email: String
  logo_url: String
  currency: String
  timezone: String
  payment_terms_default: PaymentTerms
  notes_default: String
  payment_instructions: String
  is_active: Boolean
}
```

**Returns:** `BusinessProfile`

**Example:**
```graphql
mutation UpdateBusiness {
  updateBusiness(id: "business-uuid", input: {
    website: "https://acme.com"
    logo_url: "https://cdn.acme.com/logo.png"
    payment_instructions: "Wire transfer to account #12345"
  }) {
    id
    website
    logo_url
    payment_instructions
  }
}
```

---

#### `deleteBusiness`
**Description:** Delete a business profile.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

---

## Clients

### Queries

#### `client`
**Description:** Get a specific client by ID.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Client`

**Example:**
```graphql
query GetClient {
  client(id: "client-uuid") {
    id
    business_id
    client_type
    company_name
    first_name
    last_name
    email
    phone
    mobile
    website
    tax_id
    payment_terms
    status
  }
}
```

---

#### `clients`
**Description:** Get clients with optional filters.

**Authentication:** Required

**Input:**
- `business_id: ID` (optional)
- `skip: Int = 0`
- `limit: Int = 10`
- `status: ClientStatus` (optional)
- `client_type: ClientType` (optional)

**Returns:** `[Client]`

**Example:**
```graphql
query ListClients {
  clients(business_id: "business-uuid", status: ACTIVE, limit: 50) {
    id
    company_name
    first_name
    last_name
    email
    phone
    status
  }
}
```

---

### Mutations

#### `createClient`
**Description:** Create a new client.

**Authentication:** Required

**Input:**
```graphql
input CreateClientInput {
  business_id: ID!
  client_type: ClientType!
  company_name: String
  first_name: String
  last_name: String
  email: String!
  phone: String
  mobile: String
  website: String
  tax_id: String
  payment_terms: Int
  currency: String
}
```

**Returns:** `Client`

**Example:**
```graphql
mutation CreateClient {
  createClient(input: {
    business_id: "business-uuid"
    client_type: COMPANY
    company_name: "Client Corp"
    email: "contact@clientcorp.com"
    phone: "+1234567890"
    payment_terms: 30
    currency: "USD"
  }) {
    id
    company_name
    email
    status
  }
}
```

---

#### `updateClient`
**Description:** Update an existing client.

**Authentication:** Required

**Input:**
```graphql
input UpdateClientInput {
  company_name: String
  first_name: String
  last_name: String
  email: String
  phone: String
  mobile: String
  website: String
  tax_id: String
  vat_number: String
  payment_terms: Int
  credit_limit: Float
  notes: String
  status: ClientStatus
}
```

**Returns:** `Client`

---

#### `deleteClient`
**Description:** Delete a client.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

---

## Products

### Queries

#### `product`
**Description:** Get product by ID.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Product`

**Example:**
```graphql
query GetProduct {
  product(id: "product-uuid") {
    id
    business_id
    sku
    name
    description
    unit_price
    cost_price
    unit_of_measure
    tax_rate
    is_taxable
    track_inventory
    quantity_in_stock
    low_stock_threshold
    is_active
  }
}
```

---

#### `products`
**Description:** Get list of products with optional filters.

**Authentication:** Required

**Input:**
```graphql
input ProductFilterInput {
  business_id: ID
  name: String
  sku: String
  is_active: Boolean
  track_inventory: Boolean
  low_stock_only: Boolean
}
```
- `filter: ProductFilterInput` (optional)
- `skip: Int = 0`
- `limit: Int = 10`

**Returns:** `[Product]`

**Example:**
```graphql
query ListProducts {
  products(filter: {
    business_id: "business-uuid"
    is_active: true
  }, limit: 100) {
    id
    sku
    name
    unit_price
    quantity_in_stock
  }
}
```

---

#### `productsByBusiness`
**Description:** Get products for a specific business.

**Authentication:** Required

**Input:**
- `business_id: ID!`
- `skip: Int = 0`
- `limit: Int = 10`
- `active_only: Boolean = true`

**Returns:** `[Product]`

---

#### `lowStockProducts`
**Description:** Get products that are low in stock.

**Authentication:** Required

**Input:**
- `business_id: ID` (optional)

**Returns:** `[Product]`

**Example:**
```graphql
query LowStockProducts {
  lowStockProducts(business_id: "business-uuid") {
    id
    name
    sku
    quantity_in_stock
    low_stock_threshold
  }
}
```

---

### Mutations

#### `createProduct`
**Description:** Create a new product.

**Authentication:** Required

**Input:**
```graphql
input CreateProductInput {
  business_id: ID!
  sku: String
  name: String!
  description: String
  unit_price: Float!
  cost_price: Float
  unit_of_measure: String
  tax_rate: Float
  is_taxable: Boolean
  track_inventory: Boolean
  quantity_in_stock: Int
  low_stock_threshold: Int
  image_url: String
}
```

**Returns:** `Product`

**Validation:**
- SKU must be unique within the business (if provided)

**Example:**
```graphql
mutation CreateProduct {
  createProduct(input: {
    business_id: "business-uuid"
    sku: "PROD-001"
    name: "Premium Widget"
    description: "High-quality widget"
    unit_price: 99.99
    cost_price: 45.00
    unit_of_measure: "unit"
    tax_rate: 10.0
    is_taxable: true
    track_inventory: true
    quantity_in_stock: 100
    low_stock_threshold: 10
  }) {
    id
    sku
    name
    unit_price
  }
}
```

---

#### `updateProduct`
**Description:** Update an existing product.

**Authentication:** Required

**Input:**
```graphql
input UpdateProductInput {
  sku: String
  name: String
  description: String
  unit_price: Float
  cost_price: Float
  unit_of_measure: String
  tax_rate: Float
  is_taxable: Boolean
  track_inventory: Boolean
  quantity_in_stock: Int
  low_stock_threshold: Int
  image_url: String
  is_active: Boolean
}
```

**Returns:** `Product`

---

#### `deleteProduct`
**Description:** Soft delete a product (sets is_active to False).

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

---

#### `updateProductStock`
**Description:** Update product stock quantity.

**Authentication:** Required

**Input:**
- `id: ID!`
- `quantity: Int!`
- `operation: String = "set"` (options: "set", "add", "subtract")

**Returns:** `Product`

**Example:**
```graphql
mutation UpdateStock {
  updateProductStock(
    id: "product-uuid"
    quantity: 50
    operation: "add"
  ) {
    id
    quantity_in_stock
  }
}
```

---

#### `duplicateProduct`
**Description:** Duplicate an existing product.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Product`

**Behavior:**
- Creates a copy with "(Copy)" appended to name
- Clears SKU to avoid conflicts
- Sets quantity_in_stock to 0

---

## Categories

### Queries

#### `category`
**Description:** Get category by ID.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Category`

---

#### `categories`
**Description:** Get list of categories with optional filters.

**Authentication:** Required

**Input:**
```graphql
input CategoryFilterInput {
  business_id: ID
  category_type: CategoryType
  parent_id: ID
  is_active: Boolean
  name: String
}
```
- `filter: CategoryFilterInput` (optional)
- `skip: Int = 0`
- `limit: Int = 50`

**Returns:** `[Category]`

**Example:**
```graphql
query ListCategories {
  categories(filter: {
    business_id: "business-uuid"
    category_type: INVOICE
    is_active: true
  }) {
    id
    name
    description
    color
    icon
    parent_id
    category_type
    sort_order
  }
}
```

---

#### `categoriesByBusiness`
**Description:** Get categories for a specific business.

**Authentication:** Required

**Input:**
- `business_id: ID!`
- `category_type: CategoryType` (optional)
- `active_only: Boolean = true`
- `root_only: Boolean = false`

**Returns:** `[Category]`

---

#### `categoryTree`
**Description:** Get hierarchical category tree for a business.

**Authentication:** Required

**Input:**
- `business_id: ID!`
- `category_type: CategoryType` (optional)

**Returns:** `[Category]` (root categories with subcategories)

**Example:**
```graphql
query CategoryTree {
  categoryTree(business_id: "business-uuid", category_type: INVOICE) {
    id
    name
    subcategories {
      id
      name
    }
  }
}
```

---

### Mutations

#### `createCategory`
**Description:** Create a new category.

**Authentication:** Required

**Input:**
```graphql
input CreateCategoryInput {
  business_id: ID!
  name: String!
  description: String
  color: String
  icon: String
  parent_id: ID
  category_type: CategoryType!
  sort_order: Int
}
```

**Returns:** `Category`

**Validation:**
- Parent and child must have same category_type
- Name must be unique within business, type, and parent context

**Example:**
```graphql
mutation CreateCategory {
  createCategory(input: {
    business_id: "business-uuid"
    name: "Consulting Services"
    description: "Professional consulting"
    color: "#3B82F6"
    icon: "briefcase"
    category_type: INVOICE
    sort_order: 1
  }) {
    id
    name
    color
    icon
  }
}
```

---

#### `updateCategory`
**Description:** Update an existing category.

**Authentication:** Required

**Input:**
```graphql
input UpdateCategoryInput {
  name: String
  description: String
  color: String
  icon: String
  parent_id: ID
  is_active: Boolean
  sort_order: Int
}
```

**Returns:** `Category`

**Validation:**
- Prevents circular references
- Ensures parent/child type consistency

---

#### `deleteCategory`
**Description:** Delete a category (soft delete if in use).

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

**Behavior:**
- Cannot delete if has active subcategories
- Soft deletes if used by invoices/expenses
- Hard deletes if not in use

---

#### `reorderCategories`
**Description:** Reorder categories by updating their sort_order.

**Authentication:** Required

**Input:**
- `category_ids: [ID!]!`

**Returns:** `[Category]`

**Example:**
```graphql
mutation ReorderCategories {
  reorderCategories(category_ids: ["cat-1", "cat-2", "cat-3"]) {
    id
    name
    sort_order
  }
}
```

---

## Invoices

### Queries

#### `invoice`
**Description:** Get a specific invoice by ID.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Invoice`

**Example:**
```graphql
query GetInvoice {
  invoice(id: "invoice-uuid") {
    id
    business_id
    client_id
    client {
      id
      company_name
      email
    }
    invoice_number
    status
    invoice_date
    due_date
    payment_terms
    subtotal
    tax_amount
    total_amount
    amount_paid
    amount_due
    currency
    notes
  }
}
```

---

#### `invoices`
**Description:** Get invoices with optional filters.

**Authentication:** Required

**Input:**
- `business_id: ID` (optional)
- `client_id: ID` (optional)
- `status: InvoiceStatus` (optional)
- `skip: Int = 0`
- `limit: Int = 10`

**Returns:** `[Invoice]`

**Features:**
- Redis caching (300s TTL)
- Optimized client fetching (N+1 prevention)
- Ordered by created_at DESC

**Example:**
```graphql
query ListInvoices {
  invoices(
    business_id: "business-uuid"
    status: SENT
    limit: 20
  ) {
    id
    invoice_number
    client {
      company_name
    }
    total_amount
    amount_due
    status
    due_date
  }
}
```

---

#### `invoiceItems`
**Description:** Get all items for a specific invoice.

**Authentication:** Required

**Input:**
- `invoice_id: ID!`

**Returns:** `[InvoiceItem]`

**Example:**
```graphql
query InvoiceItems {
  invoiceItems(invoice_id: "invoice-uuid") {
    id
    description
    quantity
    unit_price
    tax_rate
    discount_amount
    line_total
  }
}
```

---

### Mutations

#### `createInvoice`
**Description:** Create a new invoice with items.

**Authentication:** Required

**Input:**
```graphql
input CreateInvoiceInput {
  business_id: ID!
  client_id: ID!
  invoice_date: DateTime!
  due_date: DateTime!
  payment_terms: String
  discount_type: DiscountType
  discount_value: Float
  shipping_amount: Float
  notes: String
  payment_instructions: String
  items: [InvoiceItemInput!]!
}

input InvoiceItemInput {
  product_id: ID
  description: String!
  quantity: Float!
  unit_price: Float!
  unit_of_measure: String
  tax_rate: Float
  discount_type: DiscountType
  discount_value: Float
}
```

**Returns:** `Invoice`

**Billing Limits:** Checks monthly invoice limit based on plan.

**Behavior:**
- Auto-generates invoice number with business prefix
- Calculates all totals automatically
- Creates invoice items in transaction

**Example:**
```graphql
mutation CreateInvoice {
  createInvoice(input: {
    business_id: "business-uuid"
    client_id: "client-uuid"
    invoice_date: "2026-01-20T00:00:00Z"
    due_date: "2026-02-20T00:00:00Z"
    payment_terms: "Net 30"
    items: [
      {
        description: "Consulting Services"
        quantity: 10
        unit_price: 150.00
        unit_of_measure: "hours"
        tax_rate: 10.0
      }
    ]
  }) {
    id
    invoice_number
    total_amount
    status
  }
}
```

---

#### `updateInvoice`
**Description:** Update an existing invoice.

**Authentication:** Required

**Input:**
```graphql
input UpdateInvoiceInput {
  status: InvoiceStatus
  due_date: DateTime
  notes: String
  payment_instructions: String
}
```

**Returns:** `Invoice`

---

#### `deleteInvoice`
**Description:** Delete an invoice.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

---

#### `sendInvoice`
**Description:** Mark invoice as sent.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

**Behavior:**
- Sets status to "sent"
- Records sent_at timestamp

---

#### `markInvoiceAsPaid`
**Description:** Mark invoice as paid.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

**Behavior:**
- Sets status to "paid"
- Sets amount_paid = total_amount
- Sets amount_due = 0
- Records paid_at timestamp

---

#### `cancelInvoice`
**Description:** Cancel an invoice.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

**Behavior:**
- Sets status to "cancelled"
- Records cancelled_at timestamp

---

## Payments

### Queries

#### `payment`
**Description:** Get a specific payment by ID.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Payment`

---

#### `payments`
**Description:** Get payments with optional filters.

**Authentication:** Required

**Input:**
- `invoice_id: ID` (optional)
- `status: PaymentStatus` (optional)
- `skip: Int = 0`
- `limit: Int = 10`

**Returns:** `[Payment]`

**Example:**
```graphql
query ListPayments {
  payments(invoice_id: "invoice-uuid") {
    id
    payment_number
    payment_date
    amount
    payment_method
    status
  }
}
```

---

### Mutations

#### `createPayment`
**Description:** Create a new payment for an invoice.

**Authentication:** Required

**Input:**
```graphql
input CreatePaymentInput {
  invoice_id: ID!
  payment_date: Date!
  amount: Float!
  payment_method: PaymentMethod!
  transaction_id: String
  reference_number: String
  notes: String
}
```

**Returns:** `Payment`

**Behavior:**
- Auto-generates payment number
- Updates invoice amount_paid and amount_due
- Marks invoice as paid if fully paid

**Example:**
```graphql
mutation CreatePayment {
  createPayment(input: {
    invoice_id: "invoice-uuid"
    payment_date: "2026-01-20"
    amount: 1650.00
    payment_method: BANK_TRANSFER
    transaction_id: "TXN-123456"
    notes: "Wire transfer received"
  }) {
    id
    payment_number
    amount
    status
  }
}
```

---

#### `updatePayment`
**Description:** Update an existing payment.

**Authentication:** Required

**Input:**
```graphql
input UpdatePaymentInput {
  payment_date: Date
  amount: Float
  payment_method: PaymentMethod
  transaction_id: String
  reference_number: String
  notes: String
  status: PaymentStatus
}
```

**Returns:** `Payment`

**Behavior:**
- Recalculates invoice amounts if payment amount changes

---

#### `deletePayment`
**Description:** Delete a payment.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

**Behavior:**
- Updates invoice amounts
- Reverts invoice status if was marked as paid

---

#### `refundPayment`
**Description:** Refund a payment.

**Authentication:** Required

**Input:**
- `id: ID!`

**Returns:** `Boolean`

**Behavior:**
- Sets payment status to "refunded"
- Updates invoice amounts
- Sets invoice status to "refunded"

---

## Billing & Subscriptions

### Queries

#### `availablePlans`
**Description:** Get all active billing plans.

**Returns:** `[BillingPlanType]`

**Example:**
```graphql
query AvailablePlans {
  availablePlans {
    id
    name
    plan_type
    description
    price_monthly
    price_yearly
    currency
    max_invoices_per_month
    max_businesses
    features
  }
}
```

---

#### `currentSubscription`
**Description:** Get current user's subscription.

**Authentication:** Required

**Returns:** `SubscriptionType`

**Example:**
```graphql
query CurrentSubscription {
  currentSubscription {
    id
    plan {
      name
      plan_type
      price_monthly
      max_invoices_per_month
      max_businesses
    }
    status
    current_period_start
    current_period_end
    cancel_at_period_end
  }
}
```

---

## Waitlist

### Queries

#### `waitlistEntry`
**Description:** Get waitlist entry by ID (Admin only).

**Authentication:** Required (Admin)

**Input:**
- `id: ID!`

**Returns:** `Waitlist`

---

#### `waitlistEntries`
**Description:** Get list of waitlist entries with filters (Admin only).

**Authentication:** Required (Admin)

**Input:**
```graphql
input WaitlistFilterInput {
  email: String
  company_name: String
  source: String
  priority: WaitlistPriority
  is_notified: Boolean
  is_converted: Boolean
  tags: String
  created_after: DateTime
  created_before: DateTime
}
```
- `filter: WaitlistFilterInput` (optional)
- `skip: Int = 0`
- `limit: Int = 50`
- `order_by: String = "created_at"`
- `order_desc: Boolean = true`

**Returns:** `[Waitlist]`

---

#### `waitlistByEmail`
**Description:** Get waitlist entry by email (Public - limited info).

**Input:**
- `email: String!`

**Returns:** `Waitlist` (with limited fields)

---

#### `waitlistStats`
**Description:** Get waitlist statistics (Admin only).

**Authentication:** Required (Admin)

**Returns:** `WaitlistStats`

**Example:**
```graphql
query WaitlistStats {
  waitlistStats {
    total_count
    notified_count
    converted_count
    conversion_rate
    recent_signups
  }
}
```

---

#### `waitlistPosition`
**Description:** Get position in waitlist by email (Public).

**Input:**
- `email: String!`

**Returns:** `Int` (1-based position)

---

### Mutations

#### `joinWaitlist`
**Description:** Join the waitlist (Public endpoint).

**Input:**
```graphql
input CreateWaitlistInput {
  email: String!
  first_name: String
  last_name: String
  company_name: String
  phone: String
  message: String
  source: String
  utm_source: String
  utm_medium: String
  utm_campaign: String
  priority: WaitlistPriority
  tags: String
}
```

**Returns:** `Waitlist`

**Behavior:**
- Returns existing entry if email already exists
- Captures IP address and user agent
- Email is normalized (lowercase, trimmed)

**Example:**
```graphql
mutation JoinWaitlist {
  joinWaitlist(input: {
    email: "user@example.com"
    first_name: "John"
    last_name: "Doe"
    company_name: "Acme Inc"
    source: "landing_page"
  }) {
    id
    email
    created_at
  }
}
```

---

#### `updateWaitlistEntry`
**Description:** Update a waitlist entry (Admin only).

**Authentication:** Required (Admin)

**Input:**
```graphql
input UpdateWaitlistInput {
  first_name: String
  last_name: String
  company_name: String
  phone: String
  message: String
  source: String
  priority: WaitlistPriority
  tags: String
  notes: String
  is_notified: Boolean
  is_converted: Boolean
  user_id: ID
}
```

**Returns:** `Waitlist`

---

#### `deleteWaitlistEntry`
**Description:** Delete a waitlist entry (Admin only).

**Authentication:** Required (Admin)

**Input:**
- `id: ID!`

**Returns:** `Boolean`

---

#### `markWaitlistNotified`
**Description:** Mark waitlist entries as notified (Admin only).

**Authentication:** Required (Admin)

**Input:**
- `ids: [ID!]!`

**Returns:** `[Waitlist]`

---

#### `markWaitlistConverted`
**Description:** Mark waitlist entry as converted to user (Admin only).

**Authentication:** Required (Admin)

**Input:**
- `id: ID!`
- `user_id: ID` (optional)

**Returns:** `Waitlist`

---

#### `bulkUpdateWaitlistPriority`
**Description:** Bulk update priority for waitlist entries (Admin only).

**Authentication:** Required (Admin)

**Input:**
- `ids: [ID!]!`
- `priority: String!` (options: "normal", "high", "vip")

**Returns:** `[Waitlist]`

---

## Common Types & Enums

### Enums

#### `UserRole`
```graphql
enum UserRole {
  USER
  ADMIN
  SUPER_ADMIN
}
```

#### `UserStatus`
```graphql
enum UserStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
  DELETED
}
```

#### `BusinessType`
```graphql
enum BusinessType {
  SOLE_PROPRIETOR
  PARTNERSHIP
  COMPANY
  LLC
  CORPORATION
  NON_PROFIT
  OTHER
}
```

#### `ClientType`
```graphql
enum ClientType {
  INDIVIDUAL
  COMPANY
}
```

#### `ClientStatus`
```graphql
enum ClientStatus {
  ACTIVE
  INACTIVE
  ARCHIVED
}
```

#### `CategoryType`
```graphql
enum CategoryType {
  INVOICE
  EXPENSE
}
```

#### `InvoiceStatus`
```graphql
enum InvoiceStatus {
  DRAFT
  SENT
  VIEWED
  PAID
  PARTIALLY_PAID
  OVERDUE
  CANCELLED
  REFUNDED
}
```

#### `PaymentMethod`
```graphql
enum PaymentMethod {
  CASH
  CHECK
  BANK_TRANSFER
  CREDIT_CARD
  DEBIT_CARD
  PAYPAL
  STRIPE
  OTHER
}
```

#### `PaymentStatus`
```graphql
enum PaymentStatus {
  PENDING
  COMPLETED
  FAILED
  REFUNDED
  CANCELLED
}
```

#### `PaymentTerms`
```graphql
enum PaymentTerms {
  DUE_ON_RECEIPT
  NET_15
  NET_30
  NET_45
  NET_60
  NET_90
  CUSTOM
}
```

#### `DiscountType`
```graphql
enum DiscountType {
  PERCENTAGE
  FIXED
}
```

#### `WaitlistPriority`
```graphql
enum WaitlistPriority {
  NORMAL
  HIGH
  VIP
}
```

---

## Error Handling

All mutations and queries may throw exceptions with descriptive error messages:

- **Authentication Errors:** "Not authenticated"
- **Authorization Errors:** "Access denied. Admin privileges required."
- **Not Found Errors:** "Business not found", "Client not found", etc.
- **Validation Errors:** "Product with this SKU already exists", "Invalid OTP", etc.
- **Billing Limit Errors:** "Maximum business profiles reached for your plan. Please upgrade to create more."

**Example Error Response:**
```json
{
  "errors": [
    {
      "message": "Not authenticated",
      "path": ["myBusinesses"]
    }
  ]
}
```

---

## Authentication

Most queries and mutations require authentication. Include the JWT token in the request headers:

```http
Authorization: Bearer <your-jwt-token>
```

The token is obtained from the `login` mutation and should be stored securely on the frontend.

---

## Pagination

Queries that return lists support pagination with `skip` and `limit` parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default varies by query)

**Example:**
```graphql
query PaginatedInvoices {
  invoices(skip: 20, limit: 10) {
    id
    invoice_number
  }
}
```

---

## Caching

The `invoices` query implements Redis caching with a 300-second TTL. Cache keys are based on query parameters and user ID.

---

## Best Practices

1. **Always handle errors gracefully** - Check for error responses and display user-friendly messages
2. **Use fragments** - Define reusable GraphQL fragments for common fields
3. **Request only needed fields** - Don't over-fetch data
4. **Implement pagination** - For large datasets, use skip/limit parameters
5. **Cache responses** - Use client-side caching (Apollo Client, URQL, etc.)
6. **Validate inputs** - Validate data on frontend before sending mutations
7. **Handle authentication** - Store and refresh JWT tokens securely
8. **Monitor rate limits** - Be aware of billing plan limits (invoices, businesses)

---

## GraphQL Client Setup Example

### Apollo Client (React)

```javascript
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: 'https://your-api.com/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});

export default client;
```

---

## Support

For questions or issues, please contact the development team or refer to the backend repository documentation.

---

**Document Version:** 1.0  
**Generated:** 2026-01-20  
**Backend Version:** Latest
