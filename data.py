import csv
import datetime
from pprint import pprint

icebreakers = [
    [
        9152959, '8417493'
    ],
    [
        9077549, 'Ямал'
    ],
    [
        8417481, 'Таймыр'
    ],
    [
        8417493, 'Вайгач'
    ]
]

icebreakers_requests = []
with open('files/requests.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        # if index > 10:
        #    break
        icebreakers_requests.append(row)

start_points = ['начальная точка в Баренцевом море', 'Сабетта-1', 'Сабетта-2', 'Сабетта-3']
end_points = ['начальная точка в Баренцевом море', 'Сабетта-1', 'Сабетта-2', 'Сабетта-3']

edges = {
    1: 440.25,
    2: 450.04,
    3: 169.16,
    4: 752.79,
    5: 376.88,
    6: 257.60,
    7: 123.36,
    8: 33.15,
    9: 72.40,
    10: 85.96,
    11: 15.78,
    12: 45.52,
    13: 15.65,
    14: 256.72
}

routes = {
    'начальная точка в Баренцевом мореСабетта-3': [[11, 10, 9, 8, 7, 6, 5], [11, 10, 9, 8, 7, 3, 2, 1, 4]],
    'Сабетта-3начальная точка в Баренцевом море': [[11, 10, 9, 8, 7, 6, 5][::-1], [11, 10, 9, 8, 7, 3, 2, 1, 4][::-1]],
    'Сабетта-2начальная точка в Баренцевом море': [[13, 12, 10, 9, 8, 7, 6, 5], [13, 12, 10, 9, 8, 7, 3, 2, 1, 4]],
    'начальная точка в Баренцевом мореСабетта-2': [[13, 12, 10, 9, 8, 7, 6, 5][::-1],
                                                   [13, 12, 10, 9, 8, 7, 3, 2, 1, 4][::-1]],
    'Сабетта-1начальная точка в Баренцевом море': [[14, 12, 10, 9, 8, 7, 6, 5], [14, 12, 10, 9, 8, 7, 3, 2, 1, 4]],
    'начальная точка в Баренцевом мореСабетта-1': [[14, 12, 10, 9, 8, 7, 6, 5][::-1],
                                                   [14, 12, 10, 9, 8, 7, 3, 2, 1, 4][::-1]]
}

day_ice = []
with open('files/day_ice.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        # if index > 10:
        #    break
        day_ice.append(row)

ice_can = []
with open('files/ice_can.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        # if index > 10:
        #    break
        ice_can.append(row)

skip_status = {
    1: 'Самостоятельно',
    2: 'Нужна проводка',
    3: 'Проход невозможен'
}
class_can = {
    'No ice class': 0,
    'Arc1': 1,
    'Arc2': 2,
    'Arc3': 3,
    'Arc4': 4,
    'Arc5': 5,
    'Arc6': 6,
    'Arc7': 7,
    'Arc8': 8,
    'Arc9': 9,
    'Arc10': 10,
}