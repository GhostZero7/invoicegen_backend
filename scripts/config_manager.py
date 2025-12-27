#!/usr/bin/env python3
"""
Configuration Manager for InvoiceGen
====================================

This script handles configuration management including:
1. SSL mode configuration
2. Database URL management
3. Environment variable management
4. Configuration validation

Usage:
    python scripts/config_manager.py [command] [options]

Commands:
    ssl-disable     Disable SSL for local development
    ssl-enable      Enable SSL for production
    validate        Validate current configuration
    show            Show current configuration
    backup          Backup current configuration
    restore         Restore configuration from backup
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class ConfigManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.env_files = [".env", ".env.local", ".env.example"]
        self.backup_dir = self.project_root / "scripts" / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def read_env_file(self, file_path: str) -> dict:
        """Read environment file and return as dictionary."""
        env_vars = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip('"\'')
                        env_vars[key] = value
        return env_vars
    
    def write_env_file(self, file_path: str, env_vars: dict):
        """Write environment variables to file."""
        with open(file_path, 'w') as f:
            for key, value in env_vars.items():
                # Add quotes around values that contain special characters
                if any(char in value for char in [' ', '&', '?', '=', ';']):
                    f.write(f'{key}="{value}"\n')
                else:
                    f.write(f'{key}={value}\n')
    
    def update_database_url_ssl(self, database_url: str, ssl_mode: str) -> str:
        """Update SSL mode in database URL."""
        parsed = urlparse(database_url)
        query_params = parse_qs(parsed.query)
        
        # Update or add sslmode parameter
        query_params['sslmode'] = [ssl_mode]
        
        # Rebuild URL
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        
        return urlunparse(new_parsed)
    
    def set_ssl_mode(self, ssl_mode: str):
        """Set SSL mode in all environment files."""
        print(f"🔒 Setting SSL mode to: {ssl_mode}")
        
        for env_file in self.env_files:
            file_path = self.project_root / env_file
            if file_path.exists():
                print(f"📝 Updating {env_file}...")
                
                env_vars = self.read_env_file(str(file_path))
                
                if 'DATABASE_URL' in env_vars:
                    old_url = env_vars['DATABASE_URL']
                    new_url = self.update_database_url_ssl(old_url, ssl_mode)
                    env_vars['DATABASE_URL'] = new_url
                    
                    self.write_env_file(str(file_path), env_vars)
                    print(f"✅ Updated {env_file}")
                else:
                    print(f"⚠️  No DATABASE_URL found in {env_file}")
    
    def disable_ssl(self):
        """Disable SSL for local development."""
        print("🔓 Disabling SSL for local development...")
        self.set_ssl_mode("disable")
        print("✅ SSL disabled. Safe for local PostgreSQL without SSL.")
    
    def enable_ssl(self):
        """Enable SSL for production."""
        print("🔒 Enabling SSL for production...")
        self.set_ssl_mode("require")
        print("✅ SSL enabled. Required for production databases.")
    
    def validate_config(self):
        """Validate current configuration."""
        print("🔍 Validating configuration...")
        
        issues = []
        
        for env_file in self.env_files:
            file_path = self.project_root / env_file
            if file_path.exists():
                print(f"📋 Checking {env_file}...")
                env_vars = self.read_env_file(str(file_path))
                
                # Check required variables
                required_vars = ['DATABASE_URL', 'JWT_SECRET', 'JWT_ALGORITHM']
                for var in required_vars:
                    if var not in env_vars:
                        issues.append(f"Missing {var} in {env_file}")
                    elif not env_vars[var]:
                        issues.append(f"Empty {var} in {env_file}")
                
                # Check DATABASE_URL format
                if 'DATABASE_URL' in env_vars:
                    db_url = env_vars['DATABASE_URL']
                    if not db_url.startswith(('postgresql://', 'postgres://')):
                        issues.append(f"Invalid DATABASE_URL format in {env_file}")
                    
                    # Check SSL mode
                    if 'sslmode=' in db_url:
                        if 'localhost' in db_url and 'sslmode=require' in db_url:
                            issues.append(f"SSL required for localhost in {env_file} (may cause connection issues)")
                        elif 'neon.tech' in db_url and 'sslmode=disable' in db_url:
                            issues.append(f"SSL disabled for Neon database in {env_file} (security risk)")
                
                # Check JWT secret strength
                if 'JWT_SECRET' in env_vars:
                    jwt_secret = env_vars['JWT_SECRET']
                    if len(jwt_secret) < 32:
                        issues.append(f"JWT_SECRET too short in {env_file} (should be at least 32 characters)")
        
        if issues:
            print("❌ Configuration issues found:")
            for issue in issues:
                print(f"  • {issue}")
            return False
        else:
            print("✅ Configuration is valid!")
            return True
    
    def show_config(self):
        """Show current configuration."""
        print("📋 Current Configuration:")
        print("=" * 50)
        
        for env_file in self.env_files:
            file_path = self.project_root / env_file
            if file_path.exists():
                print(f"\n📄 {env_file}:")
                env_vars = self.read_env_file(str(file_path))
                
                for key, value in env_vars.items():
                    # Mask sensitive values
                    if key in ['JWT_SECRET', 'PASSWORD']:
                        display_value = '*' * len(value)
                    elif 'PASSWORD' in key.upper() or 'SECRET' in key.upper():
                        display_value = '*' * len(value)
                    elif key == 'DATABASE_URL':
                        # Mask password in database URL
                        parsed = urlparse(value)
                        if parsed.password:
                            masked_url = value.replace(parsed.password, '*' * len(parsed.password))
                            display_value = masked_url
                        else:
                            display_value = value
                    else:
                        display_value = value
                    
                    print(f"  {key}={display_value}")
            else:
                print(f"\n📄 {env_file}: Not found")
    
    def backup_config(self):
        """Backup current configuration."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"config_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        print(f"💾 Creating backup: {backup_name}")
        
        backed_up_files = []
        for env_file in self.env_files:
            source_path = self.project_root / env_file
            if source_path.exists():
                dest_path = backup_path / env_file
                shutil.copy2(source_path, dest_path)
                backed_up_files.append(env_file)
        
        # Create backup metadata
        metadata = {
            "timestamp": timestamp,
            "files": backed_up_files,
            "description": f"Configuration backup created on {datetime.now().isoformat()}"
        }
        
        with open(backup_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Backup created: {backup_path}")
        print(f"📁 Backed up files: {', '.join(backed_up_files)}")
        
        return backup_name
    
    def list_backups(self):
        """List available backups."""
        print("📦 Available backups:")
        
        backups = []
        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("config_backup_"):
                metadata_file = backup_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    backups.append((backup_dir.name, metadata))
        
        if not backups:
            print("  No backups found.")
            return []
        
        backups.sort(key=lambda x: x[1]['timestamp'], reverse=True)
        
        for backup_name, metadata in backups:
            print(f"  📦 {backup_name}")
            print(f"     Created: {metadata['timestamp']}")
            print(f"     Files: {', '.join(metadata['files'])}")
        
        return [backup[0] for backup in backups]
    
    def restore_config(self, backup_name: str):
        """Restore configuration from backup."""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        metadata_file = backup_path / "metadata.json"
        if not metadata_file.exists():
            print(f"❌ Invalid backup: missing metadata")
            return False
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        print(f"🔄 Restoring configuration from: {backup_name}")
        print(f"📅 Created: {metadata['timestamp']}")
        
        # Create current backup before restoring
        current_backup = self.backup_config()
        print(f"💾 Current config backed up as: {current_backup}")
        
        # Restore files
        restored_files = []
        for env_file in metadata['files']:
            source_path = backup_path / env_file
            dest_path = self.project_root / env_file
            
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                restored_files.append(env_file)
        
        print(f"✅ Restored files: {', '.join(restored_files)}")
        return True

def main():
    parser = argparse.ArgumentParser(description="InvoiceGen Configuration Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # SSL commands
    subparsers.add_parser('ssl-disable', help='Disable SSL for local development')
    subparsers.add_parser('ssl-enable', help='Enable SSL for production')
    
    # Configuration commands
    subparsers.add_parser('validate', help='Validate current configuration')
    subparsers.add_parser('show', help='Show current configuration')
    
    # Backup commands
    subparsers.add_parser('backup', help='Backup current configuration')
    subparsers.add_parser('list-backups', help='List available backups')
    
    restore_parser = subparsers.add_parser('restore', help='Restore configuration from backup')
    restore_parser.add_argument('backup_name', help='Name of backup to restore')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    config_manager = ConfigManager()
    
    print("⚙️  InvoiceGen Configuration Manager")
    print("=" * 40)
    
    if args.command == 'ssl-disable':
        config_manager.disable_ssl()
    elif args.command == 'ssl-enable':
        config_manager.enable_ssl()
    elif args.command == 'validate':
        config_manager.validate_config()
    elif args.command == 'show':
        config_manager.show_config()
    elif args.command == 'backup':
        config_manager.backup_config()
    elif args.command == 'list-backups':
        config_manager.list_backups()
    elif args.command == 'restore':
        config_manager.restore_config(args.backup_name)
    
    print("\n🎉 Configuration management completed!")

if __name__ == "__main__":
    main()