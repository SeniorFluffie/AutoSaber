import os
import json

class Beatmap:
  __INFO_FILE = 'info.dat'

  def __init__(self, beatmap_files):
    self.root_dir = self.get_root_dir(beatmap_files)
    beatmap_data = self.get_beatmap_data(beatmap_files)
    self.name = beatmap_data['name']
    self.artist = beatmap_data['artist']
    self.author = beatmap_data['author']
    self.BPM = beatmap_data['BPM']
    self.offset = beatmap_data['offset']
    self.filename = beatmap_data['filename']
    self.notes = beatmap_data['notes']

  def __str__(self):
    return "{0} - {1} (Mapped by {2})".format(self.name, self.artist, self.author)

  # generate archive's root directory
  # (needed as some files aren't zipped in an enclosed directory)
  def get_root_dir(self, beatmap_files):
    return ('' if (self.__INFO_FILE in beatmap_files.namelist()  
      or self.__INFO_FILE.capitalize() in beatmap_files.namelist())
      else beatmap_files.namelist()[0])

  # generate path for the beatmaps' info.dat/Info.dat file
  def get_info_path(self, beatmap_files):
    info_file = (self.__INFO_FILE
        if os.path.join(self.root_dir, self.__INFO_FILE) in beatmap_files.namelist()
        else self.__INFO_FILE.capitalize())
    info_path = os.path.join(self.root_dir, info_file)
    return info_path

  # generates dict for note placements (based on difficulty)
  def get_note_placements(self, beatmap_files, difficulties):
    beatmap_levels = difficulties[0]['_difficultyBeatmaps']
    note_placements = []
    for level in beatmap_levels:
      notes = {}
      notes['difficulty'] = level['_difficulty']
      print(notes['difficulty'])
      notes['filename'] = level['_beatmapFilename']
      notes['noteSpeed'] = level['_noteJumpMovementSpeed']
      notes['noteSpawnDistance'] = level['_noteJumpStartBeatOffset']
      notes['notes'] = self.get_note_data(beatmap_files, notes['filename'])
      note_placements.append(notes)
    return note_placements

  # retrieves note placements from corresponding file (Easy.dat, Normal.dat, etc.)
  def get_note_data(self, beatmap_files, file_name):
    note_path = os.path.join(self.root_dir, file_name)
    with beatmap_files.open(note_path) as note_json:
        note_data = json.loads(note_json.read())
        return note_data

  # generates a dict for all song properties
  def get_beatmap_data(self, beatmap_files):
    beatmap_info = {}
    info_path = self.get_info_path(beatmap_files)
    with beatmap_files.open(info_path) as beatmap_json:
        beatmap_data = json.loads(beatmap_json.read())
        beatmap_info['name'] = beatmap_data['_songName']
        beatmap_info['artist'] = beatmap_data['_songAuthorName']
        beatmap_info['author'] = beatmap_data['_levelAuthorName']
        beatmap_info['BPM'] = beatmap_data['_beatsPerMinute']
        beatmap_info['offset'] = beatmap_data['_songTimeOffset']
        beatmap_info['filename'] = beatmap_data['_songFilename']
        beatmap_info['difficulties'] = beatmap_data['_difficultyBeatmapSets']
    beatmap_info['notes'] = self.get_note_placements(beatmap_files, beatmap_info['difficulties'])
    beatmap_info.pop('difficulties', None)
    return beatmap_info

  def get_notes(self):
    return self.notes

