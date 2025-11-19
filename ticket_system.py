import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta
from main import bot
from brand_config import BOT_FOOTER, BrandColors
from main import has_permission, get_server_data, update_server_data, log_action

class TicketModal(discord.ui.Modal, title='🎫 Create Support Ticket'):
    def __init__(self, category_id, server_data):
        super().__init__()
        self.category_id = category_id
        self.server_data = server_data
        self.field_values = {}
        
        ticket_fields = server_data.get('ticket_fields', None)
        
        if not ticket_fields:
            ticket_fields = [
                {'label': 'Name', 'placeholder': 'Enter your full name...', 'style': 'short', 'required': True, 'max_length': 100},
                {'label': 'Describe your issue', 'placeholder': 'Please describe your issue in detail...', 'style': 'long', 'required': True, 'max_length': 1000},
                {'label': 'Urgency', 'placeholder': 'Low, Medium, or High', 'style': 'short', 'required': True, 'max_length': 10}
            ]
        
        for idx, field_config in enumerate(ticket_fields[:10]):
            style = discord.TextStyle.long if field_config.get('style') == 'long' else discord.TextStyle.short
            field = discord.ui.TextInput(
                label=field_config.get('label', f'Field {idx + 1}'),
                placeholder=field_config.get('placeholder', ''),
                style=style,
                required=field_config.get('required', True),
                max_length=field_config.get('max_length', 1000)
            )
            setattr(self, f'field_{idx}', field)
            self.add_item(field)

    async def on_submit(self, interaction: discord.Interaction):
        server_data = await get_server_data(interaction.guild.id)
        ticket_cooldowns = server_data.get('ticket_cooldowns', {})
        user_id = str(interaction.user.id)

        if user_id in ticket_cooldowns:
            last_ticket = datetime.fromisoformat(ticket_cooldowns[user_id])
            if datetime.now() - last_ticket < timedelta(minutes=10):
                embed = discord.Embed(
                    title="⏳ Ticket Cooldown",
                    description="You must wait 10 minutes between creating tickets!",
                    color=BrandColors.WARNING
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        category = interaction.guild.get_channel(int(self.category_id))
        if not category:
            await interaction.response.send_message("❌ Ticket category not found!", ephemeral=True)
            return

        main_mod_role_id = server_data.get('main_moderator_role')
        junior_mod_role_id = server_data.get('junior_moderator_role')
        support_role_id = server_data.get('ticket_support_role')

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        if main_mod_role_id:
            main_mod_role = interaction.guild.get_role(int(main_mod_role_id))
            if main_mod_role:
                overwrites[main_mod_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        if junior_mod_role_id:
            junior_mod_role = interaction.guild.get_role(int(junior_mod_role_id))
            if junior_mod_role:
                overwrites[junior_mod_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        if support_role_id:
            support_role = interaction.guild.get_role(int(support_role_id))
            if support_role:
                overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_count = server_data.get('ticket_counter', 0) + 1
        await update_server_data(interaction.guild.id, {'ticket_counter': ticket_count})
        
        clean_username = ''.join(c for c in interaction.user.name if c.isalnum() or c in ['-', '_']).lower()[:20]
        channel_name = f"{clean_username}-{ticket_count}"
        
        ticket_channel = await category.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            topic=f"Support ticket #{ticket_count} for {interaction.user}"
        )

        embed = discord.Embed(
            title="🎟️ New Support Ticket",
            description=f"**Ticket created by:** {interaction.user.mention}\n**Ticket Number:** #{ticket_count}\n**Created at:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            color=BrandColors.INFO
        )
        
        ticket_fields = server_data.get('ticket_fields', None)
        if not ticket_fields:
            ticket_fields = [
                {'label': 'Name', 'placeholder': 'Enter your full name...', 'style': 'short', 'required': True, 'max_length': 100},
                {'label': 'Describe your issue', 'placeholder': 'Please describe your issue in detail...', 'style': 'long', 'required': True, 'max_length': 1000},
                {'label': 'Urgency', 'placeholder': 'Low, Medium, or High', 'style': 'short', 'required': True, 'max_length': 10}
            ]
        
        for idx, field_config in enumerate(ticket_fields[:10]):
            field_attr = getattr(self, f'field_{idx}', None)
            if field_attr:
                embed.add_field(
                    name=f"📋 {field_config.get('label', f'Field {idx + 1}')}",
                    value=field_attr.value or 'N/A',
                    inline=True if field_config.get('style') == 'short' else False
                )
        
        embed.set_footer(text="Support team will be with you shortly!")

        view = TicketControlView()

        support_role_id = server_data.get('ticket_support_role')
        mention_text = ""
        if support_role_id:
            support_role = interaction.guild.get_role(int(support_role_id))
            if support_role:
                mention_text = f"{support_role.mention} "

        await ticket_channel.send(mention_text, embed=embed, view=view)

        ticket_cooldowns[user_id] = datetime.now().isoformat()
        await update_server_data(interaction.guild.id, {'ticket_cooldowns': ticket_cooldowns})

        response_embed = discord.Embed(
            title="✅ Ticket Created Successfully",
            description=f"Your support ticket has been created: {ticket_channel.mention}\nTicket Number: #{ticket_count}\nOur team will assist you shortly!",
            color=BrandColors.SUCCESS
        )
        await interaction.response.send_message(embed=response_embed, ephemeral=True)

        field_summary = ', '.join([f"{getattr(self, f'field_{i}', discord.ui.TextInput(label='', placeholder='')).label}: {getattr(self, f'field_{i}', discord.ui.TextInput(label='', placeholder='')).value[:50]}" for i in range(len(ticket_fields[:10])) if hasattr(self, f'field_{i}')])
        await log_action(interaction.guild.id, "tickets", f"🎫 [TICKET OPENED] {interaction.user} - Ticket #{ticket_count}")

class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.danger, emoji='🔒', custom_id='ticket_close_button')
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has moderator permissions OR ticket support role
        has_mod_permission = await has_permission(interaction, "junior_moderator")

        server_data = await get_server_data(interaction.guild.id)
        support_role_id = server_data.get('ticket_support_role')
        has_support_role = False

        if support_role_id:
            support_role = interaction.guild.get_role(int(support_role_id))
            if support_role and support_role in interaction.user.roles:
                has_support_role = True

        if not has_mod_permission and not has_support_role:
            await interaction.response.send_message("❌ You need Junior Moderator permissions or Ticket Support role to close tickets!", ephemeral=True)
            return

        server_data = await get_server_data(interaction.guild.id)
        close_category_id = server_data.get('ticket_close_category')

        if not close_category_id:
            await interaction.response.send_message("❌ Ticket close category not set! Use `/setup ticketclose` first.", ephemeral=True)
            return

        close_category = interaction.guild.get_channel(int(close_category_id))
        if not close_category:
            await interaction.response.send_message("❌ Ticket close category not found!", ephemeral=True)
            return

        # Move channel to closed category
        await interaction.channel.edit(
            category=close_category,
            name=f"closed-{interaction.channel.name}"
        )

        # Remove user access
        for member in interaction.channel.members:
            if not await has_permission_user(member, interaction.guild, "junior_moderator"):
                await interaction.channel.set_permissions(member, read_messages=False)

        embed = discord.Embed(
            title="🔒 Ticket Closed",
            description=f"This ticket has been closed by {interaction.user.mention}",
            color=BrandColors.DANGER
        )

        reopen_delete_view = ReopenDeleteTicketView()
        await interaction.response.send_message(embed=embed, view=reopen_delete_view)

        await log_action(interaction.guild.id, "tickets", f"🔒 [TICKET CLOSED] {interaction.channel.name} by {interaction.user}")

class ReopenDeleteTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Reopen Ticket', style=discord.ButtonStyle.success, emoji='🔓', custom_id='ticket_reopen_button')
    async def reopen_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await has_permission(interaction, "junior_moderator"):
            await interaction.response.send_message("❌ You need Junior Moderator permissions or higher to reopen tickets!", ephemeral=True)
            return

        server_data = await get_server_data(interaction.guild.id)
        open_category_id = server_data.get('ticket_open_category')

        if not open_category_id:
            await interaction.response.send_message("❌ Ticket open category not set!", ephemeral=True)
            return

        open_category = interaction.guild.get_channel(int(open_category_id))
        if not open_category:
            await interaction.response.send_message("❌ Ticket open category not found!", ephemeral=True)
            return

        new_name = interaction.channel.name.replace("closed-", "")
        await interaction.channel.edit(
            category=open_category,
            name=new_name
        )

        embed = discord.Embed(
            title="🔓 Ticket Reopened",
            description=f"This ticket has been reopened by {interaction.user.mention}",
            color=BrandColors.SUCCESS
        )

        close_view = TicketControlView()
        await interaction.response.send_message(embed=embed, view=close_view)

        await log_action(interaction.guild.id, "tickets", f"🔓 [TICKET REOPENED] {interaction.channel.name} by {interaction.user}")
    
    @discord.ui.button(label='Permanently Delete', style=discord.ButtonStyle.danger, emoji='🗑️', custom_id='ticket_delete_button')
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await has_permission(interaction, "main_moderator") and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("❌ Only Main Moderators and the Server Owner can permanently delete tickets!", ephemeral=True)
            return

        confirm_embed = discord.Embed(
            title="⚠️ Confirm Permanent Deletion",
            description=f"**Are you sure you want to permanently delete this ticket?**\n\n**This action CANNOT be undone!**\n\nTicket: {interaction.channel.mention}",
            color=BrandColors.DANGER
        )

        confirm_view = ConfirmDeleteView()
        await interaction.response.send_message(embed=confirm_embed, view=confirm_view, ephemeral=True)

class ConfirmDeleteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label='Confirm Delete', style=discord.ButtonStyle.danger, emoji='✅')
    async def confirm_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await has_permission(interaction, "main_moderator") and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("❌ Only Main Moderators and the Server Owner can permanently delete tickets!", ephemeral=True)
            return

        channel_name = interaction.channel.name
        
        await interaction.response.send_message(f"🗑️ Deleting ticket {interaction.channel.mention}...", ephemeral=True)
        
        await log_action(interaction.guild.id, "tickets", f"🗑️ [TICKET DELETED] {channel_name} permanently deleted by {interaction.user}")
        
        await asyncio.sleep(2)
        await interaction.channel.delete(reason=f"Ticket permanently deleted by {interaction.user}")
    
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.secondary, emoji='❌')
    async def cancel_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Ticket deletion cancelled.", ephemeral=True)
        self.stop()

class TicketOpenView(discord.ui.View):
    def __init__(self, category_id):
        super().__init__(timeout=None)
        self.category_id = category_id

    @discord.ui.button(label='🎫 Open Support Ticket', style=discord.ButtonStyle.primary, emoji='🎫', custom_id='ticket_open_button')
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        server_data = await get_server_data(interaction.guild.id)
        category_id = server_data.get('ticket_open_category')

        if not category_id:
            await interaction.response.send_message("❌ Ticket system not properly configured! Contact an administrator.", ephemeral=True)
            return

        modal = TicketModal(category_id, server_data)
        await interaction.response.send_modal(modal)

async def has_permission_user(member, guild, permission_level):
    """Check if user has required permission level"""
    if member.id == guild.owner_id:
        return True

    server_data = await get_server_data(guild.id)

    if permission_level == "main_moderator":
        main_mod_role_id = server_data.get('main_moderator_role')
        if main_mod_role_id:
            main_mod_role = guild.get_role(int(main_mod_role_id))
            return main_mod_role in member.roles

    elif permission_level == "junior_moderator":
        junior_mod_role_id = server_data.get('junior_moderator_role')
        main_mod_role_id = server_data.get('main_moderator_role')

        if junior_mod_role_id:
            junior_mod_role = guild.get_role(int(junior_mod_role_id))
            if junior_mod_role in member.roles:
                return True

        if main_mod_role_id:
            main_mod_role = guild.get_role(int(main_mod_role_id))
            if main_mod_role in member.roles:
                return True

    return False

@bot.tree.command(name="ticketsetup", description="Setup ticket system")
@app_commands.describe(
    action="Setup action",
    category="Category for tickets",
    channel="Channel to send ticket button",
    description="Description for ticket message"
)
@app_commands.choices(action=[
    app_commands.Choice(name="open", value="open"),
    app_commands.Choice(name="close", value="close")
])
async def ticket_setup(
    interaction: discord.Interaction,
    action: str,
    category: discord.CategoryChannel,
    channel: discord.TextChannel = None,
    description: str = None
):
    if not await has_permission(interaction, "main_moderator"):
        await interaction.response.send_message("❌ You need Main Moderator permissions to use this command!", ephemeral=True)
        return

    if action == "open":
        if not channel or not description:
            await interaction.response.send_message("❌ Please provide channel and description for ticket setup!", ephemeral=True)
            return

        await update_server_data(interaction.guild.id, {'ticket_open_category': str(category.id)})

        embed = discord.Embed(
            title="🎫 Support Tickets",
            description=f"{description}\n\n**Need help?** Click the button below to create a support ticket!\nOur team will assist you as soon as possible.",
            color=BrandColors.INFO
        )
        embed.set_footer(text=BOT_FOOTER)

        view = TicketOpenView(str(category.id))
        await channel.send(embed=embed, view=view)

        response_embed = discord.Embed(
            title="✅ Ticket System Setup Complete",
            description=f"**Open Category:** {category.mention}\n**Button Channel:** {channel.mention}",
            color=BrandColors.SUCCESS
        )
        await interaction.response.send_message(embed=response_embed)

    elif action == "close":
        await update_server_data(interaction.guild.id, {'ticket_close_category': str(category.id)})

        response_embed = discord.Embed(
            title="✅ Ticket Close Category Set",
            description=f"**Close Category:** {category.mention}",
            color=BrandColors.SUCCESS
        )
        await interaction.response.send_message(embed=response_embed)

    await log_action(interaction.guild.id, "setup", f"🎫 [TICKET SETUP] {action} category set by {interaction.user}")

@bot.tree.command(name="tnamechange", description="Change the name of the current ticket channel")
@app_commands.describe(name="New name for the ticket channel")
async def ticket_name_change(interaction: discord.Interaction, name: str):
    if not await has_permission(interaction, "junior_moderator"):
        await interaction.response.send_message("❌ You need Junior Moderator permissions to use this command!", ephemeral=True)
        return
    
    if not interaction.channel.name.startswith('closed-') and 'ticket' not in interaction.channel.name and '-' not in interaction.channel.name:
        await interaction.response.send_message("❌ This command can only be used in ticket channels!", ephemeral=True)
        return
    
    old_name = interaction.channel.name
    clean_name = ''.join(c for c in name if c.isalnum() or c in ['-', '_']).lower()[:50]
    
    if not clean_name:
        await interaction.response.send_message("❌ Invalid channel name! Please use alphanumeric characters, hyphens, or underscores.", ephemeral=True)
        return
    
    is_closed = old_name.startswith('closed-')
    final_name = f"closed-{clean_name}" if is_closed else clean_name
    
    try:
        await interaction.channel.edit(name=final_name)
        
        embed = discord.Embed(
            title="✅ Ticket Name Changed",
            description=f"**Old Name:** {old_name}\n**New Name:** {final_name}\n**Changed by:** {interaction.user.mention}",
            color=BrandColors.SUCCESS
        )
        embed.set_footer(text=BOT_FOOTER)
        await interaction.response.send_message(embed=embed)
        
        await log_action(interaction.guild.id, "tickets", f"📝 [TICKET RENAME] {old_name} → {final_name} by {interaction.user}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error changing ticket name: {str(e)}", ephemeral=True)

@bot.tree.command(name="ticketconfig", description="Configure ticket form fields (up to 10 fields)")
async def ticket_config(interaction: discord.Interaction):
    if not await has_permission(interaction, "main_moderator"):
        await interaction.response.send_message("❌ You need Main Moderator permissions to use this command!", ephemeral=True)
        return
    
    modal = TicketConfigModal()
    await interaction.response.send_modal(modal)

class TicketConfigModal(discord.ui.Modal, title='🎫 Configure Ticket Fields'):
    def __init__(self):
        super().__init__()
    
    field_count = discord.ui.TextInput(
        label='Number of Fields (1-10)',
        placeholder='Enter number of fields (e.g., 3)',
        required=True,
        max_length=2,
        style=discord.TextStyle.short
    )
    
    field_config = discord.ui.TextInput(
        label='Field Configuration (JSON)',
        placeholder='[{"label":"Name","placeholder":"Your name...","style":"short","required":true,"max_length":100}]',
        style=discord.TextStyle.long,
        required=True,
        max_length=2000
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            import json
            
            count = int(self.field_count.value)
            if count < 1 or count > 10:
                await interaction.response.send_message("❌ Number of fields must be between 1 and 10!", ephemeral=True)
                return
            
            fields_data = json.loads(self.field_config.value)
            
            if not isinstance(fields_data, list):
                await interaction.response.send_message("❌ Field configuration must be a JSON array!", ephemeral=True)
                return
            
            if len(fields_data) != count:
                await interaction.response.send_message(f"❌ You specified {count} fields but provided {len(fields_data)} configurations!", ephemeral=True)
                return
            
            if len(fields_data) > 10:
                await interaction.response.send_message("❌ Maximum 10 fields allowed!", ephemeral=True)
                return
            
            for idx, field in enumerate(fields_data):
                if 'label' not in field:
                    await interaction.response.send_message(f"❌ Field {idx + 1} is missing 'label'!", ephemeral=True)
                    return
                
                if 'style' in field and field['style'] not in ['short', 'long']:
                    await interaction.response.send_message(f"❌ Field {idx + 1} has invalid style! Use 'short' or 'long'.", ephemeral=True)
                    return
            
            await update_server_data(interaction.guild.id, {'ticket_fields': fields_data})
            
            fields_preview = '\n'.join([f"**{i+1}.** {f.get('label')} ({f.get('style', 'short')})" for i, f in enumerate(fields_data)])
            
            embed = discord.Embed(
                title="✅ Ticket Fields Configured",
                description=f"**Total Fields:** {count}\n\n**Fields:**\n{fields_preview}",
                color=BrandColors.SUCCESS
            )
            embed.set_footer(text=BOT_FOOTER)
            await interaction.response.send_message(embed=embed)
            
            await log_action(interaction.guild.id, "setup", f"🎫 [TICKET CONFIG] Ticket fields configured with {count} fields by {interaction.user}")
            
        except json.JSONDecodeError:
            await interaction.response.send_message("❌ Invalid JSON format! Please check your field configuration.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid number of fields! Please enter a number between 1 and 10.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error configuring ticket fields: {str(e)}", ephemeral=True)