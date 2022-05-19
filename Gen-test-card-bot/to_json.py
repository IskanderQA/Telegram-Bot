# Генератор json с запрещенными словами из файла txt

import json

simple_array = []

with open('censure.txt', encoding='utf-8') as text_file:
    for i in text_file:
        n = i.lower().split('\n')[0]
        if n != '':
            simple_array.append(n)

with open('censure.json', 'w', encoding='utf-8') as json_file:
    json.dump(simple_array, json_file)
