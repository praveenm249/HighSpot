from enum import Enum


class ChangeType(Enum):
	AddPlayList = 'add'
	RemovePlaylist = 'remove'
	UpdatePlaylist = 'update'
