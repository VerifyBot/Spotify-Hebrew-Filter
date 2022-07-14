import json
import spotipy
import configparser
from datetime import datetime
import argparse
import re

from core import get_all_songs, action_on_playlist, validate_playlist, get_api, limit_api_action
from filter_songs import filter_playlist_songs, print_stats, languages


def filter_library(filter_language, user_id=None):
  """
  Filters all the songs in a library by the language.

  :param filter_language: What language to filter by (he/en).
  :param user_id: Optional user ID if you want to filter someone else's library.
  """
  api = get_api('config.ini')

  playlists = limit_api_action(api.user_playlists, user=user_id or api.me()['id'], limit=50)

  songs = []
  filtered_songs = []
  song_c, artist_c = 0, 0
  only_artist, only_song = set(), set()

  for playlist in playlists:
    psongs = get_all_songs(api.playlist_items, limit=100, playlist_id=playlist['id'])
    fs, sc, ac, oa, os = filter_playlist_songs(psongs, filter_language)

    songs.extend(psongs)
    filtered_songs.extend(fs)
    song_c += sc
    artist_c += ac
    only_artist |= oa
    only_song |= os

  # analyze and act on the filtered songs
  print_stats(filter_language, songs, filtered_songs, song_c, artist_c, only_artist, only_song)

  # create a new playlist for the filtered songs
  pname = f'{languages[filter_language]} - {"User " + user_id if user_id else "Your Library"}'
  pdesc = f'{languages[filter_language]} filtered version {"User " + user_id if user_id else "Your"} Library'
  new_playlist = api.user_playlist_create(user=api.me()['id'], name=pname, public=False, description=pdesc)
  action_on_playlist(new_playlist['id'], filtered_songs, api.playlist_add_items)

  print(f'>> Filtered songs were saved to a new playlist:')
  print(f'>> {new_playlist["external_urls"]["spotify"]}')


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('language', choices=['en', 'he', 'custom'], type=str, help='Language to filter (en/he)')
  parser.add_argument('--user', type=str, help='If you want to filter someone else\'s library, put their ID here',
                      required=False, default=None)
  args = parser.parse_args()

  FILTER_LANGUAGE = args.language
  USER_ID = args.user

  filter_library(filter_language=FILTER_LANGUAGE, user_id=USER_ID)
