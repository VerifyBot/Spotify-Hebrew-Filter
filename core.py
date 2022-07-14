import itertools
import spotipy
import configparser

def get_api(config_filename) -> spotipy.Spotify:
  """
  Get spotify API object from config file.
  :param config_filename: config file name
  :return: spotify API object
  """
  config = configparser.ConfigParser()
  config.read(config_filename)

  auth_manager = spotipy.SpotifyOAuth(**config['spotify'])
  api = spotipy.Spotify(auth_manager=auth_manager)

  return api


def limit_api_action(source, **kw):
  all_items = []

  limit = kw.pop('limit', 100)

  for offset in itertools.count(0, limit):
    items = source(limit=limit, offset=offset, **kw)

    items = items['items']

    all_items += items

    if len(items) < limit:
      break

  return all_items


def get_all_songs(source, **kw):
  """
  Get all songs from a playlist (Bypasses the API limit by making individual requests).
  Example:
     get_all_songs(api.playlist_items, limit=100, playlist_id=playlist_id)
  """
  return limit_api_action(source, **kw)

def action_on_playlist(playlist_id, items, source, **kw):
  """
  Action on playlist (Bypasses the API limit by making individual requests).
  Example:
      action_on_playlist(new_playlist['id'], filtered_songs, api.playlist_add_items)
  """
  max_per_request = 100

  parts = (items[i:i + max_per_request] for i in range(0, len(items), max_per_request))

  position = kw.pop('position', None)
  last_part = []

  for idx, part in enumerate(parts):
    if position:
      position = max(0, idx * len(last_part))
      kw['position'] = position
      last_part = part

    source(playlist_id=playlist_id, items=part, **kw)


def validate_playlist(api, playlist_id) -> str:
  """
  Validate playlist id -- Make sure that the playlist exists before doing actions on it.
  :return: Return the playlist name if success
  """
  try:
    playlist_name = api.playlist(playlist_id=playlist_id, fields=('name'))['name']
  except Exception as exc:
    if 'invalid playlist id' in str(exc).lower():
      raise Exception('[XXX] Invalid Playlist ID - Terminating program')
    raise exc
  else:
    print(f'[?] Playlist: {playlist_name} ({playlist_id})')
    return playlist_name
