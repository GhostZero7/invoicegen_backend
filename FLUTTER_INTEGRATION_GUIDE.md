# Flutter App Integration Guide for InvoiceGen Backend

## 📊 Complete Backend Structure Overview

### API Architecture
Your backend has **3 main layers**:
1. **REST API** (FastAPI) - Traditional REST endpoints
2. **GraphQL API** (Strawberry) - Modern GraphQL queries/mutations
3. **Authentication** - JWT-based token system

---

## 🔐 Authentication Layer

### Base URL
```
Production: https://your-production-domain.com
Development: http://10.148.32.81:8000
```

### 1. User Registration
**Endpoint:** `POST /auth/register`
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. User Login
**Endpoint:** `POST /auth/login`
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Token Usage
All protected endpoints require header:
```
Authorization: Bearer <access_token>
```

Token expiration: **60 minutes** (configurable in `.env`)

---

## 📱 Data Models Overview

### Core Entities

#### 1. **User**
```dart
class User {
  String id;                    // UUID
  String email;
  String firstName;
  String lastName;
  String? phone;
  String? avatarUrl;
  bool emailVerified;
  bool twoFactorEnabled;
  String role;                  // USER, ADMIN, ACCOUNTANT
  String status;                // ACTIVE, SUSPENDED, DELETED
  DateTime? lastLoginAt;
  DateTime createdAt;
  DateTime updatedAt;
  List<BusinessProfile> businessProfiles;
}
```

#### 2. **Business Profile**
```dart
class BusinessProfile {
  String id;                    // UUID
  String userId;
  String businessName;
  String businessType;          // SOLE_PROPRIETOR, LLC, CORPORATION, PARTNERSHIP
  String? taxId;
  String? vatNumber;
  String? registrationNumber;
  String? website;
  String? phone;
  String email;
  String? logoUrl;
  String currency;              // USD, EUR, etc.
  String timezone;
  Date? fiscalYearEnd;
  String invoicePrefix;         // e.g., "INV"
  String quotePrefix;           // e.g., "QUO"
  int nextInvoiceNumber;
  int nextQuoteNumber;
  String paymentTermsDefault;
  String? notesDefault;
  String? paymentInstructions;
  bool isActive;
  DateTime createdAt;
  DateTime updatedAt;
}
```

#### 3. **Client**
```dart
class Client {
  String id;                    // UUID
  String businessId;
  String clientType;            // INDIVIDUAL, COMPANY
  String? companyName;
  String? firstName;
  String? lastName;
  String email;
  String? phone;
  String? mobile;
  String? website;
  String? taxId;
  String? vatNumber;
  String? paymentTerms;
  double? creditLimit;
  String currency;              // USD, EUR, etc.
  String language;              // en, es, fr, etc.
  String? notes;
  Map<String, dynamic>? tags;
  String status;                // ACTIVE, INACTIVE, BLOCKED
  DateTime createdAt;
  DateTime updatedAt;
  List<ClientContact> contacts;
  List<Address> addresses;
}
```

#### 4. **Invoice**
```dart
class Invoice {
  String id;                    // UUID
  String businessId;
  String clientId;
  String invoiceNumber;         // Auto-generated: INV-001, INV-002, etc.
  Date invoiceDate;
  Date dueDate;
  String status;                // DRAFT, SENT, VIEWED, PAID, OVERDUE, CANCELLED, REFUNDED
  double subtotal;
  double taxAmount;
  double discountAmount;
  double totalAmount;
  String currency;
  String paymentTerms;
  String? notes;
  String? internalNotes;
  double amountPaid;
  double amountDue;
  DateTime createdAt;
  DateTime updatedAt;
  List<InvoiceItem> items;
}
```

#### 5. **Invoice Item**
```dart
class InvoiceItem {
  String id;                    // UUID
  String invoiceId;
  String? productId;
  String description;
  double quantity;
  double unitPrice;
  double? taxRate;
  double lineTotal;             // quantity * unitPrice
  int sortOrder;
}
```

#### 6. **Product**
```dart
class Product {
  String id;                    // UUID
  String businessId;
  String? sku;
  String name;
  String? description;
  double unitPrice;
  double? costPrice;
  String unitOfMeasure;         // unit, kg, liter, hour, etc.
  double taxRate;
  bool isTaxable;
  bool trackInventory;
  int quantityInStock;
  int? lowStockThreshold;
  String? imageUrl;
  bool isActive;
  DateTime createdAt;
  DateTime updatedAt;
}
```

#### 7. **Payment**
```dart
class Payment {
  String id;                    // UUID
  String invoiceId;
  String businessId;
  String? clientId;
  double amount;
  String paymentMethod;         // CREDIT_CARD, BANK_TRANSFER, CASH, CHECK, etc.
  String status;                // PENDING, COMPLETED, FAILED
  Date paymentDate;
  String? reference;            // Transaction ID, check number, etc.
  String? notes;
  DateTime createdAt;
  DateTime updatedAt;
}
```

#### 8. **Address**
```dart
class Address {
  String id;                    // UUID
  String? userId;
  String? clientId;
  String? businessId;
  String addressType;           // BILLING, SHIPPING, BUSINESS, HOME
  String streetAddress;
  String? streetAddress2;
  String city;
  String state;
  String postalCode;
  String country;
  bool isDefault;
  DateTime createdAt;
  DateTime updatedAt;
}
```

---

## 🔗 REST API Endpoints (Currently Implemented)

### Authentication Endpoints
```
POST   /auth/register          - Register new user
POST   /auth/login             - Login user
```

### Invoice Endpoints
```
POST   /invoices/              - Create invoice
```

---

## 🔗 REST API Endpoints (Need to be Implemented)

### User Management
```
GET    /api/v1/users           - List all users (admin only)
GET    /api/v1/users/{id}      - Get user details
PUT    /api/v1/users/{id}      - Update user profile
DELETE /api/v1/users/{id}      - Delete user account
GET    /api/v1/users/me        - Get current user profile
```

### Business Profiles
```
GET    /api/v1/business        - List user's business profiles
POST   /api/v1/business        - Create new business profile
GET    /api/v1/business/{id}   - Get business details
PUT    /api/v1/business/{id}   - Update business profile
DELETE /api/v1/business/{id}   - Delete business profile
```

### Clients
```
GET    /api/v1/clients         - List clients (filtered by business)
POST   /api/v1/clients         - Create client
GET    /api/v1/clients/{id}    - Get client details
PUT    /api/v1/clients/{id}    - Update client
DELETE /api/v1/clients/{id}    - Delete client
GET    /api/v1/clients/{id}/invoices - Get client's invoices
```

### Invoices
```
GET    /api/v1/invoices        - List invoices (filtered by business)
POST   /api/v1/invoices        - Create invoice
GET    /api/v1/invoices/{id}   - Get invoice details
PUT    /api/v1/invoices/{id}   - Update invoice
DELETE /api/v1/invoices/{id}   - Delete invoice
POST   /api/v1/invoices/{id}/send - Send invoice to client
POST   /api/v1/invoices/{id}/mark-paid - Mark invoice as paid
```

### Payments
```
GET    /api/v1/payments        - List payments
POST   /api/v1/payments        - Create payment record
GET    /api/v1/payments/{id}   - Get payment details
PUT    /api/v1/payments/{id}   - Update payment
DELETE /api/v1/payments/{id}   - Delete payment
```

### Products
```
GET    /api/v1/products        - List products (filtered by business)
POST   /api/v1/products        - Create product
GET    /api/v1/products/{id}   - Get product details
PUT    /api/v1/products/{id}   - Update product
DELETE /api/v1/products/{id}   - Delete product
```

### Categories
```
GET    /api/v1/categories      - List categories
POST   /api/v1/categories      - Create category
GET    /api/v1/categories/{id} - Get category details
PUT    /api/v1/categories/{id} - Update category
DELETE /api/v1/categories/{id} - Delete category
```

---

## 📊 GraphQL API (Available)

### Base URL
```
POST /graphql
```

### Supported Queries
```graphql
# Get current user
query {
  me {
    id
    email
    firstName
    lastName
    businessProfiles {
      id
      businessName
    }
  }
}

# Get business invoices
query {
  business(id: "uuid") {
    id
    businessName
    invoices {
      id
      invoiceNumber
      status
      totalAmount
    }
  }
}

# Get clients
query {
  clients(businessId: "uuid") {
    id
    firstName
    lastName
    email
    status
  }
}
```

### Supported Mutations
```graphql
# Create invoice
mutation {
  createInvoice(input: {
    businessId: "uuid"
    clientId: "uuid"
    dueDate: "2025-01-15"
    items: [
      {
        description: "Service"
        quantity: 1
        unitPrice: 100
      }
    ]
  }) {
    id
    invoiceNumber
  }
}
```

---

## 📲 Flutter Integration Implementation

### 1. Installation Package
```yaml
dependencies:
  http: ^1.1.0
  dio: ^5.3.0
  get_it: ^7.6.0
  shared_preferences: ^2.2.0
  jwt_decoder: ^2.0.0
```

### 2. API Service Setup

```dart
// lib/services/api_service.dart
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://10.148.32.81:8000';
  
  final Dio _dio;
  final SharedPreferences _prefs;
  
  ApiService(this._dio, this._prefs) {
    _setupDio();
  }
  
  void _setupDio() {
    _dio.options.baseUrl = baseUrl;
    _dio.options.contentType = Headers.jsonContentType;
    _dio.options.headers = {
      'Accept': 'application/json',
    };
    
    // Add interceptor for token
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = _prefs.getString('access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token expired - refresh or logout
          await logout();
        }
        return handler.next(error);
      },
    ));
  }
  
  // Auth Methods
  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    String? phone,
  }) async {
    final response = await _dio.post(
      '/auth/register',
      data: {
        'email': email,
        'password': password,
        'first_name': firstName,
        'last_name': lastName,
        'phone': phone,
      },
    );
    
    if (response.statusCode == 200) {
      final token = response.data['access_token'];
      await _prefs.setString('access_token', token);
      return response.data;
    }
    throw Exception('Registration failed');
  }
  
  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await _dio.post(
      '/auth/login',
      data: {
        'email': email,
        'password': password,
      },
    );
    
    if (response.statusCode == 200) {
      final token = response.data['access_token'];
      await _prefs.setString('access_token', token);
      return response.data;
    }
    throw Exception('Login failed');
  }
  
  Future<void> logout() async {
    await _prefs.remove('access_token');
  }
  
  // User Methods
  Future<Map<String, dynamic>> getCurrentUser() async {
    final response = await _dio.get('/api/v1/users/me');
    return response.data;
  }
  
  // Business Methods
  Future<List<dynamic>> getBusinessProfiles() async {
    final response = await _dio.get('/api/v1/business');
    return response.data;
  }
  
  // Invoice Methods
  Future<List<dynamic>> getInvoices({
    String? businessId,
    String? status,
    int skip = 0,
    int limit = 20,
  }) async {
    final response = await _dio.get(
      '/api/v1/invoices',
      queryParameters: {
        'business_id': businessId,
        'status': status,
        'skip': skip,
        'limit': limit,
      },
    );
    return response.data;
  }
  
  Future<Map<String, dynamic>> createInvoice({
    required String businessId,
    required String clientId,
    required DateTime dueDate,
    required List<Map<String, dynamic>> items,
  }) async {
    final response = await _dio.post(
      '/api/v1/invoices',
      data: {
        'business_id': businessId,
        'client_id': clientId,
        'due_date': dueDate.toIso8601String(),
        'items': items,
      },
    );
    return response.data;
  }
  
  // Client Methods
  Future<List<dynamic>> getClients({String? businessId}) async {
    final response = await _dio.get(
      '/api/v1/clients',
      queryParameters: {'business_id': businessId},
    );
    return response.data;
  }
  
  // Payment Methods
  Future<Map<String, dynamic>> recordPayment({
    required String invoiceId,
    required double amount,
    required String paymentMethod,
    required DateTime paymentDate,
  }) async {
    final response = await _dio.post(
      '/api/v1/payments',
      data: {
        'invoice_id': invoiceId,
        'amount': amount,
        'payment_method': paymentMethod,
        'payment_date': paymentDate.toIso8601String(),
      },
    );
    return response.data;
  }
}
```

### 3. GraphQL Client

```dart
// lib/services/graphql_service.dart
import 'package:graphql_flutter/graphql_flutter.dart';

class GraphQLService {
  late GraphQLClient _graphQLClient;
  
  GraphQLService(String token) {
    final link = HttpLink(
      'http://10.148.32.81:8000/graphql',
      defaultHeaders: {
        'Authorization': 'Bearer $token',
      },
    );
    
    _graphQLClient = GraphQLClient(
      link: link,
      cache: GraphQLCache(),
    );
  }
  
  Future<QueryResult> getCurrentUser() {
    final query = gql(r'''
      query {
        me {
          id
          email
          firstName
          lastName
          businessProfiles {
            id
            businessName
          }
        }
      }
    ''');
    
    return _graphQLClient.query(QueryOptions(document: query));
  }
}
```

---

## 🚀 Implementation Roadmap

### Phase 1: Authentication (✅ Ready)
- [x] User Registration
- [x] User Login
- [ ] Token Refresh
- [ ] Password Reset
- [ ] 2FA Support

### Phase 2: Core Business Operations
- [ ] Business Profile Management
- [ ] Client Management (CRUD)
- [ ] Product Catalog
- [ ] Category Management

### Phase 3: Invoice Management
- [ ] Create Invoices
- [ ] Edit Invoices
- [ ] Send Invoices
- [ ] Invoice Templates
- [ ] Recurring Invoices

### Phase 4: Payment Tracking
- [ ] Record Payments
- [ ] Payment History
- [ ] Payment Methods
- [ ] Payment Status Tracking

### Phase 5: Reporting
- [ ] Revenue Reports
- [ ] Outstanding Invoices
- [ ] Payment Analytics
- [ ] Expense Reports

---

## 📋 Detailed Implementation Steps for Flutter

### Step 1: Setup Service Locator
```dart
// lib/injection_container.dart
import 'package:get_it/get_it.dart';

final getIt = GetIt.instance;

Future<void> setupServiceLocator() async {
  // Dio
  getIt.registerSingleton<Dio>(Dio());
  
  // Shared Preferences
  final prefs = await SharedPreferences.getInstance();
  getIt.registerSingleton<SharedPreferences>(prefs);
  
  // API Service
  getIt.registerSingleton<ApiService>(
    ApiService(getIt<Dio>(), getIt<SharedPreferences>()),
  );
  
  // Repositories (to create next)
  getIt.registerSingleton<AuthRepository>(
    AuthRepository(getIt<ApiService>()),
  );
}
```

### Step 2: Create Repository Layer
```dart
// lib/repositories/auth_repository.dart
class AuthRepository {
  final ApiService apiService;
  
  AuthRepository(this.apiService);
  
  Future<bool> login(String email, String password) async {
    try {
      await apiService.login(email: email, password: password);
      return true;
    } catch (e) {
      return false;
    }
  }
  
  Future<bool> register({
    required String email,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    try {
      await apiService.register(
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );
      return true;
    } catch (e) {
      return false;
    }
  }
}
```

### Step 3: Create Models
```dart
// lib/models/user.dart
class User {
  final String id;
  final String email;
  final String firstName;
  final String lastName;
  final String? phone;
  final String role;
  final DateTime createdAt;
  
  User({
    required this.id,
    required this.email,
    required this.firstName,
    required this.lastName,
    this.phone,
    required this.role,
    required this.createdAt,
  });
  
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      phone: json['phone'],
      role: json['role'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
```

---

## 🔒 Security Best Practices

1. **Token Storage**: Use flutter_secure_storage for token storage
2. **HTTPS**: Use HTTPS in production
3. **Token Refresh**: Implement token refresh mechanism
4. **Request Validation**: Validate all inputs before sending
5. **CORS**: Configure CORS properly in backend
6. **Rate Limiting**: Implement rate limiting on sensitive endpoints

---

## 📞 API Error Handling

```dart
// Standard error responses
{
  "detail": "Error message",
  "status_code": 400
}

// Validation error
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error"
    }
  ]
}
```

---

## 🎯 Next Steps

1. **Implement missing REST endpoints** for all models
2. **Add GraphQL resolvers** for all operations
3. **Implement Flutter repository pattern**
4. **Add state management** (Provider, Riverpod, or Bloc)
5. **Create UI screens** for all features
6. **Add offline capability** with local storage
7. **Implement caching strategy**
8. **Add error handling and notifications**

