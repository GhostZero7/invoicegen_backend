#!/usr/bin/env python3
"""Fix context access in GraphQL files"""

import os
import re

def fix_file(filepath):
    """Fix context access in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace user context access
        content = re.sub(r'info\.context\.get\("user"\)', 'info.context.get("current_user")', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {filepath}")
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

# Fix all GraphQL files
graphql_dirs = [
    'app/graphql/queries',
    'app/graphql/mutations'
]

for directory in graphql_dirs:
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.py') and filename != '__init__.py':
                filepath = os.path.join(directory, filename)
                fix_file(filepath)

print("Done!")