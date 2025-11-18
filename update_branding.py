#!/usr/bin/env python3
"""Script to update all files with new RXT ENGINE branding"""

import os
import re

# Files to update
FILES_TO_UPDATE = [
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
    "profile_cards.py",
    "global_logging.py",
    "voice_commands.py",
]

# Replacements to make
REPLACEMENTS = [
    # Import brand config at the top of files that need it
    ('from main import bot', 'from main import bot\nfrom brand_config import BOT_FOOTER, BrandColors'),
    
    # Footer replacements
    ('text="ᴠᴀᴀᴢʜᴀ"', 'text=BOT_FOOTER'),
    ('text="ᴠᴀᴀᴢʜᴀ-ʙᴏᴛ"', 'text=BOT_FOOTER'),
    ('text="🌴 ᴠᴀᴀᴢʜᴀ"', 'text=BOT_FOOTER'),
    ('text="VAAZHA"', 'text=BOT_FOOTER'),
    
    # Color replacements (common ones)
    ('color=0x3498db', 'color=BrandColors.INFO'),
    ('color=0xe74c3c', 'color=BrandColors.DANGER'),
    ('color=0xf39c12', 'color=BrandColors.WARNING'),
    ('color=0x43b581', 'color=BrandColors.SUCCESS'),
    ('color=0x9b59b6', 'color=BrandColors.PRIMARY'),
    ('color=0xf1c40f', 'color=BrandColors.WARNING'),
    ('color=0xe67e22', 'color=BrandColors.ACCENT'),
]

def update_file(filepath):
    """Update a single file with new branding"""
    if not os.path.exists(filepath):
        print(f"⚠️  Skipping {filepath} (not found)")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated {filepath}")
            return True
        else:
            print(f"⏭️  No changes needed for {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main update function"""
    print("🚀 RXT ENGINE Branding Update Script")
    print("=" * 50)
    
    updated_count = 0
    for filepath in FILES_TO_UPDATE:
        if update_file(filepath):
            updated_count += 1
    
    print("=" * 50)
    print(f"✅ Complete! Updated {updated_count}/{len(FILES_TO_UPDATE)} files")

if __name__ == "__main__":
    main()
