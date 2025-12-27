@echo off
REM InvoiceGen Database Setup Script for Windows
REM ============================================

echo.
echo ========================================
echo   InvoiceGen Database Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Choose an option:
echo.
echo 1. Full setup (create DB, tables, admin user, seed data)
echo 2. Create database only
echo 3. Create admin user only
echo 4. Seed initial data only
echo 5. Reset database (drop and recreate tables)
echo 6. Fix SSL issues (disable SSL for local development)
echo 7. Validate configuration
echo 8. Show current configuration
echo 9. Run Migrations (Apply pending changes)
echo 10. Create Migration (Generate new revision)
echo.

set /p choice="Enter your choice (1-10): "

if "%choice%"=="1" (
    echo Running full setup...
    python scripts/setup_database.py --all
) else if "%choice%"=="2" (
    echo Creating database...
    python scripts/setup_database.py --create-db
) else if "%choice%"=="3" (
    echo Creating admin user...
    python scripts/setup_database.py --create-admin
) else if "%choice%"=="4" (
    echo Seeding initial data...
    python scripts/setup_database.py --seed-data
) else if "%choice%"=="5" (
    echo Resetting database...
    python scripts/reset_db.py
) else if "%choice%"=="6" (
    echo Fixing SSL issues...
    python scripts/config_manager.py ssl-disable
) else if "%choice%"=="7" (
    echo Validating configuration...
    python scripts/config_manager.py validate
) else if "%choice%"=="8" (
    echo Showing configuration...
    python scripts/config_manager.py show
) else if "%choice%"=="9" (
    echo Running migrations...
    python scripts/migrate.py up
) else if "%choice%"=="10" (
    call :create_migration
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Setup completed!
echo ========================================
echo.

REM Check if there were any errors
if errorlevel 1 (
    echo There were errors during setup. Please check the output above.
) else (
    echo Setup completed successfully!
    echo.
    echo Next steps:
    echo 1. Start the application: python main.py
    echo 2. Visit http://localhost:8000/docs for API documentation
    echo 3. Visit http://localhost:8000/graphql for GraphQL interface
    echo.
    if "%choice%"=="1" (
        echo Admin credentials:
        echo Email: admin@invoicegen.com
        echo Password: admin123
        echo Please change the password after first login!
    )
)

pause
exit /b

:create_migration
set /p msg="Enter migration message: "
python scripts/migrate.py create -m "%msg%"
exit /b