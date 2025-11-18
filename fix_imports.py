#!/usr/bin/env python3
"""Fix incorrect imports from brand_config"""

import re
import os

FILES_TO_FIX = [
    "communication_commands.py",
    "moderation_commands.py",
    "xp_commands.py",
    "setup_commands.py",
    "reaction_roles.py",
    "ticket_system.py",
    "timeout_system.py",
    "timed_roles.py",
    "autorole.py",
    "security_system.py",
    "voice_commands.py",
]

def fix_file(filepath):
    """Fix imports in a file"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Pattern to match: from brand_config import BOT_FOOTER, BrandColors, <other things that shouldn't be there>
        # We want to split it into two lines:
        # from main import <things from main>
        # from brand_config import BOT_FOOTER, BrandColors
        
        # Find the problematic import line
        pattern = r'from brand_config import BOT_FOOTER, BrandColors(,.*)?'
        matches = re.findall(pattern, content)
        
        if matches:
            # Replace the problematic import
            content = re.sub(
                r'from brand_config import BOT_FOOTER, BrandColors, (.*)',
                r'from brand_config import BOT_FOOTER, BrandColors\nfrom main import \1',
                content
            )
        
        # Make sure we have the brand_config import after "from main import bot"
        if 'from brand_config import' not in content and 'from main import bot' in content:
            content = content.replace(
                'from main import bot',
                'from main import bot\nfrom brand_config import BOT_FOOTER, BrandColors'
            )
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {filepath}")
            return True
        else:
            print(f"⏭️  No fixes needed for {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

def main():
    print("🔧 Fixing Import Statements")
    print("=" * 50)
    
    fixed = 0
    for filepath in FILES_TO_FIX:
        if fix_file(filepath):
            fixed += 1
    
    print("=" * 50)
    print(f"✅ Fixed {fixed}/{len(FILES_TO_FIX)} files")

if __name__ == "__main__":
    main()
