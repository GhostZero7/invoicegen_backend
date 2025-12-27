#!/bin/bash
# InvoiceGen Database Setup Script for Unix/Linux/macOS
# ====================================================

set -e  # Exit on any error

echo ""
echo "========================================"
echo "   InvoiceGen Database Setup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python and try again."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "ERROR: Please run this script from the project root directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "Choose an option:"
echo ""
echo "1. Full setup (create DB, tables, admin user, seed data)"
echo "2. Create database only"
echo "3. Create admin user only"
echo "4. Seed initial data only"
echo "5. Reset database (drop and recreate tables)"
echo "6. Fix SSL issues (disable SSL for local development)"
echo "7. Validate configuration"
echo "8. Show current configuration"
echo ""

read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo "Running full setup..."
        $PYTHON_CMD scripts/setup_database.py --all
        ;;
    2)
        echo "Creating database..."
        $PYTHON_CMD scripts/setup_database.py --create-db
        ;;
    3)
        echo "Creating admin user..."
        $PYTHON_CMD scripts/setup_database.py --create-admin
        ;;
    4)
        echo "Seeding initial data..."
        $PYTHON_CMD scripts/setup_database.py --seed-data
        ;;
    5)
        echo "Resetting database..."
        $PYTHON_CMD scripts/setup_database.py --reset
        ;;
    6)
        echo "Fixing SSL issues..."
        $PYTHON_CMD scripts/config_manager.py ssl-disable
        ;;
    7)
        echo "Validating configuration..."
        $PYTHON_CMD scripts/config_manager.py validate
        ;;
    8)
        echo "Showing configuration..."
        $PYTHON_CMD scripts/config_manager.py show
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "   Setup completed!"
echo "========================================"
echo ""

# Check if the last command was successful
if [ $? -eq 0 ]; then
    echo "Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Start the application: $PYTHON_CMD main.py"
    echo "2. Visit http://localhost:8000/docs for API documentation"
    echo "3. Visit http://localhost:8000/graphql for GraphQL interface"
    echo ""
    if [ "$choice" = "1" ]; then
        echo "Admin credentials:"
        echo "Email: admin@invoicegen.com"
        echo "Password: admin123"
        echo "Please change the password after first login!"
    fi
else
    echo "There were errors during setup. Please check the output above."
    exit 1
fi