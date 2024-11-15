
from pprint import pprint
import re
import ast
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

# Задание 1

# Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
# В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.
# Подсказка: работайте со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" "), регулярки здесь НЕ НУЖНЫ.

def split_name(row):
  if row[0] and row[1] and row[2]:
    pass

  elif row[0] and not row[1] and not row[2]:
    name_parts = row[0].split()
    if len(name_parts) == 3:
      row[0], row[1], row[2] = name_parts
    elif len(name_parts) == 2:
      row[0], row[1] = name_parts
    elif len(name_parts) == 1:
      row[0] = name_parts[0]

  elif row[0] and row[1] and not row[2]:
    name_parts = row[1].split()
    if len(name_parts) == 2:
      row[1], row[2] = name_parts
    elif len(name_parts) == 1:
      row[2] = ""

  elif row[0] and not row[1] and row[2]:
    name_parts = row[0].split()
    if len(name_parts) == 2:
      row[0], row[1] = name_parts

  return row

contacts_list[1:] = (split_name(row) for row in contacts_list[1:])
# for row in contacts_list:
#     print(row)


# задание 2
# Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999. Подсказка: используйте регулярки для обработки телефонов.

pattern = r"(\+7|8)\W*(\d{3})\W*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:[\s-]*(?:\(?((доб\.)?)\s*(\d+)\)?)?)?"
subst = r"+7(\2)\3-\4-\5 \7\8"

result = re.sub(pattern, subst, str(contacts_list), 0, re.MULTILINE)

# if result:
#     pprint (result)


# задание 3
# Объединить все дублирующиеся записи о человеке в одну. Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).

data = ast.literal_eval(result)


headers = data[0]
people_data = data[1:]

people_dict = {}

for person in people_data:
  last_name  = person[0]
  first_name = person[1]
  patronymic = person[2] if person[2] else ''

  # full_name = f"{last_name}, {first_name}" # не срабатывает, просто удаляет отчество всем

  full_name = f"{last_name}, {first_name}, {patronymic}"

  if full_name not in people_dict:
    people_dict[full_name] = {
      'lastname': last_name,
      'firstname': first_name,
      'surname': patronymic,
      'organization': person[3],
      'position': person[4],
      'phone': person[5].strip(),
      'email': person[6].strip()
    }

  else:
    if patronymic and not people_dict[full_name]['surname']:
      people_dict[full_name]['surname'] = patronymic

    if person[4]:
        if people_dict[full_name]['position']:
          people_dict[full_name]['position'] += ' ' + person[4]
        else:
          people_dict[full_name]['position'] = person[4]

    if person[5].strip():
        if people_dict[full_name]['phone']:
          people_dict[full_name]['phone'] += ' ' + person[5].strip()
        else:
          people_dict[full_name]['phone'] = person[5].strip()
    if person[6].strip():
        if people_dict[full_name]['email']:
          people_dict[full_name]['email'] += ' ' + person[6].strip()
        else:
          people_dict[full_name]['email'] = person[6].strip()


result1 = [headers]
for full_name, data in people_dict.items():
  name_parts = full_name.split()

  first_name = name_parts[0] if len(name_parts) > 0 else ""
  last_name = name_parts[1] if len(name_parts) > 1 else ""
  patronymic_name = name_parts[2] if len(name_parts) > 2 else ""

  row = [first_name, last_name, patronymic_name]
  row.extend([data['organization'], data['position'], data['phone'], data['email']])
  result1.append(row)

# for row in result1:
#   print(row)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
#   # Вместо contacts_list подставьте свой список
  datawriter.writerows(result1)