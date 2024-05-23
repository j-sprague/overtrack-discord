# 5-23-2024, Github: j-sprague
# Originally started work in 2022

import os
import discord
import random
from discord import app_commands
from discord.ext import commands
import csv
from datetime import datetime, date
import datetime as dt
from dotenv import load_dotenv
import requests
import json


load_dotenv()

#current_session = 0

TOKEN = os.getenv('DISCORD_TOKEN')

# intents = discord.Intents.default()
# client = discord.Client(intents=intents)

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!",
    ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("-"):
        if message.content.startswith('-compare'):
            orig = await message.channel.send('Getting hero data...')
            searching = message.content[9:]
            shortcuts = {"sarah":"ogniloud-1174","rob":"EchoVertigo-1356","garren":"Schmidt-11978","james":"Jsmans89-1212","john":"Zolhielmz-1161","kevin":"kevinTube-1942","inuno":"Inunomizu-1577","frontal":"FrontalLobe-1688","aeilith":"DeadlyKitten-1265483","cobis":"Cobis-11676","exspy":"Exspy-11108"}
            if searching == "shortcuts":
                msg = "Shortcuts for compare command: " + str(shortcuts.keys())[11:-2]
                await orig.edit(content=msg)
                return
            if searching == "heroes":
                msg = "Heroes for compare command: ana ashe baptiste bastion brigitte cassidy dVa doomfist echo genji hanzo junkrat lucio mei mercy moira orisa pharah reaper reinhardt roadhog sigma soldier76 sombra symmetra torbjorn tracer widowmaker winston wreckingBall zarya zenyatta"
                await orig.edit(content=msg)
                return
            try:
                searching = searching.split()
                hero = searching[0]
                p1 = searching[1]
                p2 = searching[2]
                for i in shortcuts:
                    if i == p1.lower():
                        p1 = shortcuts[i]
                for i in shortcuts:
                    if i == p2.lower():
                        p2 = shortcuts[i]
                api_url1 = 'https://ow-api.com/v1/stats/pc/us/' + p1 + '/complete'
                data1 = requests.get(api_url1).json()
                api_url2 = 'https://ow-api.com/v1/stats/pc/us/' + p2 + '/complete'
                data2 = requests.get(api_url2).json()
                # ranks = data['ratings']
                # name = data['name']
                # icon = data['icon']
                name1 = data1['name']
                name2 = data2['name']
                embed = discord.Embed(title=f"{name1} vs {name2}")
                embed.color = 0xF5F5DC
                # embed.set_thumbnail(url=icon)
                with open('icons.json') as f:
                    img_urls = json.load(f)
                embed.set_thumbnail(url=img_urls[hero][0])
                # level = data['prestige'] * 100 + data['level']
                # embed.add_field(name=f"Level",value=f"{level}",inline=False)
                # embed.add_field(name="Endorsement Level",value=data['endorsement'],inline=False)
                # msg = ""
                # role_icon = {"tank":"<:tank:980675301963079740>","damage":"<:dps:980675302101487676>","support":"<:support:980675301065502751>"}
                # rank_icon = {"BronzeTier":"<:bronze:980675302382514206>","SilverTier":"<:silver:980675302340587580>","GoldTier":"<:gold:980675302340583434>","PlatinumTier":"<:plat:980675302873239602>","DiamondTier":"<:diamond:980675303091347457>","MasterTier":"<:masters:980675302508335154>","GrandmasterTier":"<:gm:980675303213002852>","Top500Tier":"<:t500:980675303200411648>"}
                if data1["private"] is True:
                    embed.add_field(name=f"Unable to access {name1}'s stats",value="Profile is private, data cannot be accessed",inline=False)
                    await orig.edit(embed=embed,content="")
                elif data2["private"] is True:
                    embed.add_field(name=f"Unable to access {name2}'s stats",value="Profile is private, data cannot be accessed",inline=False)
                    await orig.edit(embed=embed,content="")
                elif hero not in data1["competitiveStats"]["careerStats"]:
                    embed.add_field(name=f"Data missing",value=f"{name1} has no stats on selected hero",inline=False)
                    await orig.edit(embed=embed,content="")
                elif hero not in data2["competitiveStats"]["careerStats"]:
                    embed.add_field(name=f"Data missing",value=f"{name2} has no stats on selected hero",inline=False)
                    await orig.edit(embed=embed,content="")
                else:
                    rank_icon = {"BronzeTier":"<:bronze:980675302382514206>","SilverTier":"<:silver:980675302340587580>","GoldTier":"<:gold:980675302340583434>","PlatinumTier":"<:plat:980675302873239602>","DiamondTier":"<:diamond:980675303091347457>","MasterTier":"<:masters:980675302508335154>","GrandmasterTier":"<:gm:980675303213002852>","Top500Tier":"<:t500:980675303200411648>"}
                    playtime1 = data1["competitiveStats"]['careerStats'][hero]['game']['timePlayed']
                    playtime2 = data2["competitiveStats"]['careerStats'][hero]['game']['timePlayed']
                    try:
                        winrate1 = data1['competitiveStats']['careerStats'][hero]['game']['winPercentage']
                    except:
                        winrate1 = "0%"
                    try:
                        winrate2 = data2['competitiveStats']['careerStats'][hero]['game']['winPercentage']
                    except:
                        winrate2 = "0%"
                    embed.add_field(name="Playtime",value=f"{playtime1} vs {playtime2}")
                    embed.add_field(name="Win Percentage",value=f"{winrate1} vs {winrate2}")
                    try:
                        rank1 = "Unranked"
                        for i in data1["ratings"]:
                            if i["role"] == img_urls[hero][1]:
                                for j in rank_icon:
                                    if j in i["rankIcon"]:
                                        rank1 = rank_icon[j] + " " + str(i["level"])
                    except:
                        rank1 = "Unranked"
                    try:
                        rank2 = "Unranked"
                        for i in data2["ratings"]:
                            if i["role"] == img_urls[hero][1]:
                                for j in rank_icon:
                                    if j in i["rankIcon"]:
                                        rank2 = rank_icon[j] + " " + str(i["level"])
                    except:
                        rank2 = "Unranked"
                    embed.add_field(name="Competitive Rank",value=f"{rank1} vs {rank2}",inline=False)
                    try:
                        elim1 = data1["competitiveStats"]['careerStats'][hero]['average']['eliminationsAvgPer10Min']
                    except:
                        elim1 = 0
                    try:
                        elim2 = data2["competitiveStats"]['careerStats'][hero]['average']['eliminationsAvgPer10Min']
                    except:
                        elim2 = 0
                    embed.add_field(name="Eliminations Avg Per 10 Min",value=f"{elim1} vs {elim2}",inline=False)
                    try:
                        dmg1 = data1["competitiveStats"]['careerStats'][hero]['average']['heroDamageDoneAvgPer10Min']
                    except:
                        dmg1 = 0
                    try:
                        dmg2 = data2["competitiveStats"]['careerStats'][hero]['average']['heroDamageDoneAvgPer10Min']
                    except:
                        dmg2 = 0
                    embed.add_field(name="Hero Damage Avg Per 10 Min",value=f"{dmg1} vs {dmg2}",inline=False)
                    if 'healingDoneAvgPer10Min' in data1["competitiveStats"]['careerStats'][hero]['average'] and 'healingDoneAvgPer10Min' in data2["competitiveStats"]['careerStats'][hero]['average']:
                        heal1 = data1["competitiveStats"]['careerStats'][hero]['average']['healingDoneAvgPer10Min']
                        heal2 = data2["competitiveStats"]['careerStats'][hero]['average']['healingDoneAvgPer10Min']
                        embed.add_field(name="Healing Avg Per 10 Min",value=f"{heal1} vs {heal2}",inline=False)
                    

                    # won = data['competitiveStats']["games"]["won"]
                    # played = data['competitiveStats']['games']['played']
                    # winrate = int((won / played)*100)
                    # embed.add_field(name="Competitive Winrate",value=f"{winrate}%, {won} games won of {played}",inline=False)
                    # if ranks:
                    #     for i in ranks:
                    #         rank = ""
                    #         for j in rank_icon:
                    #             if j in i["rankIcon"]:
                    #                 rank = rank_icon[j]
                    #         msg += f'{role_icon.get(i["role"])} {rank} {i["level"]} SR\n'
                    #     embed.add_field(name="Ranks", value=msg, inline=False)
                    # else:
                    #     embed.add_field(name="Ranks", value="No ranks for this season", inline=False)
                    await orig.edit(embed=embed,content="")
            except:
                await orig.edit(content="error or something ill make an error message later  (╯°□°）╯︵ ┻━┻\nProper syntax: -compare ana Jsmans89-1212 kevinTube-1942")

        if message.content.startswith('-rank'):
            orig = await message.channel.send("Getting rank data...")
            searching = message.content[6:]
            shortcuts = {"sarah":"ogniloud-1174","rob":"EchoVertigo-1356","garren":"Schmidt-11978","james":"Jsmans89-1212","john":"Zolhielmz-1161","kevin":"kevinTube-1942","inuno":"Inunomizu-1577","frontal":"FrontalLobe-1688","aeilith":"DeadlyKitten-1265483","cobis":"Cobis-11676","exspy":"Exspy-11108"}
            if searching == "shortcuts":
                msg = "Shortcuts for rank command: " + str(shortcuts.keys())[11:-2]
                await orig.edit(content=msg)
                return
            for i in shortcuts:
                if i == searching.lower():
                    searching = shortcuts[i]
            try:
                searching = searching.split()
                platform = 'pc'
                if len(searching) > 1:
                    platform = searching[1]
                api_url = 'https://ow-api.com/v1/stats/' + platform + '/us/' + searching[0] + '/complete'
                data = requests.get(api_url).json()
                ranks = data['ratings']
                name = data['name']
                icon = data['icon']
                embed = discord.Embed(title=f"{name}'s Profile")
                if platform == 'xbl':
                    embed.color = 0x00FF00
                elif platform == 'nintendo-switch':
                    embed.color = 0xFF0000
                elif platform == 'psn':
                    embed.color = 0x0000FF
                embed.set_thumbnail(url=icon)
                # level = data['prestige'] * 100 + data['level']
                # embed.add_field(name=f"Level",value=f"{level}",inline=False)
                embed.add_field(name="Endorsement Level",value=data['endorsement'],inline=False)
                msg = ""
                role_icon = {"tank":"<:tank:980675301963079740>","offense":"<:dps:980675302101487676>","support":"<:support:980675301065502751>"}
                rank_icon = {"Bronze":"<:bronze:980675302382514206>","Silver":"<:silver:980675302340587580>","Gold":"<:gold:980675302340583434>","Platinum":"<:plat:980675302873239602>","Diamond":"<:diamond:980675303091347457>","Master":"<:masters:980675302508335154>","Grandmaster":"<:gm:980675303213002852>","Top500":"<:t500:980675303200411648>"}
                if data["private"] is True:
                    embed.add_field(name="Ranks",value="Profile is private, rank cannot be accessed",inline=False)
                else:
                    won = data['competitiveStats']["games"]["won"]
                    played = data['competitiveStats']['games']['played']
                    if played > 0:
                        winrate = int((won / played)*100)
                        embed.add_field(name="Competitive Winrate",value=f"{winrate}%, {won} games won of {played}",inline=False)
                        if ranks:
                            for i in ranks:
                                rank = ""
                                for j in rank_icon:
                                    if j in i["group"]:
                                        rank = rank_icon[j]
                                msg += f'{role_icon.get(i["role"])} {rank} {i["group"]} {i["tier"]} \n'
                            embed.add_field(name="Ranks", value=msg, inline=False)
                        else:
                            embed.add_field(name="Ranks", value="No ranks for this season", inline=False)
                        playtimes = {}
                        for i in data['competitiveStats']['topHeroes']:
                            # print(i)
                            hero = data['competitiveStats']['topHeroes'][i]
                            # print(i)
                            # print(i['timePlayed'])
                            secs = 0
                            try:
                                secs = datetime.strptime(hero['timePlayed'], '%H:%M:%S')
                            except:
                                secs = datetime.strptime(hero['timePlayed'], '%M:%S')
                            secs = (secs - dt.datetime(1900,1,1)).total_seconds()
                            playtimes[i] = secs
                        sorted_values = sorted(playtimes.values(), reverse=True)
                        sorted_dict = {}
                        for i in sorted_values:
                            for k in playtimes.keys():
                                if playtimes[k] == i:
                                    sorted_dict[k] = playtimes[k]
                                    break
                        # print(sorted_dict)
                        with open('icons.json') as f:
                            emojis = json.load(f)
                        msg = ''
                        pop_list = list(sorted_dict.keys())
                        for i in range(8):
                            try:
                                msg += emojis[pop_list[i]][2]
                            except:
                                break
                        # print(msg)
                        embed.add_field(name="Most played recently",value=msg,inline=False)
                    else:
                        embed.add_field(name="No data for current season",value="Player must have playtime in current competitive season",inline=False)
                await orig.edit(embed=embed,content="")
            except:
                await orig.edit(content="Failed to get data! Please make sure profile is public and bnet is entered correctly (case sensitive) with a hyphen separating the end numbers. (currently only searches PC NA accounts) \nProper syntax: -rank Jsmans89-1212")
            
        if message.content.startswith("-embed"):
            embed = discord.Embed(
                title = "Sample Embed",
                url = "https://google.com/",
                description = "This is a cool embed",
                color=0xFF5733
            )
            await message.channel.send(embed=embed)
        
        if message.content.startswith("-random"):
            roles = ['t','s','d']
            file = open(f'overwatch_heroes.txt','r')
            file_list = file.readlines()
            # print(message.content)
            # print(message.content[18].lower())
            try:
                if message.content[8].lower() in roles:
                    # print('in roles')
                    start_index = 0
                    end_index = 0
                    for i in range(len(file_list)):
                        if file_list[i][0] == '-' and file_list[i][1].lower() == message.content[8].lower():
                            start_index = i+1
                        elif start_index != 0 and file_list[i][0] == '-':
                            end_index = i-1
                            break
                    selected = file_list[random.randint(start_index,end_index)]
                    await message.channel.send("Randomly selected Overwatch hero: **" + selected.strip() + "**!")
                    
                else:
                    raise
            except:
                while True:
                        selected = file_list[random.randint(0,(len(file_list)-1))]
                        if selected[0] != '-':
                            break
                await message.channel.send("Randomly selected Overwatch hero: **" + selected.strip() + "**!")
                


client.run(TOKEN)