# Implementation Plan: Inline Client and Item Creation

## Overview

This implementation plan breaks down the inline client and item creation feature into discrete, incremental coding tasks. Each task builds on previous work and includes testing to validate functionality early. The implementation modifies the existing `create_invoice_screen.dart` to add inline creation dialogs for clients and products, integrating with the existing Riverpod state management architecture.

## Tasks

- [ ] 1. Create client creation dialog UI component
  - Implement `_showClientCreationDialog()` method in `create_invoice_screen.dart`
  - Add form fields: client name (required), email (optional), phone (optional), address (optional)
  - Add "Cancel" and "Create Client" buttons
  - Add form validation for required fields
  - Add loading state indicator
  - Style dialog to match existing modal design (rounded corners, shadows, modern card-based layout)
  - _Requirements: 1.2, 1.3, 3.1, 3.2, 4.1, 4.3, 4.5, 5.1, 5.7_

- [ ] 1.1 Write unit tests for client creation dialog UI
  - Test that dialog displays all required form fields
  - Test that cancel button closes dialog without creating client
  - Test that empty client name shows validation error
  - Test that loading indicator appears during submission
  - Test that submit button is disabled during API call
  - _Requirements: 1.3, 1.9, 3.1, 5.1, 5.7_

- [ ] 1.2 Write property test for email validation
  - **Property 3: Email Validation**
  - **Validates: Requirements 3.2**

- [ ] 2. Create product creation dialog UI component
  - Implement `_showProductCreationDialog()` method in `create_invoice_screen.dart`
  - Add form fields: product name (required), description (optional), price (required), tax rate (optional, default 0), unit (optional, default "unit")
  - Add "Cancel" and "Create Product" buttons
  - Add form validation for required fields and numeric inputs
  - Add loading state indicator
  - Style dialog to match existing modal design
  - _Requirements: 2.2, 2.3, 3.3, 3.4, 3.5, 4.2, 4.4, 4.6, 5.2, 5.7_

- [ ] 2.1 Write unit tests for product creation dialog UI
  - Test that dialog displays all required form fields
  - Test that cancel button closes dialog without creating product
  - Test that empty product name shows validation error
  - Test that loading indicator appears during submission
  - Test that submit button is disabled during API call
  - _Requirements: 2.3, 2.9, 3.3, 5.2, 5.7_

- [ ] 2.2 Write property tests for price and tax rate validation
  - **Property 4: Price Validation**
  - **Validates: Requirements 3.4**
  - **Property 5: Tax Rate Validation**
  - **Validates: Requirements 3.5**

- [ ] 3. Integrate client creation with ClientProvider
  - Modify `_showClientCreationDialog()` to call `ClientProvider.createClient()` on form submission
  - Get business ID from `BusinessProvider` and include in client data
  - Handle API success: close dialog, show success message
  - Handle API errors: display error message, keep dialog open
  - Add error handling for missing business context
  - _Requirements: 1.4, 1.5, 1.7, 1.8, 5.3, 5.5, 6.1, 6.3_

- [ ] 3.1 Write property test for client creation flow
  - **Property 1: Client Creation and Selection**
  - **Validates: Requirements 1.4, 1.5, 1.6**

- [ ] 3.2 Write property test for business context inclusion in clients
  - **Property 6: Business Context Inclusion for Clients**
  - **Validates: Requirements 6.1**

- [ ] 3.3 Write unit tests for client creation error handling
  - Test API failure displays error message
  - Test missing business context shows error
  - Test success message appears after creation
  - _Requirements: 1.8, 5.3, 5.5, 6.3_

- [ ] 4. Integrate product creation with ProductProvider
  - Modify `_showProductCreationDialog()` to call `ProductProvider.createProduct()` on form submission
  - Get business ID from `BusinessProvider` and include in product data
  - Handle API success: close dialog, show success message
  - Handle API errors: display error message, keep dialog open
  - Add error handling for missing business context
  - _Requirements: 2.4, 2.5, 2.7, 2.8, 5.4, 5.6, 6.2, 6.3_

- [ ] 4.1 Write property test for product creation flow
  - **Property 2: Product Creation and Population**
  - **Validates: Requirements 2.4, 2.5, 2.6**

- [ ] 4.2 Write property test for business context inclusion in products
  - **Property 7: Business Context Inclusion for Products**
  - **Validates: Requirements 6.2**

- [ ] 4.3 Write unit tests for product creation error handling
  - Test API failure displays error message
  - Test missing business context shows error
  - Test success message appears after creation
  - _Requirements: 2.8, 5.4, 5.6, 6.3_

- [ ] 5. Modify client selection modal to add "Create New Client" button
  - Update `_selectClient()` method in `create_invoice_screen.dart`
  - Add "Create New Client" button at the top of the client list
  - Style button with primary color and icon
  - Wire button to call `_showClientCreationDialog()`
  - Handle dialog result: if client created, auto-select it and close modal
  - _Requirements: 1.1, 1.2, 1.6_

- [ ] 5.1 Write unit tests for client selection modal integration
  - Test "Create New Client" button appears in modal
  - Test tapping button opens client creation dialog
  - Test newly created client is auto-selected
  - _Requirements: 1.1, 1.2, 1.6_

- [ ] 6. Modify item selection modal to add "Create New Product" button
  - Update `_addItem()` method in `create_invoice_screen.dart`
  - Add "Create New Product" button at the top of the form
  - Style button with primary color and icon
  - Wire button to call `_showProductCreationDialog()`
  - Handle dialog result: if product created, auto-populate form fields with product data
  - _Requirements: 2.1, 2.2, 2.6_

- [ ] 6.1 Write unit tests for item selection modal integration
  - Test "Create New Product" button appears in modal
  - Test tapping button opens product creation dialog
  - Test newly created product data populates form fields
  - _Requirements: 2.1, 2.2, 2.6_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Run all unit tests and property tests
  - Verify UI rendering in both light and dark modes
  - Test error handling scenarios
  - Ensure all tests pass, ask the user if questions arise

- [ ] 8. Add input validation helpers
  - Create email validation function (regex-based)
  - Create price validation function (positive numbers only)
  - Create tax rate validation function (0-100 range)
  - Create required field validation function
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 8.1 Write unit tests for validation helpers
  - Test email validation with valid and invalid inputs
  - Test price validation with positive, zero, negative, and non-numeric inputs
  - Test tax rate validation with in-range, out-of-range, and non-numeric inputs
  - Test required field validation with empty and non-empty inputs
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 9. Final integration and polish
  - Ensure consistent styling across all dialogs
  - Verify dark mode support
  - Add haptic feedback for button taps (optional enhancement)
  - Ensure keyboard dismissal on dialog close
  - Test on different screen sizes
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [ ] 9.1 Write integration tests for end-to-end flows
  - Test complete client creation flow from invoice screen
  - Test complete product creation flow from invoice screen
  - Test error recovery scenarios
  - Test with various screen sizes
  - _Requirements: 1.1-1.9, 2.1-2.9_

- [ ] 10. Final checkpoint - Ensure all tests pass
  - Run complete test suite
  - Verify all requirements are met
  - Test on physical device if possible
  - Ensure all tests pass, ask the user if questions arise

## Notes

- All tasks are required for comprehensive implementation
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties with minimum 100 iterations
- Unit tests validate specific examples and edge cases
- Integration tests verify end-to-end workflows
- The implementation leverages existing `ClientProvider.createClient()` and `ProductProvider.createProduct()` methods
- GraphQL mutations (`createClient` and `createProduct`) already exist in the backend
- Focus on maintaining visual consistency with existing UI patterns
