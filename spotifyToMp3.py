import spotipy
import winshell
import os
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
from shutil import move
from tqdm import tqdm
invalid_symbols = [":", ".", '"', "*", "?", "/", "\\", "<", ">", "|"]


def getSongsAndArtists():
    # get your credentials from spotify api and put them in a .txt file,
    # first line with the client_id and second line with the server_id
    # then change path to the credentials file
    # connecting with spotify api
    with open(r"C:\Users\Marco\Desktop\stunf\code\spotifyToMp3\credentials.txt") as f:
        [SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET] = f.read().split("\n")
        f.close()
    auth_manager = SpotifyClientCredentials(
        client_id="e76a144f90fa4360a552a9a84138432d", client_secret="1a758b5e76bc44fa85f56bd7d50ccf63")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # reading link
    playlist_code = input("Spotify playlist/album/song link: ")
    if "playlist" in playlist_code:

        playlist_dict = sp.playlist(playlist_code)

        no_of_songs = playlist_dict["tracks"]["total"]

        song_list = []
        artists_list = []
        tracks = playlist_dict["tracks"]
        items = tracks["items"]
        offset = 0
        i = 0
        while i < no_of_songs:
            song = items[i-offset]["track"]["name"]
            artists = [k["name"] for k in items[i-offset]["track"]["artists"]]
            artists = ','.join(artists)
            song_list.append(song)
            artists_list.append(artists)
            if (i+1) % 100 == 0:
                tracks = sp.next(tracks)
                items = tracks["items"]
                offset = i+1
            i += 1
        return song_list, artists_list, playlist_dict["name"]
    elif "album" in playlist_code:
        playlist_dict = sp.album(playlist_code)
        no_of_songs = playlist_dict["tracks"]["total"]
        songs_of_album = []
        artists_of_album = []
        j = 0
        while j < no_of_songs:
            songs_of_album.append(playlist_dict["tracks"]["items"][j]["name"])
            artists_of_album.append(playlist_dict["label"])
            j += 1
        return songs_of_album, artists_of_album, playlist_dict["name"]
    elif "track" in playlist_code:
        playlist_dict = sp.track(playlist_code)
        artists_track = ""
        for i in range(len(playlist_dict["artists"])):
            artists_track += (playlist_dict["artists"][i]["name"]) + " "
        return playlist_dict["name"], artists_track, playlist_dict["name"]


print(f"\nSpotify to MP3 Program\n")
while(True):
    musica_lista, artista_lista, name = getSongsAndArtists()
    for symbol in invalid_symbols:
        if symbol in name:
            name = name.replace(symbol, "_")
    path = winshell.desktop() + "\\" + name
    if name == musica_lista:
        path = winshell.desktop()

    def getLink(name):
        videosSearch = VideosSearch(name, limit=1)
        return videosSearch.result()["result"][0]["link"]

    def downloadMP3(link):
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
        # download the file
        out_file = video.download(output_path=path)
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        move(out_file, new_file)

    tudo = []
    i = 0
    if name == musica_lista:
        tudo.append(name + " - " + artista_lista)
    else:
        while (i < len(musica_lista)):
            tudo.append(musica_lista[i] + " - " + artista_lista[i])
            i = i + 1

    links = []
    for a in tqdm(range(0, len(tudo))):
        links.append(getLink(tudo[int(a)]))
        downloadMP3(links[a])
    print("Done!\n")
