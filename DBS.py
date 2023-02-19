import nextcord
from nextcord.ext import commands
from spotipy.oauth2 import SpotifyOAuth
import spotipy


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
check = []
playlist_list = []

@bot.event
async def on_message(ctx):
    messages = await ctx.channel.history(limit=1).flatten()
    for message in messages:
        check.clear()
        results.clear()
        if "https://open.spotify.com/" in message.content:
            spotify_message = message.content.split()[0]
            spotify_link = spotify_message.split("?")[0]
            if spotify_link not in check:
                check.append(spotify_link)
            playlist = sp.playlist_items(
                playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=("track",))
            for item in playlist["items"]:
                track = item.get("track")
                if track:
                    url_id = (track["id"])
                    track_url = "https://open.spotify.com/track/" + url_id
                    if track_url not in playlist_list:
                        playlist_list.append(track_url)
            for song in check:
                if song not in playlist_list:
                    results.append(song)
                    if results not in playlist_list:
                        sp.playlist_add_items(playlist_id, items=results, position=None)
                        await message.reply("I added the song to the playlist")
                if song in playlist_list:
                    await message.reply("Song is already in the playlist")



bot.run(token)
