import json
import spotipy
import configparser
from datetime import datetime
import argparse
import re

from core import get_all_songs, action_on_playlist, validate_playlist, get_api

languages = {'he': 'Hebrew', 'en': 'English', 'custom': 'Custom'}


def filter_playlist_songs(songs, filter_language):
  assert filter_language in ('he', 'en', 'custom'), "Invalid language provided -- must be 'he' or 'en'"

  if filter_language == 'custom':
    language_symbols = input('[?] Enter your unique lanaguage symbols: ')
    filter_callback = lambda s: bool(re.search(r'[{}]'.format(language_symbols), s))
  else:
    # basically hebrew means includes אבגדהוזחטיכלמנסעפצקרשתףךץןם and the rest is english
    HEBREW_REGEX = re.compile(r'[אבגדהוזחטיכלמנסעפצקרשתףךץןם]')
    CALLBACKS = {
      'he': lambda s: bool(HEBREW_REGEX.search(s)),
      'en': lambda s: not bool(HEBREW_REGEX.search(s)),
    }

    filter_callback = CALLBACKS[filter_language]

  filtered_songs = []

  # stats
  song_c, artist_c = 0, 0
  only_artist, only_song = set(), set()

  for song in songs:
    song_name_search = filter_callback(song['track']['name'])
    artist_name_search = filter_callback("".join(artist['name'] for artist in song['track']['artists']))

    # statistics for fun
    if song_name_search: song_c += 1
    if artist_name_search: artist_c += 1
    if artist_name_search and not song_name_search: only_artist.add(song['track']['name'])
    if song_name_search and not artist_name_search: only_song.add(song['track']['name'])

    if song_name_search or artist_name_search:
      filtered_songs.append(song['track']['id'])

  return filtered_songs, song_c, artist_c, only_artist, only_song


def print_stats(filter_language, songs, filtered_songs, song_c, artist_c, only_artist, only_song):
  print('=== Statistics ===')
  print(f'~@ Filtering language: {languages[filter_language]}')
  print(f'~@ Filtered songs: {len(filtered_songs)}/{len(songs)}')
  print(f'~@ Filtered songs by song name: {song_c}')
  print(f'~@ Filtered songs by artist name: {artist_c}')
  print(f'~@ Filtered songs by artist name and no song name: {len(only_artist)}')
  # if only_artist: print("\t", "\n\t ".join(only_artist))
  print(f'~@ Filtered songs by song name and no artist name: {len(only_song)}')
  print('====================\n')


def filter_playlist(playlist_id, filter_language):
  """
  Filters all the songs in a playlist by the language.
  :param playlist_id: The playlist id.
  :param filter_language: What language to filter by (he/en).
  """
  api = get_api('config.ini')

  playlist_name = validate_playlist(api, PLAYLIST_ID)

  songs = get_all_songs(api.playlist_items, limit=100, playlist_id=playlist_id)

  filtered_songs, song_c, artist_c, only_artist, only_song = filter_playlist_songs(songs, filter_language)

  # analyze and act on the filtered songs
  print_stats(filter_language, songs, filtered_songs, song_c, artist_c, only_artist, only_song)

  # create a new playlist for the filtered songs
  pname = f'{languages[filter_language]} - {playlist_name}'
  pdesc = f'{languages[filter_language]} filtered version of {playlist_name}'
  new_playlist = api.user_playlist_create(user=api.me()['id'], name=pname, public=False, description=pdesc)
  action_on_playlist(new_playlist['id'], filtered_songs, api.playlist_add_items)

  print(f'>> Filtered songs were saved to a new playlist:')
  print(f'>> {new_playlist["external_urls"]["spotify"]}')


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('language', choices=['en', 'he', 'custom'], type=str, help='Language to filter (en/he)')
  parser.add_argument('id', type=str, help='Playlist ID to filter')
  args = parser.parse_args()

  R = r'(?:https:\/\/open\.spotify\.com\/playlist\/)?([^?]*)(?:\?.+)?'
  PLAYLIST_ID = re.match(R, args.id).groups()[0]
  FILTER_LANGUAGE = args.language

  filter_playlist(playlist_id=PLAYLIST_ID, filter_language=FILTER_LANGUAGE)
