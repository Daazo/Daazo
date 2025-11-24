import discord
from discord.ext import commands
from discord import app_commands
from main import bot
from brand_config import create_permission_denied_embed, create_owner_only_embed,  BOT_FOOTER, BrandColors, create_success_embed, create_error_embed, create_info_embed, create_command_embed, create_warning_embed
from main import has_permission, get_server_data, update_server_data, log_action

@bot.tree.command(name="setup", description="Configure bot settings")\n@app_commands.describe(\n    action="What to setup",
    value="Value to set",
    role="Role to assign",
    channel="Channel to set",
    category="Category for organized logging"
)
@app_commands.choices(action=[
    app_commands.Choice(name="main_moderator", value="main_moderator"),\n    app_commands.Choice(name="junior_moderator", value="junior_moderator"),\n    app_commands.Choice(name="welcome", value="welcome"),\n    app_commands.Choice(name="welcome_title", value="welcome_title"),\n    app_commands.Choice(name="welcome_image", value="welcome_image"),\n    app_commands.Choice(name="karma_channel", value="karma_channel"),\n    app_commands.Choice(name="ticket_support_role", value="ticket_support_role"),\n    app_commands.Choice(name="auto_role", value="auto_role")\n])\nasync def setup(\n    interaction: discord.Interaction,\n    action: str,\n    value: str = None,\n    role: discord.Role = None,\n    channel: discord.TextChannel = None,\n    category: discord.CategoryChannel = None\n):\n    # Check permissions\n    if action == "main_moderator":\n        if interaction.user.id != interaction.guild.owner_id:\n            await interaction.response.send_message(embed=create_owner_only_embed(), ephemeral=True)\n            return\n    else:\n        if not await has_permission(interaction, "main_moderator"):\n            await interaction.response.send_message(embed=create_permission_denied_embed("Main Moderator"), ephemeral=True)\n            return\n\n    server_data = await get_server_data(interaction.guild.id)\n\n    if action == "main_moderator":\n        if not role:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a role!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'main_moderator_role': str(role.id)})\n\n        embed = discord.Embed(\n            title="⚡ **Main Moderator Role Set**",
            description=f"**◆ Role:** {role.mention}\n**◆ Set by:** {interaction.user.mention}",
            color=BrandColors.PRIMARY
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Main moderator role set to {role.name} by {interaction.user}")\n\n    elif action == "junior_moderator":\n        if not role:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a role!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'junior_moderator_role': str(role.id)})\n\n        embed = discord.Embed(\n            title="⚡ **Junior Moderator Role Set**",
            description=f"**◆ Role:** {role.mention}\n**◆ Set by:** {interaction.user.mention}",
            color=BrandColors.PRIMARY
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Junior moderator role set to {role.name} by {interaction.user}")\n\n    elif action == "welcome":\n        if not channel:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a welcome channel!"), ephemeral=True)\n            return\n\n        # Store welcome settings\n        welcome_data = {\n            'welcome_channel': str(channel.id),\n            'welcome_message': value or f"Welcome {{user}} to {{server}}!",
        }

        # If image URL is provided, store it
        if value and ("http" in value.lower() and any(ext in value.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp'])):\n            # Extract message and image\n            parts = value.split('|')\n            if len(parts) == 2:\n                welcome_data['welcome_message'] = parts[0].strip()\n                welcome_data['welcome_image'] = parts[1].strip()\n            else:\n                welcome_data['welcome_image'] = value\n\n        await update_server_data(interaction.guild.id, welcome_data)\n\n        # Test welcome functionality\n        test_embed = discord.Embed(\n            title="💠 **Welcome System Test**",
            description=f"**◆ Channel:** {channel.mention}\n**◆ Message:** {welcome_data['welcome_message']}\n" +\n                       (f"**◆ Image/GIF:** ✓ Working properly" if welcome_data.get('welcome_image') else "**◆ Image/GIF:** None set"),\n            color=BrandColors.PRIMARY\n        )\n        if welcome_data.get('welcome_image'):\n            test_embed.set_image(url=welcome_data['welcome_image'])\n\n        test_embed.set_footer(text=f"{BOT_FOOTER} • Welcome system is ready!")\n        await interaction.response.send_message(embed=test_embed)\n\n    elif action == "welcome_title":\n        if not value:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a welcome title!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'welcome_title': value})\n\n        embed = discord.Embed(\n            title="💠 **Welcome Title Set**",
            description=f"**◆ Title:** {value}\n**◆ Set by:** {interaction.user.mention}\n\n*Use {{user}} and {{server}} placeholders*",
            color=BrandColors.PRIMARY
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Welcome title set by {interaction.user}")\n\n    elif action == "welcome_image":\n        if not value:\n            await interaction.response.send_message(embed=create_error_embed("Please specify an image URL for welcome messages!"), ephemeral=True)\n            return\n\n        # Basic URL validation\n        if not (value.startswith('http://') or value.startswith('https://')):\n            await interaction.response.send_message(embed=create_error_embed("Please provide a valid image URL (starting with http:// or https://)"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'welcome_image': value})\n\n        embed = discord.Embed(\n            title="💠 **Welcome Image Set**",
            description=f"**◆ Image URL:** {value}\n**◆ Set by:** {interaction.user.mention}",
            color=BrandColors.PRIMARY
        )
        embed.set_image(url=value)
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Welcome image set by {interaction.user}")\n\n    elif action == "prefix":\n        if not value:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a prefix!"), ephemeral=True)\n            return\n\n        if len(value) > 5:\n            await interaction.response.send_message(embed=create_error_embed("Prefix must be 5 characters or less!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'prefix': value})\n\n        embed = discord.Embed(\n            title="⚡ **Prefix Updated**",
            description=f"**◆ New Prefix:** `{value}`\n**◆ Set by:** {interaction.user.mention}",
            color=BrandColors.PRIMARY
        )
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Prefix set to '{value}' by {interaction.user}")\n\n    elif action == "karma_channel":\n        if not channel:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a channel for karma announcements!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'karma_channel': str(channel.id)})\n\n        embed = discord.Embed(\n            title="💠 **Karma Channel Set**",
            description=f"**◆ Karma milestone announcements will be sent to:** {channel.mention}",
            color=BrandColors.PRIMARY
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)

        await log_action(interaction.guild.id, "setup", f"✨ [KARMA SETUP] Karma channel set to {channel} by {interaction.user}")\n\n    elif action == "auto_role":\n        if not role:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a role for auto assignment!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'auto_role': str(role.id)})\n\n        embed = discord.Embed(\n            title="⚡ **Auto Role Set**",
            description=f"**◆ Role:** {role.mention}\n**◆ Set by:** {interaction.user.mention}\n\n*This role will be automatically assigned to new members.*",
            color=BrandColors.PRIMARY
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Auto role set to {role.name} by {interaction.user}")\n\n    elif action == "ticket_support_role":\n        if not role:\n            await interaction.response.send_message(embed=create_error_embed("Please specify a role for ticket support!"), ephemeral=True)\n            return\n\n        await update_server_data(interaction.guild.id, {'ticket_support_role': str(role.id)})\n\n        embed = discord.Embed(\n            title="🎫 **Ticket Support Role Set**",
            description=f"**◆ Role:** {role.mention}\n**◆ Set by:** {interaction.user.mention}\n\n*This role will be mentioned when tickets are created.*",
            color=BrandColors.PRIMARY
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild.id, "setup", f"⚙️ [SETUP] Ticket support role set to {role.name} by {interaction.user}"), create_success_embed, create_error_embed, create_info_embed, create_command_embed, create_warning_embed, create_permission_denied_embed, create_owner_only_embed
