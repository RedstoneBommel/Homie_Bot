from discord.ext import commands, tasks
import scrapetube as tube
import json

class youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("json/videoLinks.json", "r") as videoLinksFile:
            videoLinks = json.load(videoLinksFile)
            self.channels = videoLinks["youtube"]
        self.videos = {}

        @commands.Cog.listener()
        async def on_ready(self):
            check.start()

        @tasks.loop(seconds = 30)
        async def check(self):
            linkChannel = self.bot.get_channel(1192413723386707979)
            for nameChannel in self.channels:
                videos = tube.get_channel(channel_url = self.channels[nameChannel], limit = 5)
                videosID = []
                for video in videos:
                    videosID.append(video["videoId"])
                if check.current_loop == 0:
                    videos[nameChannel] = videosID
                    continue
                for videoID in videosID:
                    if videoID not in videos[nameChannel]:
                        videoURL = f"htps://youtu.be/{videoID}"
                        await linkChannel.send(f"**{nameChannel}** has uploaded a new video \n\n {videoURL}")
                videos[nameChannel] = videosID
