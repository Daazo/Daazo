import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from main import bot
from brand_config import create_permission_denied_embed, create_owner_only_embed,  BOT_FOOTER, BrandColors, create_success_embed, create_error_embed, create_info_embed, create_command_embed, create_warning_embed
from main import has_permission, log_action
import os
from datetime import datetime, timedelta
import time

@bot.tree.command(name="say", description="Make the bot say something")\n@app_commands.describe(\n    message="Message to say",
    channel="Channel to send to (optional)",
    image="Image URL to attach (optional)",
    heading="Custom heading/title for the message (optional)"
)
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None, image: str = None, heading: str = None):
    if not await has_permission(interaction, "junior_moderator"):
        await interaction.response.send_message(embed=create_permission_denied_embed("Junior Moderator"), ephemeral=True)
        return

    target_channel = channel or interaction.channel

    # If heading or image is provided, send as embed
    if heading or image:
        embed = discord.Embed(
            title=heading if heading else None,
            description=message,
            color=BrandColors.INFO
        )
        if image:
            # Basic URL validation
            if image.startswith(('http://', 'https://')) and any(ext in image.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):\n                embed.set_image(url=image)\n            else:\n                await interaction.response.send_message(create_error_embed("Invalid image URL! Please provide a valid image URL.", ephemeral=True)\n                return\n\n        embed.set_footer(text=BOT_FOOTER, icon_url=bot.user.display_avatar.url)\n        await target_channel.send(embed=embed)\n    else:\n        await target_channel.send(message)\n\n    embed = discord.Embed(\n        title="✅ Message Sent",
        description=f"Message sent to {target_channel.mention}",
        color=BrandColors.SUCCESS
    )
    embed.set_footer(text=BOT_FOOTER)
    await interaction.response.send_message(embed=embed, ephemeral=True)

    await log_action(interaction.guild.id, "communication", f"💬 [SAY] Message sent to {target_channel.name} by {interaction.user}")\n\n@bot.tree.command(name="embed", description="Send a rich embed message")\n@app_commands.describe(\n    title="Embed title",
    description="Embed description",
    color="Embed color (hex or name)",
    channel="Channel to send to (optional)",
    image="Image URL to attach (optional)"
)
async def embed_command(
    interaction: discord.Interaction,
    title: str = None,
    description: str = None,
    color: str = "blue",
    channel: discord.TextChannel = None,
    image: str = None
):
    if not await has_permission(interaction, "junior_moderator"):
        await interaction.response.send_message(embed=create_permission_denied_embed("Junior Moderator"), ephemeral=True)
        return

    target_channel = channel or interaction.channel

    # Parse color
    color_map = {
        "red": 0xe74c3c,
        "green": 0x43b581,
        "blue": 0x3498db,
        "yellow": 0xf1c40f,
        "purple": 0x9b59b6,
        "orange": 0xe67e22
    }

    if color.lower() in color_map:
        embed_color = color_map[color.lower()]
    elif color.startswith("#"):
        try:
            embed_color = int(color[1:], 16)
        except:
            embed_color = 0x3498db
    else:
        embed_color = 0x3498db

    embed = discord.Embed(color=embed_color)

    if title:
        embed.title = title
    if description:
        embed.description = description
    
    if image:
        # Basic URL validation
        if image.startswith(('http://', 'https://')) and any(ext in image.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):\n            embed.set_image(url=image)\n        else:\n            await interaction.response.send_message(create_error_embed("Invalid image URL! Please provide a valid image URL.", ephemeral=True)\n            return\n\n    embed.set_footer(text=BOT_FOOTER, icon_url=bot.user.display_avatar.url)\n\n    await target_channel.send(embed=embed)\n\n    response_embed = discord.Embed(\n        title="✅ Embed Sent",
        description=f"Embed sent to {target_channel.mention}",
        color=BrandColors.SUCCESS
    )
    response_embed.set_footer(text=BOT_FOOTER)
    await interaction.response.send_message(embed=response_embed, ephemeral=True)

    await log_action(interaction.guild.id, "communication", f"📝 [EMBED] Embed sent to {target_channel.name} by {interaction.user}")\n\n@bot.tree.command(name="announce", description="Send an announcement")\n@app_commands.describe(\n    channel="Channel to announce in",
    message="Announcement message",
    mention="Role or @everyone to mention (optional)",
    image="Image URL to attach (optional)",
    heading="Custom announcement heading (default: Server Announcement)"
)
async def announce(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    message: str,
    mention: str = None,
    image: str = None,
    heading: str = None
):
    if not await has_permission(interaction, "main_moderator"):
        await interaction.response.send_message(embed=create_permission_denied_embed("Main Moderator"), ephemeral=True)
        return

    announcement_content = ""

    if mention:
        if mention.lower() == "@everyone":
            announcement_content = "@everyone\n"
        else:
            # Try to find role by name
            role = discord.utils.get(interaction.guild.roles, name=mention)
            if role:
                announcement_content = f"{role.mention}\n"

    # Use custom heading or default
    announcement_title = heading if heading else "📢 **Server Announcement** 📢"
    
    embed = discord.Embed(
        title=announcement_title,
        description=message,
        color=BrandColors.WARNING
    )
    
    if image:
        # Basic URL validation
        if image.startswith(('http://', 'https://')) and any(ext in image.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):\n            embed.set_image(url=image)\n        else:\n            await interaction.response.send_message(create_error_embed("Invalid image URL! Please provide a valid image URL.", ephemeral=True)\n            return\n\n    embed.set_footer(text=BOT_FOOTER, icon_url=bot.user.display_avatar.url)\n\n    await channel.send(announcement_content, embed=embed)\n\n    response_embed = discord.Embed(\n        title="✅ Announcement Sent",
        description=f"Announcement sent to {channel.mention}",
        color=BrandColors.SUCCESS
    )
    response_embed.set_footer(text=BOT_FOOTER)
    await interaction.response.send_message(embed=response_embed, ephemeral=True)

    await log_action(interaction.guild.id, "communication", f"📢 [ANNOUNCEMENT] Announcement sent to {channel.name} by {interaction.user}")\n\n@bot.tree.command(name="poll", description="Create a poll")\n@app_commands.describe(\n    question="Poll question",
    option1="First option",
    option2="Second option",
    option3="Third option (optional)",
    option4="Fourth option (optional)"
)
async def poll(
    interaction: discord.Interaction,
    question: str,
    option1: str,
    option2: str,
    option3: str = None,
    option4: str = None
):
    if not await has_permission(interaction, "junior_moderator"):
        await interaction.response.send_message(embed=create_permission_denied_embed("Junior Moderator"), ephemeral=True)
        return

    options = [option1, option2]
    if option3:
        options.append(option3)
    if option4:
        options.append(option4)

    embed = discord.Embed(
        title="📊 Poll",
        description=f"**{question}**\n\n" + "\n".join([f"{chr(0x1f1e6 + i)} {option}" for i, option in enumerate(options)]),\n        color=BrandColors.INFO\n    )\n    embed.set_footer(text=BOT_FOOTER, icon_url=bot.user.display_avatar.url)\n\n    await interaction.response.send_message(embed=embed)\n    message = await interaction.original_response()\n\n    # Add reactions\n    for i in range(len(options)):\n        await message.add_reaction(chr(0x1f1e6 + i))\n\n    await log_action(interaction.guild.id, "communication", f"📊 [POLL] Poll created by {interaction.user}: {question}")\n\n@bot.tree.command(name="reminder", description="Set a reminder")\n@app_commands.describe(\n    message="Reminder message",
    time="Time (e.g., 1h30m, 45s, 2h)"
)
async def reminder(interaction: discord.Interaction, message: str, time: str):
    if not await has_permission(interaction, "junior_moderator"):
        await interaction.response.send_message(embed=create_permission_denied_embed("Junior Moderator"), ephemeral=True)
        return

    # Parse time
    import re
    time_regex = re.compile(r'(\d+)([smhd])')
    matches = time_regex.findall(time.lower())

    if not matches:
        await interaction.response.send_message(create_error_embed("Invalid time format! Use format like: 1h30m, 45s, 2h", ephemeral=True)
        return

    total_seconds = 0
    for amount, unit in matches:
        amount = int(amount)
        if unit == 's':
            total_seconds += amount
        elif unit == 'm':
            total_seconds += amount * 60
        elif unit == 'h':
            total_seconds += amount * 3600
        elif unit == 'd':
            total_seconds += amount * 86400

    if total_seconds > 86400 * 7:  # Max 7 days
        await interaction.response.send_message(create_error_embed("Maximum reminder time is 7 days!", ephemeral=True)
        return

    embed = discord.Embed(
        title="⏰ Reminder Set",
        description=f"I'll remind you about: **{message}**\nIn: **{time}**",
        color=BrandColors.SUCCESS
    )
    embed.set_footer(text=BOT_FOOTER)
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # Set reminder
    await asyncio.sleep(total_seconds)

    reminder_content = f"**{message}**"
    reminder_embed = discord.Embed(
        title="⏰ Reminder",
        description=reminder_content,
        color=BrandColors.WARNING
    )
    reminder_embed.set_footer(text=BOT_FOOTER)

    try:
        await interaction.user.send(embed=reminder_embed)
        # Log DM sent
        from advanced_logging import log_dm_sent
        await log_dm_sent(interaction.user, reminder_content, interaction.guild)
    except:
        # If DM fails, try to send in channel
        try:
            await interaction.followup.send(f"{interaction.user.mention}", embed=reminder_embed)\n        except:\n            pass\n\n@bot.tree.command(name="dm", description="Send a DM to a user")\n@app_commands.describe(user="User to send DM to", message="Message to send")\nasync def dm_command(interaction: discord.Interaction, user: discord.Member, message: str):\n    if not await has_permission(interaction, "main_moderator"):\n        await interaction.response.send_message(embed=create_permission_denied_embed("Main Moderator"), ephemeral=True)\n        return\n\n    try:\n        embed = discord.Embed(\n            title=f"📩 Message from {interaction.guild.name}",
            description=message,
            color=BrandColors.INFO
        )
        embed.set_footer(text=BOT_FOOTER)

        await user.send(embed=embed)
        # Log DM sent
        from advanced_logging import log_dm_sent
        await log_dm_sent(user, message, interaction.guild)

        response_embed = discord.Embed(
            title="✅ DM Sent",
            description=f"DM sent to {user.mention}",
            color=BrandColors.SUCCESS
        )
        response_embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=response_embed, ephemeral=True)

        await log_action(interaction.guild.id, "communication", f"📨 [DM] DM sent to {user} by {interaction.user}")\n\n    except discord.Forbidden:\n        await interaction.response.send_message(create_error_embed("Cannot send DM to this user (DMs might be disabled)", ephemeral=True)\n    except Exception as e:\n        await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)\n\n# Help and contact commands are handled in main.py to avoid duplicates\n\n@bot.event\nasync def on_message(message):\n    if message.author == bot.user:\n        return\n\n    # Reaction Role Setup Command\n    if message.content.startswith("reaction role setup"):\n        if not await has_permission(message, "main_moderator"):\n            await message.channel.send("Main Moderator")\n            return\n\n        await message.channel.send("Please provide the message, emoji, role, and channel for the reaction role.")\n        await message.channel.send("Optional: Specify if 'remove role' should be enabled and the role to remove.")\n\n        def check(m):\n            return m.author == message.author and m.channel == message.channel\n\n        try:\n            # Get message\n            msg_prompt = await bot.wait_for("message", check=check, timeout=60)\n            message_content = msg_prompt.content\n            message_to_react = await bot.get_channel(message.channel.id).fetch_message(int(message_content.split(' ')[0])) # Assuming message ID is first\n\n            # Get emoji\n            emoji_prompt = await bot.wait_for("message", check=check, timeout=60)\n            emoji_str = emoji_prompt.content\n\n            # Get role\n            role_prompt = await bot.wait_for("message", check=check, timeout=60)\n            role_name = role_prompt.content\n            guild = message.guild\n            role = discord.utils.get(guild.roles, name=role_name)\n            if not role:\n                await message.channel.send(f"❌ Role '{role_name}' not found.")\n                return\n\n            # Get channel\n            channel_prompt = await bot.wait_for("message", check=check, timeout=60)\n            channel_name = channel_prompt.content\n            target_channel = discord.utils.get(guild.text_channels, name=channel_name)\n            if not target_channel:\n                await message.channel.send(f"❌ Channel '{channel_name}' not found.")\n                return\n\n            # Get remove role option\n            remove_role_prompt = await bot.wait_for("message", check=check, timeout=60)\n            remove_role_enabled = remove_role_prompt.content.lower() == 'yes'
            role_to_remove = None

            if remove_role_enabled:
                remove_role_prompt_2 = await bot.wait_for("message", check=check, timeout=60)
                role_to_remove_name = remove_role_prompt_2.content
                role_to_remove = discord.utils.get(guild.roles, name=role_to_remove_name)
                if not role_to_remove:
                    await message.channel.send(f"❌ Role to remove '{role_to_remove_name}' not found.")\n                    return\n\n            # Add reaction to the message\n            try:\n                await message_to_react.add_reaction(emoji_str)\n            except discord.HTTPException:\n                await message.channel.send("❌ Invalid emoji provided.")\n                return\n\n            # Store reaction role data (you'll need a persistent storage for this)\n            # For now, we'll just log it\n            log_data = {\n                "message_id": message_to_react.id,\n                "emoji": emoji_str,\n                "role_id": role.id,\n                "channel_id": target_channel.id,\n                "remove_role_enabled": remove_role_enabled,\n                "role_to_remove_id": role_to_remove.id if role_to_remove else None\n            }\n            print(f"Reaction role setup: {log_data}") # Replace with actual storage\n\n            await message.channel.send("Reaction role setup complete!")\n\n        except asyncio.TimeoutError:\n            await message.channel.send("❌ Timeout. Please try the command again.")\n        except Exception as e:\n            await message.channel.send(f"❌ An error occurred: {e}")\n\n\n\n@bot.event\nasync def on_raw_reaction_add(payload: discord.RawReactionActionEvent):\n    if payload.user_id == bot.user.id:\n        return\n\n    # Retrieve reaction role data (replace with your actual storage retrieval)\n    # Example: reaction_roles = get_reaction_roles_from_storage()\n    reaction_roles = {\n        # message_id: {"emoji": emoji_str, "role_id": role_id, "channel_id": channel_id, "remove_role_enabled": bool, "role_to_remove_id": role_to_remove_id}\n    }\n    # Dummy data for testing, replace with actual storage\n    # This needs to be populated when the reaction role setup command is used\n    # For example:\n    # reaction_roles[123456789012345678] = {"emoji": "👍", "role_id": 987654321098765432, "channel_id": 112233445566778899, "remove_role_enabled": False, "role_to_remove_id": None}\n    # reaction_roles[876543210987654321] = {"emoji": "⭐", "role_id": 123456789012345678, "channel_id": 112233445566778899, "remove_role_enabled": True, "role_to_remove_id": 101010101010101010}\n\n\n    if payload.message_id in reaction_roles:\n        role_data = reaction_roles[payload.message_id]\n        guild = bot.get_guild(payload.guild_id)\n        member = guild.get_member(payload.user_id)\n        emoji = str(payload.emoji)\n\n        if emoji == role_data["emoji"]:\n            role_to_assign = guild.get_role(role_data["role_id"])\n            if not role_to_assign:\n                return\n\n            if role_data["remove_role_enabled"]:\n                role_to_remove = guild.get_role(role_data["role_to_remove_id"])\n                if role_to_remove and role_to_remove in member.roles:\n                    await member.remove_roles(role_to_remove)\n                    print(f"Assigned role {role_to_assign.name} to {member.display_name}") # Logging\n\n            if role_to_assign not in member.roles:\n                await member.add_roles(role_to_assign)\n                print(f"Assigned role {role_to_assign.name} to {member.display_name}") # Logging\n\n@bot.event\nasync def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):\n    if payload.user_id == bot.user.id:\n        return\n\n    # Retrieve reaction role data (replace with your actual storage retrieval)\n    reaction_roles = {\n        # message_id: {"emoji": emoji_str, "role_id": role_id, "channel_id": channel_id, "remove_role_enabled": bool, "role_to_remove_id": role_to_remove_id}\n    }\n    # Dummy data for testing, replace with actual storage\n\n    if payload.message_id in reaction_roles:\n        role_data = reaction_roles[payload.message_id]\n        guild = bot.get_guild(payload.guild_id)\n        member = guild.get_member(payload.user_id)\n        emoji = str(payload.emoji)\n\n        if emoji == role_data["emoji"]:\n            role_to_assign = guild.get_role(role_data["role_id"])\n            if not role_to_assign:\n                return\n\n            if role_to_assign in member.roles:\n                await member.remove_roles(role_to_assign)\n                print(f"Removed role {role_to_assign.name} from {member.display_name}") # Logging\n\n            if role_data["remove_role_enabled"]:\n                role_to_remove = guild.get_role(role_data["role_to_remove_id"])\n                if role_to_remove and role_to_remove in member.roles:\n                    await member.remove_roles(role_to_remove)\n                    print(f"Removed role {role_to_remove.name} from {member.display_name}") # Logging\n\n# Contact command is handled in main.py to avoid duplicates
