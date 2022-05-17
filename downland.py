import shutil
import sys
import os
import time
import datetime

from tqdm import tqdm
import requests

a = time.time()

COMMAND = sys.argv[1:]

DATES = COMMAND[:2]

URL = 'https://api.zoom.us/v2/users/me/'

JWT = input('Введите JWT токен: ')

TOTAL_MEETINGS = 0
TOTAL_FILES = 0


def main(directory):
    date_from = [date for date in DATES if 'date_from' in date][0].split('=')[1]
    date_to = [date for date in DATES if 'date_to' in date][0].split('=')[1]
    month_from_to = []
    for date in (date_from, date_to):
        if date.split('-')[1][0] == '0':
            month_from_to.append(int(date.split('-')[1][1]))
        else:
            month_from_to.append(int(date.split('-')[1]))
    days_from_to = []
    for date in (date_from, date_to):
        if date.split('-')[2][0] == '0':
            days_from_to.append(int(date.split('-')[2][1]))
        else:
            days_from_to.append(int(date.split('-')[2]))
    year_from = int(date_from.split('-')[0])
    year_to = int(date_to.split('-')[0])
    if year_from == year_to:
        if month_from_to[0] == month_from_to[1]:
            start_date = datetime.datetime(year_from, month_from_to[0], days_from_to[0])
            next_date = datetime.datetime(year_to, month_from_to[1], days_from_to[1])
            print(start_date, next_date)
            downland(directory, start_date, next_date)
        else:
            for month in range(month_from_to[0], month_from_to[1]):
                next_month = month + 1
                start_date = datetime.datetime(year_from, month, 1)
                next_date = datetime.datetime(year_to, next_month, 1)
                if next_month == month_from_to[1]:
                    next_date = datetime.datetime(year_to, next_month, days_from_to[1])
                if month == month_from_to[0] or (month == month_from_to[0] and next_month == month_from_to[1]):
                    start_date = datetime.datetime(year_to, month, days_from_to[0])
                print(start_date, next_date)
                downland(directory, start_date, next_date)
    else:
        month_in_year = 13
        for year in range(year_from, year_to + 1):
            if year == year_from:
                month_start = month_from_to[0]
            else:
                month_start = 1
            for month in range(month_start, month_in_year):
                next_month = month + 1
                next_year = year
                if month == 12:
                    if year + 1 == year_to:
                        month_in_year = month_from_to[1]
                    next_month = 1
                    next_year = year + 1
                day = 1
                next_day = 1
                if year == year_from and month == month_from_to[0]:
                    day = days_from_to[0]
                if next_month == month_from_to[1] and next_year == year_to:
                    next_day = days_from_to[1]
                start_date = datetime.datetime(year, month, day)
                next_date = datetime.datetime(next_year, next_month, next_day)
                print(start_date, next_date)
                downland(directory, start_date, next_date)


def downland_recording(downland_url, topic, fyle_type, save_directory):
    try:
        r = requests.get('{}?access_token={}'.format(downland_url, JWT), stream=True)
        if r.status_code == 200:
            with open(r'{}'.format(save_directory) + topic + '.{}'.format(fyle_type.lower()), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    except requests.RequestException as problem:
        raise ConnectionError('Превышено количество запросов, ошибка: {}'.format(problem))


def downland(save_directory, start_date, next_date, ):
    date_string = '%Y-%m-%d'
    response_data = requests.get(
        '{}recordings?from={}&to={}'.format(URL, start_date.strftime(date_string),
                                            next_date.strftime(date_string)),
        headers={
            'Authorization':
                'Bearer {}'.format(JWT)}).json()
    global TOTAL_FILES
    os.chdir(save_directory)
    for meeting in tqdm(response_data['meetings']):
        TOTAL_FILES += len(meeting['recording_files'])
        if not os.path.isdir(dir := '{}_{}'.format(meeting['topic'], meeting['start_time'])):
            if '/' in dir:
                dir = dir.replace('/', '')
            os.mkdir(dir)
        for recording_file in meeting['recording_files']:
            downland_recording(recording_file['download_url'],
                               meeting['topic'],
                               recording_file['file_type'],
                               save_directory + f'{dir}/')
    global TOTAL_MEETINGS
    TOTAL_MEETINGS += len(response_data['meetings'])


if __name__ == '__main__':
    if directory := COMMAND[2:]:
        main(directory[0].split('=')[1])
    else:
        if not os.path.isdir('videos'):
            os.mkdir('videos')
        main('{}/videos/'.format(os.getcwd()))
    print(f'Всего встреч скачалось: {TOTAL_MEETINGS}')
    print(f'Всего файлов скачалось: {TOTAL_FILES}')
    print(f'Время скачивания: {time.time() - a}')
