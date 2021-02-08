import os
import zipfile
from beatmap import Beatmap

# retrieve current dir and data dir
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = 'data'
dataset_path = os.path.join(dir_path, data_path)

# iterate through the dataset and load each archive
def load_beatmaps():
    dataset = []
    for filename in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, filename)
        archive = zipfile.ZipFile(file_path, 'r')
        with archive as beatmap_archive:
            dataset += load_beatmap_archive(beatmap_archive)
            return dataset
    return dataset

# iterates through individual songs in the archive
def load_beatmap_archive(archive):
    beatmap_list = []
    for song_path in archive.namelist():
        with archive.open(song_path) as beatmap:
            beatmap_list.append(load_beatmap(beatmap))
    return beatmap_list

# loads song in (from corresponding zip) and converts to custom class
def load_beatmap(beatmap):
    beatmap_archive = zipfile.ZipFile(beatmap, 'r')
    with beatmap_archive as beatmap_files:
        beatmap = Beatmap(beatmap_files)
        return beatmap

beatmaps = load_beatmaps()