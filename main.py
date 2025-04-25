import discord

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

def is_success_message(content):
    """Check if message contains success confirmation text."""
    return content and any(
        phrase in content 
        for phrase in [
            "Successfully donated",
            "Successfully paid",
            "donated successfully", # Not totally useless, but can remove this one and the one below
            "paid successfully"
        ]
    )

async def extract_success_text(message):
    """Extracts success confirmation text from message or components."""
    if is_success_message(message.content):
        return message.content
    
    if message.components:
        for component_row in message.components:
            for component in component_row.children:
                if (str(component.type) == "ComponentType.text_display" and 
                    hasattr(component, 'content') and 
                    is_success_message(component.content)):
                    return component.content
    return None

async def process_message(message):
    """Processes Dank Memer messages and extracts success confirmations."""
    if message.author.id == 270904126974590976:  
        success_text = await extract_success_text(message)
        if success_text:
            await message.channel.send(success_text)

@bot.event
async def on_message(message):
    if message.author.id == 270904126974590976:  
        await process_message(message)

@bot.event
async def on_message_edit(before, after):
    if after.author.id == 270904126974590976:  
        await process_message(after)

bot.run(TOKEN)
