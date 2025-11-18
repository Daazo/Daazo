# RXT ENGINE Brand Configuration
# Complete theming system for the bot

# Bot Information
BOT_NAME = "RXT ENGINE"
BOT_VERSION = "2.0.0"
BOT_TAGLINE = "RXT ENGINE — Powering Every Corner of Your Community"
BOT_DESCRIPTION = "RXT ENGINE is a powerful multi-function Discord bot built for automation, moderation, music, utilities, security, and more — engineered to keep your server fast, stable, and perfectly managed."
BOT_FOOTER = "RXT ENGINE • Powered by R!O</>"

# Brand Colors (Hex to Discord int conversion)
class BrandColors:
    # Primary Colors
    PRIMARY = 0x8A4FFF  # Quantum Purple
    SECONDARY = 0x4F8CFF  # Hyper Blue
    ACCENT = 0xB86BFF  # Soft Neon Violet
    
    # Background Colors
    BACKGROUND = 0x0E0E11  # Matte Black
    HIGHLIGHT = 0x2A2A2F  # Carbon Grey
    
    # Status Colors
    SUCCESS = 0x00E68A  # Success Green
    WARNING = 0xFFB84D  # Warning Orange
    DANGER = 0xFF4D4D  # Danger Red
    
    # Utility Colors
    INFO = 0x4F8CFF  # Same as Secondary
    NEUTRAL = 0x2A2A2F  # Same as Highlight

# RGB Colors for Image Generation (PIL)
class BrandColorsRGB:
    # Primary Colors
    PRIMARY = (138, 79, 255)  # Quantum Purple
    SECONDARY = (79, 140, 255)  # Hyper Blue
    ACCENT = (184, 107, 255)  # Soft Neon Violet
    
    # Background Colors
    BACKGROUND = (14, 14, 17)  # Matte Black
    HIGHLIGHT = (42, 42, 47)  # Carbon Grey
    
    # Status Colors
    SUCCESS = (0, 230, 138)  # Success Green
    WARNING = (255, 184, 77)  # Warning Orange
    DANGER = (255, 77, 77)  # Danger Red
    
    # Text Colors
    TEXT_PRIMARY = (255, 255, 255)  # White
    TEXT_SECONDARY = (200, 200, 200)  # Light Grey
    TEXT_MUTED = (150, 150, 150)  # Medium Grey

# Embed Style Templates
class EmbedStyles:
    @staticmethod
    def success(title, description):
        """Success embed template"""
        return {
            "title": f"✅ {title}",
            "description": description,
            "color": BrandColors.SUCCESS
        }
    
    @staticmethod
    def error(title, description):
        """Error embed template"""
        return {
            "title": f"❌ {title}",
            "description": description,
            "color": BrandColors.DANGER
        }
    
    @staticmethod
    def warning(title, description):
        """Warning embed template"""
        return {
            "title": f"⚠️ {title}",
            "description": description,
            "color": BrandColors.WARNING
        }
    
    @staticmethod
    def info(title, description):
        """Info embed template"""
        return {
            "title": f"ℹ️ {title}",
            "description": description,
            "color": BrandColors.INFO
        }
    
    @staticmethod
    def command(title, description):
        """Command execution embed template"""
        return {
            "title": f"🚀 {title}",
            "description": description,
            "color": BrandColors.PRIMARY
        }

# Message Templates
class MessageTemplates:
    @staticmethod
    def permission_denied():
        return "**Access Denied**\nYou don't have the required permissions to use this command."
    
    @staticmethod
    def cooldown(seconds):
        return f"**Cooldown Active**\nPlease wait **{seconds:.1f}s** before using this command again."
    
    @staticmethod
    def command_success(action):
        return f"**Command Executed Successfully**\n**Action:** {action}\n**Status:** Completed ⚡"

# Bot Personality & Tone
PERSONALITY = {
    "vibe": ["Futuristic", "Fast", "Clean", "Professional", "AI-powered assistant"],
    "tone": "Short, confident, uses bold text and emojis",
    "style": "Title → Body → Footer"
}
