# 🎶 Spotify Hebrew Filter 🎶

Python application to filter out all the Hebrew songs from your Spotify playlist. You can also filter the rest of the
songs (English)

# Usage

First you need a spotify application. If you don't have one, follow this instructions:

- Create a [Spotify Application](https://developer.spotify.com/dashboard/applications)
    - In `Redirect URIs` add:
        - http://localhost:4832/callback
        - http://localhost:4832/callback/
- Put your `Client ID` and `Client Secret` in the `config.ini` file

✨ To use the filter make sure that the first argument is the **langauge** you want to filter and the second argument is
the **playlist id/url**

```shell
py filter_songs.py <en|he> <playlist_id>
```

## Example

📌 In this example, we will filter all the Hebrew songs from the given playlist.

```shell
# Filter Hebrew songs from a playlist
>> py filter_songs.py he https://open.spotify.com/playlist/37i9dQZF1DXdmWiWhAYJ4a

[?] Playlist: "להיטי קיץ 2022 (37i9dQZF1DXdmWiWhAYJ4a)"
  === Statistics ===
~ Filtering language: Hebrew
~ Filtered songs: 53/80
~ Filtered songs by song name: 53
~ Filtered songs by artist name: 5
~ Filtered songs by artist name and no song name: 0
~ Filtered songs by song name and no artist name: 48

Filtered songs were saved to a new playlist:
https://open.spotify.com/playlist/4vulxeFZhNYT67Xz1kMwuH
```

# Extend the filter to all of your spotify library

📂 If you want to filter your whole library into one playlist, you can use the `filter_library.py` script:

```shell
py filter_library.py <he|en>
```

📌 To filter someone else's library, you can use the `filter_library.py` script with the `--user` argument:

```shell
py filter_library.py <he|en> --user <user_id>
``` 

# Filter your own language

To use a custom langauge filter, run the normal script (either playlist or library filter) and put `custom` as the
langauge argument. Once run, you will need to input your language's custom symbols.

Example:

```shell
>> py filter_songs.py custom 37i9dQZF1DXdmWiWhAYJ4a  
[?] Enter your unique lanaguage symbols: אבגדהוזחטיכלמנסעפצקרשתףךץןם

# normal script output... 
``` 
