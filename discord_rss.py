import feedparser
import time
import html2text
import discord
import asyncio
from datetime import datetime as dt

# create a new client
client = discord.Client()

# secret token
token = 'MzY0OTM0ODQ4ODY5MTcxMjAw.DLhQzA.65t4WL8ib44YjMfRofjTYFlaHPw'
# app_id from discord developer's app creation section
app_id = '364934848869171200'
# channel_id for Nocturne-testing
channel_id_primary = '324271405573079061'
# channel_id for James' server
channel_id = '279350547260112896'
# another channel_id
channel_id_2 = '365758538079010826'
# url of the RSS feed being used
rss_url = 'https://fbis251.github.io/overwatch_news_feed/pc.atom'

# help message to display
helpm = "\r\n If you'd like to check the most recent OverWatch patch notes:\r\n"
helpm = helpm + "```!patch notes```\r\n"
helpm = helpm + "To delete patch notes:\r\n```!clean patch notes```"

# previousTitle is used to identify if a new post has occured on the feed
# it saves the previous feed's first title and compared
# it against a newly downloaded feed
global previousTitle
# used in unixReport function
global count
# initiate the global vars
count = 0
previousTitle = ''

# parses rss and converts the html to markdown
def convert_text_to_md():
    d = feedparser.parse(rss_url)
    # initiating the string to be returned
    returnstuff = ""
    # use the most recent post (element 0)
    post = d.entries[0]
    # remove any strange characters by only keeping ascii
    output = (post.title.encode('ascii', 'ignore').decode('ascii'))
    output = output + ("\n---------------------------------------\n")
    html = (post.summary.encode('ascii', 'ignore').decode('ascii'))
    # convert the text from html to markdown
    text = html2text.html2text(html)
    returnstuff = returnstuff + output + text
    return returnstuff

# check just the title of the newest rss feed
# compare to previously saved title
def need_to_update():
    # in python you have to declare you're using a 
    # global var to have write access
    global previousTitle
    d = feedparser.parse(rss_url)
    post = d.entries[0]
    # remove any characters that arent ascii
    title = post.title.encode('ascii', 'ignore').decode('ascii')
    # if the title has changed, update previousTitle for the next check
    if title != previousTitle:
        previousTitle = title
        return 1

# checks if a message's author is the bot
def is_me(m):
    return m.author == client.user

# custom asyncronous function
# used to trigger the need_to_update once per hour
async def unixReport():
    global count
    while True:
        # if its 5 minutes past the turn of the hour
        if dt.now().minute == 5: #if you want to add channels, then add more await bot.send_message stuff idk
            # used incase the sleep function doesn't properly delay the function
            if count == 0:
                count = 1
                # if the newest post isn't the same as previous post
                if need_to_update(): 
                    # then parse the newest post
                    message = convert_text_to_md()
                    # if message is greater than 1500 characters, we need to split it into chunks
                    if len(message) > 1500:
                        position = 0
                        end = 1500
                        # go is used as a trigger to stop/start
                        go = 1
                        while (go > 0):
                            # ..messagetext..
                            # then send the message to any channels added here
                            # note this could be converted to run for a loop over a list of saved channels
                            # pretty easily. I should do this next time I work on it
                            # a list would be easy enough, but text file in same folder preferred
                            info = '..' + message[position:end] + '..'
                            await client.send_message(client.get_channel(channel_id), info)
                            await client.send_message(client.get_channel(channel_id_2), info)
                            await client.send_message(client.get_channel(channel_id_primary), info)
                            # move to get the next chunk
                            position = position + 1500
                            end = end + 1500
                            # if we've just sent the last message to send
                            if go == 2:
                                go = 0
                                # probably uneccesary
                                break
                            # if the end of the message comes before our next "end postion"
                            # we need to use that as the new tail/end position
                            if end > (len(message) - 1):
                                end = len(message)-1
                                go = 2
                    # if post length less than 1500 characters, just send it to the appropriate channels
                    else:
                        await client.send_message(client.get_channel(channel_id), message)
                        await client.send_message(client.get_channel(channel_id_2), message)
                        await client.send_message(client.get_channel(channel_id_primary), messaage)
        # once we hit 6 minutes past the hour, reset counter
        elif dt.now().minute == 6:
            count = 0
        await asyncio.sleep(1)

# runs when the client first connects
@client.event
async def on_ready():
    global count
    global xtime
    xtime = str(dt.now())
    # initiate the asyncronous task
    asyncio.get_event_loop().create_task(unixReport())

    # print info to terminal
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # print connected servers
    for server in client.servers:
        print(server.name)
    print('------')

# runs when a member joins the server
# (only once, when they're invited)
@client.event
async def on_member_join(member):
    tmp = await client.send_message(member.server, helpm)

# this runs when any message is sent in a connected channel
@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        helpmessage = message.author.mention + helpm
        await client.send_message(message.channel, helpmessage)
    if message.content.startswith('!clean patch notes'):
        deleted = await client.purge_from(message.channel, limit=50, check=is_me)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))

    if message.content.startswith('!patch notes'):
        message_to_send = convert_text_to_md()
        if len(message_to_send) > 1500:
            position = 0
            end = 1500
            go = 1
            while (go > 0):
                info = '..' + message_to_send[position:end] + '..'
                await client.send_message(message.channel, info)
                position = position + 1500
                end = end + 1500
                if go == 2:
                    go = 0
                    break
                if end > (len(message_to_send) - 1):
                    end = len(message_to_send)-1
                    go = 2
        else:
            await client.send_message(message.channel, message)


client.run(token)
