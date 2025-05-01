# discord-quote-parser
This is a simple python script which can be run on any Discord server through Discord's Bot framework. The intent of the script is to read all text within a specified channel, use regex to parse anything formatted as a quote, and then write all of the quotes found to a .CSV file.

What you do with the resulting CSV is entirely up to you. But this script was initially created to assist in creating a Jeopardy-like game where contestants were given a quote and tasked with guessing who said it.

# To run this yourself

>[!NOTE]
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
