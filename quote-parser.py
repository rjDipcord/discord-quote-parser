import discord
import re
import pandas as pd
import asyncio
from datetime import datetime, date, time, timezone

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

# Define your inclusive date range (YYYY-MM-DD)
# The script will ONLY fetch messages that fall between these two dates.
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 
intents.members = True
client = discord.Client(intents=intents)

# Adjusted regex to match both formats
quote_pattern = re.compile(r'"(.*?)"\s*[\n\r]*[~\-–—]*\s*<@!?(\d+)>', re.DOTALL)

data = []

# Convert the dates provided to a format we can feed to the API.
start_dt = datetime.combine(START_DATE, time.min).replace(tzinfo=timezone.utc)
end_dt = datetime.combine(END_DATE, time.max).replace(tzinfo=timezone.utc)

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
    print(f"🔍 Scanning messages after {start_dt} and before {end_dt}")

    message_count = 0
    match_count = 0

    async for message in channel.history(limit=None, oldest_first=True, after=start_dt, before=end_dt):
        message_count += 1
        content = message.content.strip()
        print(f"\n📨 Message {message_count}")
        print(f"🕒 Date: {message.created_at}")
        print(f"🔤 content: {content}")

        quote = None
        author = None
        user_id = None

        match = re.search(r'"(.*?)"\s*[\n\r]*[~\-–—]*\s*<@!?(\d+)>', content, re.DOTALL)
        if match:
            quote = match.group(1).strip()
            user_id = match.group(2)
            print(f"   ✅ Regex matched: quote='{quote}' | user_id={user_id}")
        else:
            print(f"   ⚠️ Regex did not match this message.")

        # Resolve the author
        if user_id:
            print(f"   🔍 Resolving user ID: {user_id}")
            try:
                member = guild.get_member(int(user_id))
                if member:
                    author = f"{member.name}#{member.discriminator}"
                    print(f"   ✅ Found in guild: {author}")
                else:
                    print(f"   ⚠️ Not found in guild. Trying global fetch...")
                    try:
                        user = await client.fetch_user(int(user_id))
                        author = f"{user.name}#{user.discriminator}"
                        print(f"   ✅ Found globally: {author}")
                    except discord.NotFound:
                        author = f"<@{user_id}>"
                        print(f"   ❌ User not found globally. Using raw ID: {author}")
            except Exception as e:
                author = f"<@{user_id}>"
                print(f"   ❌ Exception during user resolution: {e}")
        else:
            author = f"{message.author.name}#{message.author.discriminator}"
            print(f"   🔄 No mention found. Defaulting to message author: {author}")

        if quote:
            print(f"   ✅ Final Match: '{quote}' by {author}")
            data.append({
                "quote": quote,
                "author": author,
                "date": message.created_at.isoformat()
            })
            match_count += 1
        else:
            print(f"   ⚠️ Skipping message: No quote found.")

    print(f"\n🔎 Finished scanning {message_count} messages.")
    print(f"📝 Found {match_count} quotes. Writing to CSV...")

    df = pd.DataFrame(data)
    df.to_csv("quotes.csv", index=False)
    print("✅ Saved to quotes.csv")

    await client.close()


client.run(TOKEN)
