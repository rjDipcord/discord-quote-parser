import discord
import re
import pandas as pd
import asyncio

TOKEN = "YOUR BOT TOKEN GOES HERE"
GUILD_ID = 1234567890  # Replace with your server ID
CHANNEL_ID = 1234567890  # Replace with the target channel ID

'''
Here is an example of the above config:
Token should be retreived from the Discord Developer Portal under the "Bot" tab.
TOKEN = "ASDFNikaisdfjsdhfkkviuviurvhuihrvrv.SFGhsfgufhguifhguifh.ASDGFJSFGHSDFSIDFJINCIRsfhbhvjsd"

Both guild ID and Channel ID can be retreived simply by copying the LINK to a specific channel in your discord.
EXAMPLE:
                               THIS IS GUILD_ID    THIS IS CHANNEL_ID
https://discord.com/channels/1247043930646114385/1247045931149294509

In this case, your config would look like this:
GUILD_ID = 1247043930646114385 
CHANNEL_ID = 1247045931149294509 
'''

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Make sure this intent is enabled
client = discord.Client(intents=intents)

# Matches: "some text" @User (mention) OR "some text" (without @mention)
quote_pattern = re.compile(r'"(.+?)"\s+<@!?(\d+)>|"(.*?)"')

data = []

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(f"❌ Guild with ID {GUILD_ID} not found.")
        await client.close()
        return

    channel = guild.get_channel(CHANNEL_ID)
    if not channel:
        print(f"❌ Channel with ID {CHANNEL_ID} not found in guild '{guild.name}'.")
        await client.close()
        return

    print(f"🔍 Scanning channel '{channel.name}' in server '{guild.name}' ({guild.id}/{channel.id})")

    message_count = 0
    match_count = 0

    async for message in channel.history(limit=None, oldest_first=True):
        message_count += 1
        content = message.content.strip()

        # Verbose logging
        print(f"\n📨 Message {message_count} by {message.author}")
        print(f"🕒 Date: {message.created_at}")
        print(f"🔤 content: {repr(content)}")

        if not content:
            print("   ⚠️ Skipping empty message.")
            continue

        matches = quote_pattern.findall(content)
        if not matches:
            print("   ⛔ No matches in this message.")
        
        for match in matches:
            quote, user_id, fallback_quote = match

            quote_text = quote if quote else fallback_quote

            if user_id:  # If a user mention was found
                try:
                    member = guild.get_member(int(user_id)) or await guild.fetch_member(int(user_id))
                    if member:
                        author = f"{member.name}#{member.discriminator}"
                    else:
                        author = f"<@{user_id}>"
                except discord.NotFound:
                    author = f"<@{user_id}>"
            else:
                author = f"{message.author.name}#{message.author.discriminator}"

            print(f"   ✅ Match: '{quote_text}' by {author}")
            data.append({
                "quote": quote_text,
                "author": author,
                "date": message.created_at.isoformat()
            })
            match_count += 1

    print(f"\n🔎 Finished scanning {message_count} messages.")
    print(f"📝 Found {match_count} quotes. Writing to CSV...")

    df = pd.DataFrame(data)
    df.to_csv("quotes.csv", index=False)
    print("✅ Saved to quotes.csv")

    await client.close()

client.run(TOKEN)
