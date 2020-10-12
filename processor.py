from enums import ChangeType
import json


class Processor(object):
	def __init__(self):
		self.data = None
		with open("files/mixtape.json") as file:
			self.data = json.load(file)
		'''
		mixtape.json was downloaded and stored in the files directory but
		we can get it through GET request as well using the requests module like below
		import requests
		self.data = requests.get(url, headers={"Content-Type":"application/json"}).json()
		'''

	def processChanges(self):
		with open("files/changes.json") as file:
			changes = json.load(file)

		for change in changes:
			# Adding a Playlist
			if change == ChangeType.AddPlayList.value:
				user_id = changes[change]["user_id"]
				song_ids = changes[change]["song_ids"]
				self._addPlaylist(user_id, song_ids)

			# Removing a Playlist
			elif change == ChangeType.RemovePlaylist.value:
				playlist_id = changes[change]
				self._removePlaylist(playlist_id)

			# Updating a Playlist
			elif change == ChangeType.UpdatePlaylist.value:
				playlist_id = changes[change]["id"]
				song_id = changes[change]["song_id"]
				self._updatePlaylist(playlist_id, song_id)

		with open("files/output.json", "w") as file:
			json.dump(self.data, file, indent=4, cls=json.JSONEncoder)

	def _addPlaylist(self, user_id, song_ids):
		# Playlist id is generated by incrementing the id of the last playlist, assuming playlists are in order
		playlist = {}
		last_playlist = self.data["playlists"][-1]
		playlist_id = int(last_playlist["id"]) + 1
		playlist["id"] = str(playlist_id)
		playlist["user_id"] = user_id

		# if song_ids are not provided then pick the first song_id for the playlist
		if len(song_ids) == 0:
			song_ids = [self.data["songs"][0]["id"]]
		playlist["song_ids"] = song_ids
		self.data["playlists"].append(playlist)

	def _removePlaylist(self, playlist_id):
		# Assuming playlists are in order, performing  a binary search to find the playlist
		index = self._findIndex(playlist_id, "playlists")
		if index >= 0:
			del self.data["playlists"][index]
		else:
			print("playlist {} is not found in mixtape.json".format(playlist_id))

	def _updatePlaylist(self, playlist_id, song_id):
		# assuming playlist and songs are in order, performing a binary search to get the playlist
		# and to verify that given song is existing in songs
		playlist_index = self._findIndex(playlist_id, "playlists")

		if playlist_index >= 0:
			song_index = self._findIndex(song_id, "songs")
			if song_index >= 0:
				self.data["playlists"][playlist_index]["song_ids"].append(song_id)
			else:
				print("song {} is not found in mixtape.json".format(song_id))
		else:
			print("playlist {} is not found in mixtape.json".format(playlist_id))

	def _findIndex(self, search_id, key):
		# Binary Search
		low = 0
		high = len(self.data[key])

		while low < high:
			mid = (low + high) // 2
			if self.data[key][mid]["id"] == search_id:
				return mid
			elif int(search_id) < int(self.data[key][mid]["id"]):
				high = mid
			else:
				low = mid

			if mid in [0, len(self.data[key]) - 1]:
				return -1