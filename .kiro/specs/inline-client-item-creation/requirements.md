# Requirements Document

## Introduction

This feature enables users to create new clients and products/items directly from the invoice creation screen without navigating away. Currently, users must pre-create clients and items before creating an invoice, which is inconvenient when dealing with new customers or ad-hoc items. This inline creation capability will streamline the invoice creation workflow and improve user productivity.

## Glossary

- **Invoice_Creation_Screen**: The Flutter screen where users create new invoices (`create_invoice_screen.dart`)
- **Client_Selection_Modal**: The bottom sheet modal that displays the list of existing clients for selection
- **Item_Selection_Modal**: The bottom sheet modal that displays the form for adding line items to an invoice
- **Client_Creation_Dialog**: A new inline form dialog for creating clients without leaving the invoice screen
- **Product_Creation_Dialog**: A new inline form dialog for creating products without leaving the invoice screen
- **ClientProvider**: The Riverpod state management provider for client data operations
- **ProductProvider**: The Riverpod state management provider for product data operations
- **GraphQL_API**: The backend API that handles data persistence via GraphQL mutations

## Requirements

### Requirement 1: Client Creation from Invoice Screen

**User Story:** As a user creating an invoice, I want to create a new client directly from the client selection modal, so that I can quickly add new customers without interrupting my invoice workflow.

#### Acceptance Criteria

1. WHEN the user opens the Client_Selection_Modal, THE Invoice_Creation_Screen SHALL display a "Create New Client" button at the top of the modal
2. WHEN the user taps the "Create New Client" button, THE Invoice_Creation_Screen SHALL display the Client_Creation_Dialog
3. WHEN the Client_Creation_Dialog is displayed, THE Invoice_Creation_Screen SHALL show input fields for client name, email, phone, and address
4. WHEN the user submits the Client_Creation_Dialog with valid data, THE ClientProvider SHALL call the createClient GraphQL mutation
5. WHEN the client creation succeeds, THE ClientProvider SHALL add the new client to the local state
6. WHEN the client creation succeeds, THE Invoice_Creation_Screen SHALL automatically select the newly created client for the invoice
7. WHEN the client creation succeeds, THE Invoice_Creation_Screen SHALL close the Client_Creation_Dialog and return to the invoice form
8. IF the client creation fails, THEN THE Invoice_Creation_Screen SHALL display an error message to the user
9. WHEN the user cancels the Client_Creation_Dialog, THE Invoice_Creation_Screen SHALL return to the Client_Selection_Modal without creating a client

### Requirement 2: Product Creation from Invoice Screen

**User Story:** As a user creating an invoice, I want to create a new product directly from the item selection modal, so that I can quickly add custom items without interrupting my invoice workflow.

#### Acceptance Criteria

1. WHEN the user opens the Item_Selection_Modal, THE Invoice_Creation_Screen SHALL display a "Create New Product" button at the top of the modal
2. WHEN the user taps the "Create New Product" button, THE Invoice_Creation_Screen SHALL display the Product_Creation_Dialog
3. WHEN the Product_Creation_Dialog is displayed, THE Invoice_Creation_Screen SHALL show input fields for product name, description, price, tax rate, and unit of measure
4. WHEN the user submits the Product_Creation_Dialog with valid data, THE ProductProvider SHALL call the createProduct GraphQL mutation
5. WHEN the product creation succeeds, THE ProductProvider SHALL add the new product to the local state
6. WHEN the product creation succeeds, THE Invoice_Creation_Screen SHALL automatically populate the item form with the newly created product data
7. WHEN the product creation succeeds, THE Invoice_Creation_Screen SHALL close the Product_Creation_Dialog and return to the item form
8. IF the product creation fails, THEN THE Invoice_Creation_Screen SHALL display an error message to the user
9. WHEN the user cancels the Product_Creation_Dialog, THE Invoice_Creation_Screen SHALL return to the Item_Selection_Modal without creating a product

### Requirement 3: Form Validation

**User Story:** As a user, I want the system to validate my input when creating clients and products, so that I can ensure data quality and avoid errors.

#### Acceptance Criteria

1. WHEN the user attempts to submit the Client_Creation_Dialog with an empty client name, THE Invoice_Creation_Screen SHALL prevent submission and display a validation error
2. WHEN the user enters an email in the Client_Creation_Dialog, THE Invoice_Creation_Screen SHALL validate that it follows a valid email format
3. WHEN the user attempts to submit the Product_Creation_Dialog with an empty product name, THE Invoice_Creation_Screen SHALL prevent submission and display a validation error
4. WHEN the user enters a price in the Product_Creation_Dialog, THE Invoice_Creation_Screen SHALL validate that it is a valid positive number
5. WHEN the user enters a tax rate in the Product_Creation_Dialog, THE Invoice_Creation_Screen SHALL validate that it is a valid number between 0 and 100

### Requirement 4: UI Consistency and Dark Mode Support

**User Story:** As a user, I want the inline creation dialogs to match the existing app design, so that I have a consistent and familiar experience.

#### Acceptance Criteria

1. THE Client_Creation_Dialog SHALL use the same modern card-based design as the existing Invoice_Creation_Screen
2. THE Product_Creation_Dialog SHALL use the same modern card-based design as the existing Invoice_Creation_Screen
3. THE Client_Creation_Dialog SHALL support dark mode with appropriate color schemes
4. THE Product_Creation_Dialog SHALL support dark mode with appropriate color schemes
5. THE Client_Creation_Dialog SHALL use the same rounded corners, shadows, and spacing as existing modals
6. THE Product_Creation_Dialog SHALL use the same rounded corners, shadows, and spacing as existing modals

### Requirement 5: User Feedback and Loading States

**User Story:** As a user, I want to see clear feedback when creating clients and products, so that I know the system is working and understand the results of my actions.

#### Acceptance Criteria

1. WHEN the user submits the Client_Creation_Dialog, THE Invoice_Creation_Screen SHALL display a loading indicator while the API request is in progress
2. WHEN the user submits the Product_Creation_Dialog, THE Invoice_Creation_Screen SHALL display a loading indicator while the API request is in progress
3. WHEN a client is successfully created, THE Invoice_Creation_Screen SHALL display a success message
4. WHEN a product is successfully created, THE Invoice_Creation_Screen SHALL display a success message
5. WHEN client creation fails, THE Invoice_Creation_Screen SHALL display an error message with details about the failure
6. WHEN product creation fails, THE Invoice_Creation_Screen SHALL display an error message with details about the failure
7. WHILE the API request is in progress, THE Invoice_Creation_Screen SHALL disable the submit button to prevent duplicate submissions

### Requirement 6: Business Context Integration

**User Story:** As a user, I want newly created clients and products to be associated with my current business, so that they are properly organized and accessible.

#### Acceptance Criteria

1. WHEN creating a new client, THE ClientProvider SHALL automatically include the current business ID from the BusinessProvider
2. WHEN creating a new product, THE ProductProvider SHALL automatically include the current business ID from the BusinessProvider
3. IF no business context is available, THEN THE Invoice_Creation_Screen SHALL prevent the creation dialog from opening and display an error message
