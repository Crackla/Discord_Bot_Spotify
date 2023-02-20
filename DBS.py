import nextcord
from nextcord.ext import commands
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import re


playlist_id = "playlist_id"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="client_id",
                                               client_secret="client_secret",
                                               redirect_uri="http://localhost:8080",
                                               scope="playlist-read-private user-library-read playlist-modify-public"))

token = "token"
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


results = []
playlist_list = []


@bot.event
async def on_message(ctx):
    messages = await ctx.channel.history(limit=1).flatten()
    if ctx.author == bot.user:
        return
    for message in messages:
        if "spotify.com/track" in message.content:
            results.clear()
            spotify_link_pattern = r"(?P<url>https?://(?:open\.|play\.)?spotify\.com/track/[a-zA-Z0-9?=]+)"
            spotify_links = re.findall(spotify_link_pattern, message.content)
            for spotify_link in spotify_links:
                spotify_string = "".join(spotify_link)
                spotify_url = spotify_string.split("?")[0]
                if spotify_url not in results:
                  results.append(spotify_url)
            playlist = sp.playlist_items(
                playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=("track",))
            for item in playlist["items"]:
                track_id = (item["track"]["id"])
                track_url = "https://open.spotify.com/track/" + track_id
                if track_url not in playlist_list:
                    playlist_list.append(track_url)
            for song in results:
                if song not in playlist_list:
                    sp.playlist_add_items(playlist_id, items=[song], position=None)
                    await message.reply("I added this song to the playlist \U0001F600" + "\n" + song)
                if song in playlist_list:
                    await message.reply("This song is already in the playlist \U0001F605" + "\n" + song)



bot.run(token)
