# Импортируем csv для обработки файлов с оценками эффективности.
# Импортируем argparse для парсинга аргументов из терминала.
# Импортируем tabulate для вывода отчёта.
# Импортируем os для удаления временных данных.
import csv
import argparse
import tabulate
import os


class ReportGenerator:
    def __init__(self):
        self.args = None
        self.report_data = None

    # В данном методе разбираем аргументы, сохраняем их в атрибуты files и report
    # Добавлен блок "help", а также дополнительные имена для атрибутов:
    # -f, --filenames для имён файлов; -r, --report_name для имени файла-отчёта.
    # Если не передать название файлу-отчёту, то он будет называться performance.
    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--files", "-f", "--filenames",
            type=str,
            default=None,
            help="Employee performance files",
            nargs="*"  # необходимо для приёма нескольких имён файлов
        )
        parser.add_argument(
            "--report", "-r", "--report_name",
            type=str,
            default="performance",
            help="Job performance report"
        )
        self.args = parser.parse_args()

    # В данном методе формируем данные из файлов в единый файл.
    # Эти данные можно использовать для различных методов.
    # Сохраняем данные в файл data_tmp.csv
    def process_files(self):
        # Проходимся циклом по каждому файлу
        # и добавляем необходимую нам информацию в файл
        if not self.args.files:
            raise ValueError('Необходимо указать имя(-ена) файла(-ов)')

        with open('data_tmp.csv', 'w', newline='') as csvfile:
            with open(self.args.files[0], encoding="utf-8") as file:
                fieldnames = next(csv.reader(file))  # считываем названия столбцов из первого файла
                csv_writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
                csv_writer.writeheader()
            for csv_file in self.args.files:
                with open(csv_file, encoding="utf-8") as file:
                    csv_reader = csv.DictReader(file)
                    csv_writer.writerows(csv_reader)

    # В данном методе формируем отчёт по эффективности
    def make_a_performance_report(self):

        # Внутри файла проходимся построчно по каждому сотруднику
        # и добавляем необходимую нам информацию в словарь:
        # должность (позицию) и оценку эффективности.
        temp_result = dict()
        with open('data_tmp.csv', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
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

        # Формируем список словарей из списка кортежей.
        # Добавляем номер (ранг) записи по каждой должности.
        report_data = list()
        for n, group in enumerate(temp_result, 1):
            report_data.append({"": n, "position": group[0], "performance": group[1]})
        self.report_data = report_data

    # Данный метод сохраняет отчёт в csv-файл.
    def save_report(self):
        with open(self.args.report, "w", encoding="utf-8", newline="") as file:
            fieldnames = list(self.report_data[0].keys())
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(self.report_data)

    # Данный метод выводит отчёт на печать.
    def print_report(self):
        to_print = tabulate.tabulate(self.report_data, headers="keys", floatfmt=".2f")
        print(to_print)

    # Данный метод удаляет файл с временными данными
    @staticmethod
    def delete_temp_data():
        os.remove("data_tmp.csv")


if __name__ == "__main__":
    generator = ReportGenerator()               # Создаём экземпляр Отчётогенератора
    generator.parse_arguments()                 # Парсим аргументы
    try:
        generator.process_files()               # Обрабатываем файлы, мёрджим их во временный файл
        generator.make_a_performance_report()   # Делаем отчёт по эффективности
        generator.save_report()                 # Сохраняем отчёт в csv-файле
        generator.print_report()                # Выводим отчёт на экран
        generator.delete_temp_data()            # Удаляем временный файл
    except ValueError as error:
        print(error)
