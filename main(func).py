# Импортируем csv для обработки файлов с оценками эффективности.
# Импортируем argparse для парсинга аргументов из терминала.
# Импортируем tabulate для вывода отчёта.
import csv
import argparse
import tabulate

# В данном блоке разбираем аргументы, сохраняем их в переменные files и report
# Добавлен блок "help", а также дополнительные имена для переменных:
# -f, --filenames для имён файлов; -r, --report_name для имени файла-отчёта.
# Если не передать название файлу-отчёту, то он будет называться performance.
parser = argparse.ArgumentParser()
parser.add_argument(
    "--files", "-f", "--filenames",
    type=str,
    default=None,
    help="Employee performance files",
    nargs="*"               # необходимо для приёма нескольких имён файлов
)
parser.add_argument(
    "--report", "-r", "--report_name",
    type=str,
    default="performance",
    help="Job performance report"
)
args = parser.parse_args()

# Заводим временный словарь, куда будем считывать
# результаты по эффективности каждого сотрудника в список.
temp_result = dict()

# Проходимся циклом по каждому файлу.
# Внутри файлов проходимся построчно по каждому сотруднику
# и добавляем необходимую нам информацию в словарь:
# должность (позицию) и оценку эффективности
# Можно сохранять и другие данные, которыми можно будет
# воспользоваться для формирования других отчётов (например,
# сделать отчёт, сколько сотрудников владеют нужной технологией).
for csv_file in args.files:
    with open(csv_file, encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row["position"] not in temp_result:
                temp_result[row["position"]] = list()
            temp_result[row["position"]].append(float(row["performance"]))

# Меняем данные в словаре: список с оценками меняем на среднюю эффективность.
for position, ratings in temp_result.items():
    ratings_sum = sum(ratings)
    rating_count = len(ratings)
    average_rating = round(ratings_sum / rating_count, 2)
    temp_result[position] = average_rating

# Сортируем данные по эффективности, получаем уже список кортежей
# вида [(<должность_1>, <ср. эффективность_1>), ...].
temp_result = sorted(temp_result.items(), key=lambda x: x[1], reverse=True)

# Формируем список словарей из списка кортежей: для записи в csv через DictWriter.
# Добавляем номер (ранг) записи по каждой должности.
result = list()
for n, group in enumerate(temp_result, 1):
    result.append({"": n, "position": group[0], "performance": group[1]})

# Записываем данные в результирующий csv-файл.
with open(args.report, "w", encoding="utf-8", newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=["", "position", "performance"])
    csv_writer.writeheader()
    csv_writer.writerows(result)

# Записываем информацию для вывода отчёта на экран.
# После выводим её.
to_print = tabulate.tabulate(result, headers="keys", floatfmt=".2f")
print(to_print)
