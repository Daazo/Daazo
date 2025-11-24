import os
import discord
from discord import app_commands
from discord.ext import commands
import re
from datetime import datetime
from google import genai
from google.genai import types

from brand_config import BrandColors, BOT_FOOTER
from main import bot, db, has_permission, get_server_data, log_action, create_error_embed, create_permission_denied_embed

# IMPORTANT: KEEP THIS COMMENT
# Integration: blueprint:python_gemini
# Using Gemini 2.5 Flash for fast AI responses and Gemini 2.0 Flash for image generation

# Initialize Gemini client
try:
    gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    print("✅ Gemini AI client initialized")
except Exception as e:
    gemini_client = None
    print(f"⚠️ Gemini AI client failed to initialize: {e}")

# Image generation keywords
IMAGE_KEYWORDS = [
    'create', 'generate', 'make', 'draw', 'design', 'paint', 'sketch',
    'image', 'picture', 'photo', 'illustration', 'art', 'artwork',
    'logo', 'banner', 'wallpaper', 'icon', 'graphic'
]

def is_image_request(message_content: str) -> bool:
    """Detect if user is requesting image generation"""
    content_lower = message_content.lower()
    
    # Check for common image generation patterns
    image_patterns = [
        r'\b(create|generate|make|draw|design)\s+(a|an|me)?\s*(image|picture|photo|logo|art)',
        r'\b(image|picture|photo|logo|art)\s+of\b',
        r'\bshow\s+me\s+(a|an)\s+(picture|image|photo)',
    ]
    
    for pattern in image_patterns:
        if re.search(pattern, content_lower):
            return True
    
    # Check if message contains multiple image-related keywords
    keyword_count = sum(1 for keyword in IMAGE_KEYWORDS if keyword in content_lower)
    return keyword_count >= 2

async def generate_ai_image(prompt: str, temp_path: str) -> bool:
    """Generate image using Gemini"""
    try:
        if not gemini_client:
            return False
        
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        if not response.candidates:
            return False
        
        content = response.candidates[0].content
        if not content or not content.parts:
            return False
        
        for part in content.parts:
            if part.inline_data and part.inline_data.data:
                with open(temp_path, 'wb') as f:
                    f.write(part.inline_data.data)
                return True
        
        return False
    except Exception as e:
        print(f"❌ [AI IMAGE ERROR] {e}")
        return False

async def get_ai_response(prompt: str) -> str:
    """Get AI text response from Gemini"""
    try:
        if not gemini_client:
            return "❌ AI service is currently unavailable. Please check the API key configuration."
        
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return response.text or "I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"❌ [AI ERROR] {e}")
        return f"❌ An error occurred: {str(e)}"

@bot.tree.command(name="set-ai-channel", description="🤖 Set the AI chat channel (Owner/Main Moderator only)")
@app_commands.describe(channel="Channel where AI will respond to messages")
async def set_ai_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    """Set the AI chat channel for the server"""
    if not await has_permission(interaction, "main_moderator"):
        await interaction.response.send_message(
            embed=create_permission_denied_embed("Main Moderator"),
            ephemeral=True
        )
        return
    
    try:
        if db is not None:
            await db.ai_settings.update_one(
                {'guild_id': str(interaction.guild.id)},
                {'$set': {
                    'ai_channel_id': str(channel.id),
                    'setup_by': str(interaction.user.id),
                    'setup_at': datetime.utcnow()
                }},
                upsert=True
            )
        
        embed = discord.Embed(
            title="🤖 AI Chat Channel Set",
            description=f"**AI Channel:** {channel.mention}\n**Setup by:** {interaction.user.mention}\n**Status:** Active",
            color=BrandColors.PRIMARY
        )
        embed.add_field(
            name="💬 How It Works",
            value="✓ Just type normally in the AI channel\n✓ No commands needed\n✓ AI auto-detects image requests\n✓ Powered by Gemini 1.5 Flash",
            inline=False
        )
        embed.set_footer(text=BOT_FOOTER)
        
        await interaction.response.send_message(embed=embed)
        await log_action(
            interaction.guild.id,
            "ai_chat",
            f"🤖 [AI CHANNEL SET] {interaction.user} set AI channel to {channel.mention}"
        )
        
        # Global logging
        try:
            from advanced_logging import send_global_log
            await send_global_log(
                "ai_chat",
                f"**🤖 AI Channel Setup**\n**Server:** {interaction.guild.name}\n**Channel:** {channel.mention}\n**Setup by:** {interaction.user.mention}",
                interaction.guild
            )
        except:
            pass
            
    except Exception as e:
        await interaction.response.send_message(
            embed=create_error_embed(f"Failed to set AI channel: {str(e)}"),
            ephemeral=True
        )

async def handle_ai_message(message):
    """Handle AI chat in designated channels (called from main on_message handler)"""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Ignore if not in a guild
    if not message.guild:
        return
    
    # Check if AI is enabled for this server
    if db is None:
        return
    
    try:
        ai_settings = await db.ai_settings.find_one({'guild_id': str(message.guild.id)})
        
        # No AI channel set
        if not ai_settings or not ai_settings.get('ai_channel_id'):
            return
        
        # Check if message is in the AI channel
        if str(message.channel.id) != ai_settings.get('ai_channel_id'):
            return
        
        # Check if Gemini client is initialized
        if not gemini_client:
            await message.channel.send("❌ AI service is currently unavailable. Please ask an admin to configure the API key.")
            return
        
        # Show typing indicator
        async with message.channel.typing():
            # Check if this is an image generation request
            if is_image_request(message.content):
                # Generate image
                temp_image_path = f"/tmp/ai_generated_{message.id}.png"
                
                success = await generate_ai_image(message.content, temp_image_path)
                
                if success:
                    # Send the generated image
                    embed = discord.Embed(
                        title="🎨 Generated Image",
                        description=f"**Prompt:** {message.content[:100]}{'...' if len(message.content) > 100 else ''}",
                        color=BrandColors.PRIMARY
                    )
                    embed.set_footer(text=f"Generated for {message.author.display_name}")
                    
                    file = discord.File(temp_image_path, filename="generated_image.png")
                    embed.set_image(url="attachment://generated_image.png")
                    
                    await message.reply(embed=embed, file=file)
                    
                    # Clean up temp file
                    try:
                        os.remove(temp_image_path)
                    except:
                        pass
                    
                    # Log the interaction
                    await log_action(
                        message.guild.id,
                        "ai_chat",
                        f"🎨 [AI IMAGE] {message.author} generated image: {message.content[:50]}"
                    )
                    
                    # Global logging
                    try:
                        from advanced_logging import send_global_log
                        await send_global_log(
                            "ai_chat",
                            f"**🎨 AI Image Generated**\n**User:** {message.author.mention}\n**Prompt:** {message.content[:100]}",
                            message.guild
                        )
                    except:
                        pass
                else:
                    await message.reply("❌ Failed to generate image. Please try again with a different prompt.")
            else:
                # Generate text response
                response_text = await get_ai_response(message.content)
                
                # Split response if too long (Discord limit is 2000 chars)
                if len(response_text) > 2000:
                    # Send in chunks
                    chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
                    for chunk in chunks:
                        await message.reply(chunk)
                else:
                    await message.reply(response_text)
                
                # Log the interaction
                await log_action(
                    message.guild.id,
                    "ai_chat",
                    f"🤖 [AI CHAT] {message.author}: {message.content[:50]}"
                )
                
                # Global logging
                try:
                    from advanced_logging import send_global_log
                    await send_global_log(
                        "ai_chat",
                        f"**🤖 AI Chat**\n**User:** {message.author.mention}\n**Query:** {message.content[:100]}",
                        message.guild
                    )
                except:
                    pass
                    
    except Exception as e:
        print(f"❌ [AI CHAT ERROR] {e}")
        await message.reply("❌ An error occurred while processing your request. Please try again.")

print("✅ AI Chat system loaded (Gemini 1.5 Flash)")
