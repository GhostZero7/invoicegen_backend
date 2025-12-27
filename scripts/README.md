# InvoiceGen Database Setup Scripts

This directory contains scripts to help you set up and manage your InvoiceGen database and configuration.

## Quick Start

### Windows
```bash
scripts\setup.bat
```

### Unix/Linux/macOS
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Scripts Overview

### 1. `setup_database.py`
Main database setup script with comprehensive functionality:

**Features:**
- ✅ Database creation
- ✅ Table creation with all models
- ✅ Admin user creation
- ✅ Initial data seeding
- ✅ SSL configuration handling
- ✅ Database connection testing

**Usage:**
```bash
# Full setup
python scripts/setup_database.py --all

# Individual operations
python scripts/setup_database.py --create-db
python scripts/setup_database.py --create-admin
python scripts/setup_database.py --seed-data
python scripts/setup_database.py --reset

# SSL configuration
python scripts/setup_database.py --ssl-mode disable
python scripts/setup_database.py --ssl-mode require
```

### 2. `config_manager.py`
Configuration management script for handling environment variables and SSL settings:

**Features:**
- ✅ SSL mode management
- ✅ Configuration validation
- ✅ Configuration backup/restore
- ✅ Environment file management

**Usage:**
```bash
# SSL management
python scripts/config_manager.py ssl-disable
python scripts/config_manager.py ssl-enable

# Configuration management
python scripts/config_manager.py validate
python scripts/config_manager.py show
python scripts/config_manager.py backup
python scripts/config_manager.py list-backups
python scripts/config_manager.py restore backup_name
```

### 3. `setup.bat` / `setup.sh`
Interactive setup scripts for easy database initialization:

**Features:**
- ✅ Interactive menu
- ✅ Cross-platform support
- ✅ Error handling
- ✅ User-friendly interface

## Common Issues & Solutions

### SSL Connection Error
```
psycopg2.OperationalError: server does not support SSL, but SSL was required
```

**Solution:**
```bash
# Option 1: Use the interactive script
scripts\setup.bat  # Choose option 6

# Option 2: Use config manager directly
python scripts/config_manager.py ssl-disable
```

### Database Connection Failed
**Check:**
1. PostgreSQL is running
2. Database credentials are correct
3. Database exists
4. SSL mode is appropriate for your setup

**Solution:**
```bash
# Validate configuration
python scripts/config_manager.py validate

# Create database if missing
python scripts/setup_database.py --create-db
```

### Missing Admin User
```bash
python scripts/setup_database.py --create-admin
```

**Default Admin Credentials:**
- Email: `admin@invoicegen.com`
- Password: `admin123`
- ⚠️ **Change password after first login!**

## Environment Configuration

### Local Development (.env.local)
```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/invoicegen?sslmode=disable"
```

### Production (.env)
```env
DATABASE_URL="postgresql://user:password@host:5432/database?sslmode=require"
```

## Database Models Included

The setup script creates tables for all models:
- ✅ Users & Authentication
- ✅ Business Profiles
- ✅ Clients & Contacts
- ✅ Products & Categories
- ✅ Invoices & Invoice Items
- ✅ Quotes & Quote Items
- ✅ Payments & Expenses
- ✅ Tax Rates & Addresses
- ✅ Notifications & Reminders
- ✅ Waitlist & Audit Logs

## Initial Data Seeding

The seed data includes:
- **Categories:** General, Services, Office Supplies, Travel, Marketing
- **Tax Rates:** No Tax (0%), Standard VAT (20%), Reduced VAT (5%)
- **Admin User:** Ready-to-use admin account

## Backup & Restore

Configuration backups are stored in `scripts/backups/` with timestamps:
```
scripts/backups/
├── config_backup_20231215_143022/
│   ├── .env
│   ├── .env.local
│   └── metadata.json
```

## Troubleshooting

### Script Permissions (Unix/Linux/macOS)
```bash
chmod +x scripts/setup.sh
chmod +x scripts/setup_database.py
chmod +x scripts/config_manager.py
```

### Python Path Issues
Make sure you're running from the project root:
```bash
# Should see main.py in current directory
ls main.py

# Run scripts from project root
python scripts/setup_database.py --help
```

### Database Connection Testing
```bash
# Test connection
python scripts/setup_database.py --create-db
```

## Next Steps After Setup

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Access the interfaces:**
   - API Documentation: http://localhost:8000/docs
   - GraphQL Interface: http://localhost:8000/graphql
   - Health Check: http://localhost:8000/health

3. **Change admin password:**
   - Login with admin credentials
   - Update password through API or GraphQL

4. **Configure for production:**
   ```bash
   python scripts/config_manager.py ssl-enable
   python scripts/config_manager.py validate
   ```

## Support

If you encounter issues:
1. Check the error messages carefully
2. Validate your configuration: `python scripts/config_manager.py validate`
3. Try the SSL fix: `python scripts/config_manager.py ssl-disable`
4. Reset the database: `python scripts/setup_database.py --reset`