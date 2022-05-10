import sys
import os

from dotenv import load_dotenv
import requests
import urllib.request

load_dotenv()

COMMAND = sys.argv[1:]

DATES = COMMAND[:2]

URL = 'https://api.zoom.us/v2/users/me/recordings?from={}&to={}'.format(
    [date for date in DATES if 'date_from' in date][0].split('=')[1],
    [date for date in DATES if 'date_to' in date][0].split('=')[1])


def downland_recording(save_directory=''):
    response_data = requests.get(
        URL,
        headers={
            'Authorization':
                'Bearer {}'.format(os.getenv('JWT'))}).json()
    if save_directory == '':
        if not os.path.isdir('videos'):
            os.mkdir('videos')
        save_directory = '{}/videos/'.format(os.getcwd())
    for index, meeting in enumerate(response_data['meetings']):
        print(f'Скачиваем запись {index + 1}')
        for recording_file in meeting['recording_files']:
            urllib.request.urlretrieve(
                recording_file['download_url'],
                save_directory + meeting['start_time'])


if __name__ == '__main__':
    if directory := COMMAND[2:]:
        downland_recording(directory[0].split('=')[1])
    else:
        downland_recording()
