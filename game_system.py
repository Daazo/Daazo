import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
from typing import Optional, Union
from brand_config import BrandColors, VisualElements, BOT_FOOTER

# Global references for main.py integration
db = None
log_action_func = None

def setup_game_system(database, log_func):
    """Initializes the game system with database and logging from main.py"""
    global db, log_action_func
    db = database
    log_action_func = log_func

# --- MULTIPLAYER LOGIC ---
class TicTacToeView(discord.ui.View):
    def __init__(self, p1: discord.Member, p2: discord.Member, guild_id: int, log_func):
        super().__init__(timeout=60)
        self.p1, self.p2, self.turn = p1, p2, p1
        self.board, self.guild_id, self.log_func = [0] * 9, guild_id, log_func
        self.winner: Optional[Union[discord.Member, str]] = None
        for i in range(9): self.add_item(TicTacToeButton(i))

    async def check_winner(self):
        combos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for c in combos:
            if self.board[c[0]] == self.board[c[1]] == self.board[c[2]] != 0:
                self.winner = self.p1 if self.board[c[0]] == 1 else self.p2
                return True
        if 0 not in self.board: self.winner = "Draw"; return True
        return False

class TicTacToeButton(discord.ui.Button):
    def __init__(self, index: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=index // 3)
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        if interaction.user != view.turn: return await interaction.response.send_message("Not your turn!", ephemeral=True)
        if view.board[self.index] != 0: return await interaction.response.send_message("Taken!", ephemeral=True)

        view.board[self.index] = 1 if view.turn == view.p1 else 2
        self.label, self.disabled = ("X" if view.turn == view.p1 else "O"), True
        self.style = discord.ButtonStyle.primary if view.turn == view.p1 else discord.ButtonStyle.success

        if await view.check_winner():
            for item in view.children: item.disabled = True
            msg = "🤝 **DRAW!**" if view.winner == "Draw" else f"🏆 **WINNER!** {view.winner.mention}"
            await interaction.response.edit_message(embed=discord.Embed(title="🎮 TIC-TAC-TOE", description=f"{VisualElements.CIRCUIT_LINE}\n{msg}", color=BrandColors.SUCCESS), view=view)
            if view.log_func: await view.log_func(view.guild_id, "general", f"🎮 **Game Ended**: TTT | {view.p1.name} vs {view.p2.name} | Result: {view.winner}")
            view.stop()
        else:
            view.turn = view.p2 if view.turn == view.p1 else view.p1
            await interaction.response.edit_message(embed=discord.Embed(title="🎮 TIC-TAC-TOE", description=f"{VisualElements.CIRCUIT_LINE}\n**Turn:** {view.turn.mention}", color=BrandColors.PRIMARY), view=view)

class RPSView(discord.ui.View):
    def __init__(self, p1: discord.Member, p2: discord.Member, guild_id: int, log_func):
        super().__init__(timeout=60)
        self.p1, self.p2, self.choices = p1, p2, {p1.id: None, p2.id: None}
        self.guild_id, self.log_func = guild_id, log_func

    @discord.ui.button(label="ROCK", emoji="🪨")
    async def rock(self, i, b): await self.handle(i, "rock")
    @discord.ui.button(label="PAPER", emoji="📄")
    async def paper(self, i, b): await self.handle(i, "paper")
    @discord.ui.button(label="SCISSORS", emoji="✂️")
    async def scissors(self, i, b): await self.handle(i, "scissors")

    async def handle(self, i, choice):
        if i.user.id not in self.choices: return await i.response.send_message("Not playing!", ephemeral=True)
        if self.choices[i.user.id]: return await i.response.send_message("Already picked!", ephemeral=True)
        self.choices[i.user.id] = choice
        await i.response.send_message(f"Selected: `{choice.upper()}`", ephemeral=True)
        if all(self.choices.values()):
            c1, c2 = self.choices[self.p1.id], self.choices[self.p2.id]
            if c1 == c2: res, win = "🤝 **DRAW!**", "Draw"
            elif (c1=="rock" and c2=="scissors") or (c1=="paper" and c2=="rock") or (c1=="scissors" and c2=="paper"):
                res, win = f"🏆 **WINNER!** {self.p1.mention}", self.p1.name
            else: res, win = f"🏆 **WINNER!** {self.p2.mention}", self.p2.name
            await i.message.edit(embed=discord.Embed(title="🎮 RPS", description=f"{self.p1.name}: `{c1.upper()}`\n{self.p2.name}: `{c2.upper()}`\n\n{res}", color=BrandColors.SUCCESS), view=None)
            if self.log_func: await self.log_func(self.guild_id, "general", f"🎮 **Game Ended**: RPS | {self.p1.name} vs {self.p2.name} | Winner: {win}")
            self.stop()

# --- SYSTEM COG ---
class GameSystem(commands.Cog):
    def __init__(self, bot): self.bot = bot
    game_group = app_commands.Group(name="game", description="RXT ENGINE Gaming Core")

    @game_group.command(name="set-channel")
    @app_commands.choices(game_type=[app_commands.Choice(name="Trivia", value="trivia"), app_commands.Choice(name="RPS", value="rps"), app_commands.Choice(name="Tic Tac Toe", value="ttt")])
    async def set_game_channel(self, interaction, game_type: str, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("Admin only!", ephemeral=True)
        if db: await db.game_configs.update_one({'guild_id': str(interaction.guild.id)}, {'$set': {f'channels.{game_type}': str(channel.id)}}, upsert=True)
        await interaction.response.send_message(f"✅ {game_type.upper()} locked to {channel.mention}")

    async def check_channel(self, interaction, game_type):
        if db:
            config = await db.game_configs.find_one({'guild_id': str(interaction.guild.id)})
            target = config.get('channels', {}).get(game_type) if config else None
            if target and str(interaction.channel.id) != target:
                await interaction.response.send_message(f"❌ This game is restricted to <#{target}>", ephemeral=True); return False
        return True

    @game_group.command(name="trivia")
    async def trivia(self, interaction):
        if not await self.check_channel(interaction, "trivia"): return
        q = random.choice([{"q": "Planet known as Red Planet?", "a": "Mars", "o": ["Mars", "Venus", "Jupiter"]}, {"q": "Capital of Japan?", "a": "Tokyo", "o": ["Tokyo", "Seoul", "Osaka"]}])
        view = discord.ui.View()
        for opt in q["o"]:
            btn = discord.ui.Button(label=opt)
            async def cb(i, o=opt):
                await i.response.edit_message(embed=discord.Embed(title="RESULT", description=f"{'✓' if o==q['a'] else '✗'} Correct: `{q['a']}`", color=BrandColors.SUCCESS if o==q['a'] else BrandColors.DANGER), view=None)
            btn.callback = cb; view.add_item(btn)
        await interaction.response.send_message(embed=discord.Embed(title="⚡ TRIVIA", description=q['q'], color=BrandColors.PRIMARY), view=view)

    @game_group.command(name="rps")
    async def rps(self, interaction, opponent: discord.Member):
        if not await self.check_channel(interaction, "rps"): return
        await interaction.response.send_message(embed=discord.Embed(title="🎮 RPS CHALLENGE", description=f"{interaction.user.mention} vs {opponent.mention}"), view=RPSView(interaction.user, opponent, interaction.guild.id, log_action_func))

    @game_group.command(name="ttt")
    async def ttt(self, interaction, opponent: discord.Member):
        if not await self.check_channel(interaction, "ttt"): return
        await interaction.response.send_message(embed=discord.Embed(title="🎮 TIC-TAC-TOE", description=f"**Turn:** {interaction.user.mention}"), view=TicTacToeView(interaction.user, opponent, interaction.guild.id, log_action_func))

async def setup(bot): await bot.add_cog(GameSystem(bot))
