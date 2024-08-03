import re

f = open('task_1_lamps_testing.txt', 'r')
m = []  # массив отбираемых лампочек m
s = []  # массив неисправнех лампочек s

first_line = f.readline()
parts = first_line.split(", ")
N = int(parts[0].split(": ")[1]) # общее количество проверяемых лампочек
Nexp = int(parts[1].split("=")[1]) # количество проверок
f.readline()
for str in f:
    match = re.search(r"'m': (\d+), 's': (\d+)", str)
    result = [int(match.group(1)), int(match.group(2))]
    m.append(result[0])
    s.append(result[1])
f.close()