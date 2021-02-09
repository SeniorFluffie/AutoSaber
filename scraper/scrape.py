import os
import zipfile
from beatmap_scraper import BeatmapScraper

ID_PREFIX = 'Lucy - Beat Saber Maps/'
ID_PREFIX_LENGTH = len(ID_PREFIX)
ID_LENGTH = 5

# iterate through all beatmap archives in the data directory
def get_beatmap_ids(dataset_path):
    beatmap_ids = []
    for filename in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, filename)
        archive = zipfile.ZipFile(file_path, 'r')
        with archive as beatmap_archive:
            beatmap_ids += get_archive_ids(beatmap_archive)
    return beatmap_ids

# scrape all files in the provided archive
def get_archive_ids(archive):
    ids = []
    for beatmap_file in archive.namelist():
        ids.append(beatmap_file[ID_PREFIX_LENGTH : ID_PREFIX_LENGTH + ID_LENGTH].strip('('))
    return ids

if __name__ == "__main__":
    # get current working directory 
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    dataset_path = os.path.join(parent_dir, 'dataset', 'data')
    # scrape beatmaps
    beatmap_ids = get_beatmap_ids(dataset_path)
    beatmap_scraper = BeatmapScraper(beatmap_ids)
