
import discord
from discord.ext import commands, tasks
import asyncio
import traceback
from datetime import datetime
import json
from main import bot, BOT_SUPPORT_SERVER_ID, BOT_LOGS_CATEGORY_ID

# Channel IDs for different log types (will be set when channels are created)
LOG_CHANNELS = {
    'server_activity': None,    # All server activity logs
    'dm_logs': None,           # DM messages to bot
    'error_logs': None,        # Bot errors and exceptions
    'server_list': None        # Live server list updates
}

async def setup_support_server_logging():
    """Setup logging channels in the support server"""
    try:
        support_guild = bot.get_guild(BOT_SUPPORT_SERVER_ID)
        if not support_guild:
            print(f"❌ Support server not found: {BOT_SUPPORT_SERVER_ID}")
            return
        
        category = support_guild.get_channel(BOT_LOGS_CATEGORY_ID)
        if not category:
            print(f"❌ Logs category not found: {BOT_LOGS_CATEGORY_ID}")
            return
        
        # Create log channels if they don't exist
        channels_to_create = [
            ('📊-server-activity-logs', 'All server activity from all servers where bot is active 🌐'),
            ('💬-dm-message-logs', 'All DM messages sent to the bot from users 📨'),
            ('❌-bot-error-logs', 'All bot errors, exceptions, and system issues 🚨'),
            ('🌍-live-server-list', 'Real-time list of all servers where bot is active 📋')
        ]
        
        for channel_name, description in channels_to_create:
            existing_channel = discord.utils.get(category.channels, name=channel_name)
            if not existing_channel:
                channel = await support_guild.create_text_channel(
                    name=channel_name,
                    category=category,
                    topic=description
                )
                
                # Store channel IDs
                log_type = channel_name.split('-')[1]  # Extract key from name
                if log_type == 'server':
                    LOG_CHANNELS['server_activity'] = channel.id
                elif log_type == 'dm':
                    LOG_CHANNELS['dm_logs'] = channel.id
                elif log_type == 'bot':
                    LOG_CHANNELS['error_logs'] = channel.id
                elif log_type == 'live':
                    LOG_CHANNELS['server_list'] = channel.id
                
                # Send initial setup message
                embed = discord.Embed(
                    title=f"🌴 **{channel_name.replace('-', ' ').title()}**",
                    description=f"**{description}**\n\n*This channel will receive real-time logs from all servers.*\n\n**🤖 Bot:** {bot.user.mention}\n**Setup time:** {discord.utils.format_dt(discord.utils.utcnow())}",
                    color=0x43b581
                )
                embed.set_footer(text="🌴 ᴠᴀᴀᴢʜᴀ Support Server Logging", icon_url=bot.user.display_avatar.url)
                await channel.send(embed=embed)
            else:
                # Store existing channel IDs
                log_type = channel_name.split('-')[1]
                if log_type == 'server':
                    LOG_CHANNELS['server_activity'] = existing_channel.id
                elif log_type == 'dm':
                    LOG_CHANNELS['dm_logs'] = existing_channel.id
                elif log_type == 'bot':
                    LOG_CHANNELS['error_logs'] = existing_channel.id
                elif log_type == 'live':
                    LOG_CHANNELS['server_list'] = existing_channel.id
        
        print("✅ Support server logging channels setup complete!")
        
        # Start the server list updater
        update_server_list.start()
        
    except Exception as e:
        print(f"❌ Error setting up support server logging: {e}")

async def log_to_support_server(log_type: str, message: str, guild_name: str = None, user: discord.User = None):
    """Send logs to support server channels"""
    try:
        if log_type not in LOG_CHANNELS or not LOG_CHANNELS[log_type]:
            return
        
        support_guild = bot.get_guild(BOT_SUPPORT_SERVER_ID)
        if not support_guild:
            return
        
        channel = support_guild.get_channel(LOG_CHANNELS[log_type])
        if not channel:
            return
        
        # Create appropriate embed based on log type
        if log_type == 'server_activity':
            color = 0x3498db
            title = f"📊 Server Activity - {guild_name}"
        elif log_type == 'dm_logs':
            color = 0x9b59b6
            title = f"💬 DM Message - {user.display_name if user else 'Unknown'}"
        elif log_type == 'error_logs':
            color = 0xe74c3c
            title = "❌ Bot Error"
        else:
            color = 0x95a5a6
            title = "📋 System Log"
        
        embed = discord.Embed(
            title=title,
            description=message,
            color=color,
            timestamp=datetime.now()
        )
        
        if user:
            embed.set_footer(text=f"User ID: {user.id}", icon_url=user.display_avatar.url)
        else:
            embed.set_footer(text="🌴 ᴠᴀᴀᴢʜᴀ Logs", icon_url=bot.user.display_avatar.url)
        
        await channel.send(embed=embed)
        
    except Exception as e:
        print(f"❌ Error logging to support server: {e}")

@tasks.loop(minutes=5)
async def update_server_list():
    """Update the live server list every 5 minutes"""
    try:
        if not LOG_CHANNELS['server_list']:
            return
        
        support_guild = bot.get_guild(BOT_SUPPORT_SERVER_ID)
        if not support_guild:
            return
        
        channel = support_guild.get_channel(LOG_CHANNELS['server_list'])
        if not channel:
            return
        
        # Get all servers
        servers = []
        total_members = 0
        
        for guild in bot.guilds:
            servers.append({
                'name': guild.name,
                'id': guild.id,
                'members': guild.member_count,
                'owner': str(guild.owner) if guild.owner else 'Unknown'
            })
            total_members += guild.member_count
        
        # Sort by member count
        servers.sort(key=lambda x: x['members'], reverse=True)
        
        # Create server list embed
        embed = discord.Embed(
            title="🌍 **Live Server List** 📋",
            description=f"**Total Servers:** `{len(servers)}`\n**Total Members:** `{total_members:,}`\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            color=0x43b581,
            timestamp=datetime.now()
        )
        
        # Add top servers
        server_list = ""
        for i, server in enumerate(servers[:15]):  # Show top 15 servers
            server_list += f"**{i+1}.** {server['name']}\n🆔 `{server['id']}`\n👥 {server['members']:,} members\n👑 {server['owner']}\n\n"
        
        if len(servers) > 15:
            server_list += f"*... and {len(servers) - 15} more servers*"
        
        embed.add_field(
            name="📈 **Top Servers by Member Count**",
            value=server_list if server_list else "No servers",
            inline=False
        )
        
        embed.set_footer(text="🌴 Updated every 5 minutes", icon_url=bot.user.display_avatar.url)
        
        # Delete previous messages and send new one
        async for message in channel.history(limit=5):
            if message.author == bot.user:
                await message.delete()
        
        await channel.send(embed=embed)
        
    except Exception as e:
        print(f"❌ Error updating server list: {e}")
        await log_error_to_support(f"Server list update error: {str(e)}")

async def log_error_to_support(error_message: str, guild_name: str = None):
    """Log errors to support server"""
    await log_to_support_server('error_logs', error_message, guild_name)

async def log_dm_to_support(user: discord.User, message_content: str):
    """Log DM messages to support server"""
    dm_log = f"**Message:** {message_content}\n**User:** {user} ({user.id})\n**Account Created:** {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    await log_to_support_server('dm_logs', dm_log, user=user)

async def log_server_activity_to_support(guild_name: str, activity_message: str):
    """Log server activity to support server"""
    await log_to_support_server('server_activity', activity_message, guild_name)

# Override the existing log_action function to also send to support server
original_log_action = None

async def enhanced_log_action(guild_id, log_type, message):
    """Enhanced log action that also sends to support server"""
    # Call original log_action
    if original_log_action:
        await original_log_action(guild_id, log_type, message)
    
    # Get guild name
    guild = bot.get_guild(int(guild_id))
    guild_name = guild.name if guild else f"Guild {guild_id}"
    
    # Send to support server
    await log_server_activity_to_support(guild_name, f"**{log_type.upper()}:** {message}")

# Setup when bot is ready
@bot.event
async def on_ready_support_logging():
    """Setup support server logging when bot is ready"""
    global original_log_action
    
    # Store original log_action function
    from main import log_action
    original_log_action = log_action
    
    # Replace with enhanced version
    import main
    main.log_action = enhanced_log_action
    
    # Setup channels
    await setup_support_server_logging()

# Error handler for comprehensive error logging
@bot.event
async def on_error_support_logging(event, *args, **kwargs):
    """Log all bot errors to support server"""
    error_msg = f"**Event:** {event}\n**Error:** {traceback.format_exc()}"
    await log_error_to_support(error_msg)

# Command error handler
@bot.event
async def on_command_error_support_logging(ctx, error):
    """Log command errors to support server"""
    error_msg = f"**Command:** {ctx.command}\n**User:** {ctx.author} ({ctx.author.id})\n**Guild:** {ctx.guild.name if ctx.guild else 'DM'}\n**Error:** {str(error)}"
    await log_error_to_support(error_msg, ctx.guild.name if ctx.guild else "DM")

# Application command error handler
@bot.tree.on_error
async def on_app_command_error_support_logging(interaction: discord.Interaction, error):
    """Log application command errors to support server"""
    error_msg = f"**Command:** {interaction.command.name if interaction.command else 'Unknown'}\n**User:** {interaction.user} ({interaction.user.id})\n**Guild:** {interaction.guild.name if interaction.guild else 'DM'}\n**Error:** {str(error)}"
    await log_error_to_support(error_msg, interaction.guild.name if interaction.guild else "DM")

print("✅ Support server logging system loaded")
