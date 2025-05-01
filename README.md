# discord-quote-parser
This is a simple python script which can be run on any Discord server through Discord's Bot framework. The intent of the script is to read all text within a specified channel, use regex to parse anything formatted as a quote, and then write all of the quotes found to a .CSV file.

What you do with the resulting CSV is entirely up to you. But this script was initially created to assist in creating a Jeopardy-like game where contestants were given a quote and tasked with guessing who said it.

# How it Works
This script rquires a specific format to parse, label, and store quotes correctly. It expects a quote to be in the following format:

``` "This is something someone said" ~ @This is who said it```

It will still filter out quotes with similar formatting, but the format cannot stray very far from [Quote][Handle]. If it does, the regex may not reliably detect it, or it may match on something that isn't a quote at all.

I can't gurantee this script will work for you if the quotes are formatted differently than described above. If you need it modified, write a detailed issue report and I can try to make it work for you. Otherwise, have your users change their formatting to match.

# To Run this Yourself

>[!IMPORTANT]
>This script has been tested with python 3.11.6. Your experience may be different on other versions.
>This script also has dependencies for ```discord.py``` and ```pandas```. They can be installed with ```pip install discord.py pandas```

 
1. Create a Discord bot in the Discord developer portal. https://discord.com/developers/applications

Name it whatever you like.

2. In the left pane, you will need to navigate to the Bot panel and assign some permissions, as well as find your Bot Token.

![image](https://github.com/user-attachments/assets/ac014a18-a44f-4e6b-ba2d-a13d51797ddf)

3. Here, be sure to enable ```Server Members``` and ```Message Content``` intents. They are needed for the bot to read messages and automatically convert user IDs to their member discriminator.

![image](https://github.com/user-attachments/assets/82336d5c-ea73-4beb-92fe-353a1c3dcf30)

4. Add the bot to your server by generating an OAuth URL. Include the **Bot** scope and the **Read Message History** permission.

5. Give your bot permission to view your channel through your server's permissions system.

6. Copy the link to your channel. Extract the **Guild ID** and the **Channel ID** from the generated URL. Enter these into the script where specified.

7. Run the script.

8. Profit???

>[!NOTE]
>Full disclosure, this script was hardcore _vibe coded_. It works, but it's not very efficient. I did my best to condense it down and make it less resource heavy. If you have ideas to improve it, consider submitting a PR ❤️.
