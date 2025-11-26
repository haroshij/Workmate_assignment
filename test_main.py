import os   # Необходимо для проверки создания файла.
import sys  # Импортируем для корректности парсинга.
import pytest
from main import ReportGenerator


class MockParser:
    """
    Класс предназначен для имитирования аргументов при парсинге.
    :parameter:
        files (list[str]): список с именами файлов для обработки;
        report (str): имя файла для отчёта
    """

    def __init__(self, files=None, report='performance'):
        self.files = files
        self.report = report


def make_report_generator(files=None, report='performance'):
    """
    Функция формирует и возвращает экземпляр класса ReportGenerator с замоканным аттрибутом args.
    :parameter:
        files (list[str]): список с именами файлов для обработки;
        report (str): имя файла для отчёта
    :return:
        ReportGenerator()
    """
    report_generator = ReportGenerator()
    parse_args = MockParser(files=files, report=report)
    report_generator.args = parse_args
    return report_generator


def test_init():
    """
    Тестирование инициализации экземпляра класса ReportGenerator.
    """
    report_generator = ReportGenerator()
    assert isinstance(report_generator, ReportGenerator)


def test_parse_arguments(monkeypatch):
    """
    Тестирование парсинга аргументов из строки терминала.
    :param monkeypatch: фикстура, позволяющая временно изменять аргументы в строке терминале.
    """
    test_argv = [
        "script.py",
        "-f", "file1.csv", "file2.csv",
        "--report_name", "my_report.csv"
    ]
    monkeypatch.setattr(sys, "argv", test_argv)
    generator = ReportGenerator()
    generator.parse_arguments()
    assert generator.args.files == ["file1.csv", "file2.csv"]
    assert generator.args.report == "my_report.csv"


def test_are_filenames_not_exists():
    """
    Тестирование возбуждения ValueError в случае непередачи имён файлов для обработки.
    """
    report_generator = make_report_generator()
    with pytest.raises(ValueError, match="Must specify the file name or file names."):
        report_generator.process_files()


def test_process_files():
    """
    Тестирование создания временного файла data_tmp.csv.
    """
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv'],
        report='test_report.csv'
    )
    report_generator.process_files()
    assert os.path.exists('data_tmp.csv')
    report_generator.delete_temp_data()


def test_delete_temp_data():
    """
    Тестирование удаления временного файла data_tmp.csv.
    """
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv']
    )
    report_generator.process_files()
    report_generator.delete_temp_data()
    assert os.path.exists('data_tmp.csv') is False


def test_save_report_with_default_name():
    """
    Тестирование создания файла-отчёта по эффективности с именем по умолчанию.
    """
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv']
    )
    report_generator.process_files()
    report_generator.make_a_performance_report()
    report_generator.save_report()
    report_generator.delete_temp_data()
    assert os.path.exists('performance')
    os.remove('performance')


def test_save_report_with_random_name():
    """
    Тестирование создания файла-отчёта по эффективности со случайным именем.
    """
    from string import ascii_letters
    from random import choice, randint
    length = randint(4, 16)
    report_name = ''.join(choice(ascii_letters) for _ in range(length))
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv'],
        report_name
    )
    report_generator.process_files()
    report_generator.make_a_performance_report()
    report_generator.save_report()
    report_generator.delete_temp_data()
    assert os.path.exists(f'{report_name}')
    os.remove(report_name)


def test_print_report(capfd):
    """
    Тестирование вывода отчёта в терминал.
    :param capfd: фикстура, захватывающая вывод в терминал.
    """
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv']
    )
    report_generator.process_files()
    report_generator.make_a_performance_report()
    report_generator.save_report()
    report_generator.delete_temp_data()
    assert report_generator.print_report() is None
    out, err = capfd.readouterr()
    assert out == ("    position      performance\n--  ----------  -------------\n"
                   " 1  fighter              4.50\n 2  cook                 3.50\n")


def test_make_a_performance_report():
    """
    Тестирование формирования отчёта и сохранения его в аттрибут экзаемпляра ReportGenerator.
    """
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv']
    )
    report_generator.process_files()
    report_generator.make_a_performance_report()
    assert report_generator.__getattribute__("report_data")
