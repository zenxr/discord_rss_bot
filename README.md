# OverWatch Updates Discord Bot
This bot utilizes an rss feed that is updated when OverWatch patch notes are released. It checks once an hour for an update to the rss feed, and if found will send a message to the channel_ids used. It can be modified to use many other RSS feeds. The RSS feed is intepreted using feedparser, then the html summary inside is eventually converted to MarkDown (a format Discord naturally accepts)
```
Note: discord_rss.py is the bot file you should execute
```
### Usage (in Discord)
* !help
* !patch notes
* !clean patch notes

### Getting Started
* Python3 (3.5 used)
* feedparser (install using pip or other method)
* html2text (install using pip or other method)

### Installing and Running
* Create a discord developer's Application and get the secret token, please see [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
* Place the secret_token of your application in testing_rss.py file
* Obtain the channel IDs of the channels you'd like the bot to interact with
* Place the channel IDs in the testing_rss.py file accordingly
* Go into the directory that contains the files
```
cd /your/path/to/files/discord_rss_bot
```
* Execute the bot
```
python3.5 testing_rss.py
```

### Author
**Cody Stephenson**


