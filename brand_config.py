# RXT ENGINE Brand Configuration
# Quantum Purple Theme - Advanced AI Core System

# Bot Information
BOT_NAME = "RXT ENGINE"
BOT_VERSION = "2.0.0"
BOT_TAGLINE = "Advanced AI Core • Quantum-Powered Community Management"
BOT_DESCRIPTION = "RXT ENGINE is an advanced AI core system operating inside a holographic engine. Built with futuristic quantum technology for complete server automation, security, and community management."
BOT_FOOTER = "⚡ RXT ENGINE • Quantum Core System"

# Owner Information
BOT_OWNER_ID = "1087619527166132234"
BOT_OWNER_NAME = "R!O</>"
BOT_OWNER_DESCRIPTION = "Founder and lead developer driving the creation, maintenance, and evolution of the RXT ENGINE platform."

# Director Information
BOT_DIRECTOR_ID = "1087619527166132234"
BOT_DIRECTOR_NAME = "TOKYO<3"
BOT_DIRECTOR_DESCRIPTION = "Leads core architecture, feature innovation, and system stability behind RXT ENGINE's automation ecosystem."

# Brand Colors - Quantum Purple Theme (Discord int format)
class BrandColors:
    # Primary Quantum Purple Theme
    PRIMARY = 0xA66BFF  # Quantum Purple (Main brand color)
    SECONDARY = 0xC78CFF  # Hyper Violet Glow
    ACCENT = 0xD6D6FF  # Electric White Glow
    NEON_EDGE = 0xE0C9FF  # Neon Edge Lines
    
    # Background & Panels
    BACKGROUND = 0x0D0D0F  # Deep Matte Black
    PANEL = 0x1A1A1D  # Carbon Grey
    
    # Status Colors (Neon variants to match theme)
    SUCCESS = 0x3DFFAA  # Hologram Green
    WARNING = 0xFFB84D  # Neon Amber
    DANGER = 0xFF3B5F  # Neon Red
    
    # Utility Colors
    INFO = 0xA66BFF  # Same as Primary
    NEUTRAL = 0x1A1A1D  # Same as Panel
    
    # Quantum Purple Gradient (for karma levels and progressive systems)
    GRADIENT_1 = 0x9370DB  # Medium Purple
    GRADIENT_2 = 0x9F7FFF  # Light Purple
    GRADIENT_3 = 0xA66BFF  # Quantum Purple (Primary)
    GRADIENT_4 = 0xB380FF  # Bright Violet
    GRADIENT_5 = 0xC78CFF  # Hyper Violet Glow
    GRADIENT_6 = 0xD6D6FF  # Electric White Glow
    GRADIENT_7 = 0xE0C9FF  # Neon Edge Lines
    GRADIENT_8 = 0x8A4FFF  # Deep Quantum
    GRADIENT_9 = 0x7B3FE4  # Royal Purple

# RGB Colors for Image Generation (PIL) - Quantum Purple Theme
class BrandColorsRGB:
    # Primary Quantum Purple Theme
    PRIMARY = (166, 107, 255)  # Quantum Purple
    SECONDARY = (199, 140, 255)  # Hyper Violet Glow
    ACCENT = (214, 214, 255)  # Electric White Glow
    NEON_EDGE = (224, 201, 255)  # Neon Edge Lines
    
    # Background & Panels
    BACKGROUND = (13, 13, 15)  # Deep Matte Black
    PANEL = (26, 26, 29)  # Carbon Grey
    
    # Status Colors
    SUCCESS = (61, 255, 170)  # Hologram Green
    WARNING = (255, 184, 77)  # Neon Amber
    DANGER = (255, 59, 95)  # Neon Red
    
    # Text Colors
    TEXT_PRIMARY = (255, 255, 255)  # Pure White
    TEXT_SECONDARY = (214, 214, 255)  # Electric White Glow
    TEXT_MUTED = (150, 150, 150)  # Medium Grey
    TEXT_NEON = (224, 201, 255)  # Neon Edge Glow

# Visual Elements - Geometric Tech Design
class VisualElements:
    # Circuit Line Dividers
    CIRCUIT_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    THIN_LINE = "─────────────────────────────────────────────────"
    
    # Hologram Dots & Particles
    DOTS = "⬡ ⬢ ⬣"
    PARTICLES = "✦ ✧ ⚡ ◆ ◇"
    
    # System Icons
    SYSTEM_ONLINE = "🟣"  # Purple dot
    SYSTEM_ACTIVE = "⚡"
    SYSTEM_CORE = "◆"
    QUANTUM_ICON = "💠"
    
    # Geometric Shapes
    HEXAGON = "⬡"
    DIAMOND = "◆"
    TRIANGLE = "▲"
    
    # Status Indicators
    STATUS_ONLINE = "🟣 ONLINE"
    STATUS_ACTIVE = "⚡ ACTIVE"
    STATUS_PROCESSING = "◆ PROCESSING"

# Embed Style Templates - Quantum Theme
class EmbedStyles:
    @staticmethod
    def success(title, description):
        """Success embed - Hologram Green"""
        return {
            "title": f"✓ {title}",
            "description": f"{description}\n{VisualElements.CIRCUIT_LINE}",
            "color": BrandColors.SUCCESS
        }
    
    @staticmethod
    def error(title, description):
        """Error embed - Neon Red"""
        return {
            "title": f"✗ {title}",
            "description": f"{description}\n{VisualElements.CIRCUIT_LINE}",
            "color": BrandColors.DANGER
        }
    
    @staticmethod
    def warning(title, description):
        """Warning embed - Neon Amber"""
        return {
            "title": f"⚠ {title}",
            "description": f"{description}\n{VisualElements.CIRCUIT_LINE}",
            "color": BrandColors.WARNING
        }
    
    @staticmethod
    def info(title, description):
        """Info embed - Quantum Purple"""
        return {
            "title": f"◆ {title}",
            "description": f"{description}\n{VisualElements.CIRCUIT_LINE}",
            "color": BrandColors.PRIMARY
        }
    
    @staticmethod
    def command(title, description):
        """Command execution embed - Quantum Purple"""
        return {
            "title": f"⚡ {title}",
            "description": f"{description}\n{VisualElements.CIRCUIT_LINE}",
            "color": BrandColors.PRIMARY
        }
    
    @staticmethod
    def quantum(title, description):
        """Quantum theme embed - Primary color with circuit lines"""
        return {
            "title": f"💠 {title}",
            "description": f"{description}\n{VisualElements.CIRCUIT_LINE}",
            "color": BrandColors.PRIMARY
        }

# Message Templates - AI Core Personality
class MessageTemplates:
    @staticmethod
    def permission_denied():
        return f"**◆ ACCESS DENIED**\n{VisualElements.CIRCUIT_LINE}\nInsufficient permissions to execute this command.\nRequired authorization level not met."
    
    @staticmethod
    def cooldown(seconds):
        return f"**⚡ SYSTEM COOLDOWN**\n{VisualElements.CIRCUIT_LINE}\nQuantum core recharging...\n**Retry in:** {seconds:.1f}s"
    
    @staticmethod
    def command_success(action):
        return f"**✓ COMMAND EXECUTED**\n{VisualElements.CIRCUIT_LINE}\n**Action:** {action}\n**Status:** {VisualElements.STATUS_ACTIVE}"
    
    @staticmethod
    def processing():
        return f"**◆ PROCESSING REQUEST**\n{VisualElements.CIRCUIT_LINE}\nQuantum core analyzing..."
    
    @staticmethod
    def system_ready():
        return f"**⚡ SYSTEM READY**\n{VisualElements.CIRCUIT_LINE}\nAll quantum systems operational."

# Bot Personality & Tone - Futuristic AI Core
PERSONALITY = {
    "core_identity": "Advanced AI Core System",
    "vibe": ["Futuristic", "Quantum-powered", "Automated", "Smart", "Clean", "Fast", "Responsive"],
    "tone": "Professional AI assistant - confident, efficient, minimal",
    "style": "Geometric lines + neon purple accents + circuit patterns",
    "voice": [
        "System notifications",
        "Clean status reports", 
        "Direct responses",
        "Quantum/holographic terminology"
    ],
    "visual_theme": [
        "Circuit-line dividers",
        "Hologram dots/particles",
        "Geometric shapes",
        "Neon scanlines",
        "Hexagon framing",
        "Glowing wireframes"
    ]
}

# Button Styles - Matching Logo Design
class ButtonStyles:
    """
    Button style guide for Discord components
    """
    # Primary - Quantum Purple
    PRIMARY = {
        "style": "primary",  # Discord's blue (we can't set custom colors for buttons)
        "emoji": "⚡",
        "description": "Main actions - Quantum Purple theme"
    }
    
    # Secondary - Carbon Grey with Purple Border
    SECONDARY = {
        "style": "secondary",  # Discord's grey
        "emoji": "◆",
        "description": "Secondary actions - Carbon Grey"
    }
    
    # Success - Hologram Green
    SUCCESS = {
        "style": "success",  # Discord's green
        "emoji": "✓",
        "description": "Confirmations - Hologram Green"
    }
    
    # Danger - Neon Red
    DANGER = {
        "style": "danger",  # Discord's red
        "emoji": "✗",
        "description": "Destructive actions - Neon Red"
    }

# Quantum Core System Messages
class SystemMessages:
    BOOT_UP = f"""
⚡ **QUANTUM CORE INITIALIZING**
{VisualElements.CIRCUIT_LINE}
◆ AI systems loading...
◆ Holographic engine calibrating...
◆ Neural networks synchronizing...
{VisualElements.CIRCUIT_LINE}
✓ **RXT ENGINE ONLINE**
    """
    
    SHUTDOWN = f"""
⚡ **QUANTUM CORE SHUTTING DOWN**
{VisualElements.CIRCUIT_LINE}
◆ Saving neural patterns...
◆ Disconnecting from matrix...
{VisualElements.CIRCUIT_LINE}
✓ **SAFE TO POWER OFF**
    """
    
    ERROR = f"""
✗ **SYSTEM ERROR DETECTED**
{VisualElements.CIRCUIT_LINE}
◆ Quantum core encountered an anomaly
◆ Error handlers active
◆ Attempting auto-recovery...
    """

# Permission Denied Embed Helpers
def create_permission_denied_embed(required_role: str):
    """Create a themed permission denied embed for Discord"""
    import discord
    error_embed = discord.Embed(
        title="◆ ACCESS DENIED",
        description=f"You don't have permission to use this command.\n**Required:** {required_role}",
        color=BrandColors.DANGER,
        timestamp=__import__('datetime').datetime.now()
    )
    error_embed.add_field(name=f"{VisualElements.CIRCUIT_LINE}", value="", inline=False)
    error_embed.set_footer(text=BOT_FOOTER)
    return error_embed

def create_owner_only_embed():
    """Create a themed owner-only embed"""
    import discord
    error_embed = discord.Embed(
        title="◆ OWNER ONLY",
        description="Only the server owner can perform this action.",
        color=BrandColors.DANGER,
        timestamp=__import__('datetime').datetime.now()
    )
    error_embed.add_field(name=f"{VisualElements.CIRCUIT_LINE}", value="", inline=False)
    error_embed.set_footer(text=BOT_FOOTER)
    return error_embed

# COMPREHENSIVE MESSAGE HELPERS - ALL MESSAGE TYPES THEMED
def create_success_embed(title: str, description: str = "", fields = None):
    """Success embed - Hologram Green with circuit lines"""
    import discord
    from datetime import datetime
    embed = discord.Embed(
        title=f"✓ {title}",
        description=description + f"\n{VisualElements.CIRCUIT_LINE}" if description else f"{VisualElements.CIRCUIT_LINE}",
        color=BrandColors.SUCCESS,
        timestamp=datetime.now()
    )
    if fields:
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_footer(text=BOT_FOOTER)
    return embed

def create_error_embed(title: str, description: str = "", fields = None):
    """Error embed - Neon Red with circuit lines"""
    import discord
    from datetime import datetime
    embed = discord.Embed(
        title=f"✗ {title}",
        description=description + f"\n{VisualElements.CIRCUIT_LINE}" if description else f"{VisualElements.CIRCUIT_LINE}",
        color=BrandColors.DANGER,
        timestamp=datetime.now()
    )
    if fields:
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_footer(text=BOT_FOOTER)
    return embed

def create_info_embed(title: str, description: str = "", fields = None):
    """Info embed - Quantum Purple with circuit lines"""
    import discord
    from datetime import datetime
    embed = discord.Embed(
        title=f"◆ {title}",
        description=description + f"\n{VisualElements.CIRCUIT_LINE}" if description else f"{VisualElements.CIRCUIT_LINE}",
        color=BrandColors.PRIMARY,
        timestamp=datetime.now()
    )
    if fields:
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_footer(text=BOT_FOOTER)
    return embed

def create_command_embed(title: str, description: str = "", fields = None):
    """Command execution embed - Quantum Purple with lightning bolt"""
    import discord
    from datetime import datetime
    embed = discord.Embed(
        title=f"⚡ {title}",
        description=description + f"\n{VisualElements.CIRCUIT_LINE}" if description else f"{VisualElements.CIRCUIT_LINE}",
        color=BrandColors.PRIMARY,
        timestamp=datetime.now()
    )
    if fields:
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_footer(text=BOT_FOOTER)
    return embed

def create_warning_embed(title: str, description: str = "", fields = None):
    """Warning embed - Neon Amber with circuit lines"""
    import discord
    from datetime import datetime
    embed = discord.Embed(
        title=f"⚠ {title}",
        description=description + f"\n{VisualElements.CIRCUIT_LINE}" if description else f"{VisualElements.CIRCUIT_LINE}",
        color=BrandColors.WARNING,
        timestamp=datetime.now()
    )
    if fields:
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=False)
    embed.set_footer(text=BOT_FOOTER)
    return embed
