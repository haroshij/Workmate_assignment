import os
import sys
import pytest
from main import ReportGenerator


class MockParser:
    def __init__(self, files=None, report='performance'):
        self.files = files
        self.report = report


def make_report_generator(files=None, report='performance'):
    report_generator = ReportGenerator()
    parse_args = MockParser(files=files, report=report)
    report_generator.args = parse_args
    return report_generator


def test_init():
    report_generator = ReportGenerator()
    assert isinstance(report_generator, ReportGenerator)


def test_parse_arguments(monkeypatch):
    # Подменяем системные аргументы командной строки.
    test_argv = [
        "script.py",
        "-f", "file1.csv", "file2.csv",
        "--report_name", "my_report.csv"
    ]
    monkeypatch.setattr(sys, "argv", test_argv)
    generator = ReportGenerator()
    generator.parse_arguments()
    # Проверяем, что аргументы корректно распарсились.
    assert generator.args.files == ["file1.csv", "file2.csv"]
    assert generator.args.report == "my_report.csv"


def test_are_filenames_not_exists():
    report_generator = make_report_generator()
    with pytest.raises(ValueError, match="Must specify the file name or file names."):
        report_generator.process_files()


def test_are_filenames_exists():
    report_generator = make_report_generator(['file_1', 'file_2'])
    assert report_generator.args.files == ['file_1', 'file_2']


def test_process_files():
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv'],
        report='test_report.csv'
    )
    report_generator.process_files()
    assert os.path.exists('data_tmp.csv')
    report_generator.delete_temp_data()


def test_delete_temp_data():
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv']
    )
    report_generator.process_files()
    report_generator.delete_temp_data()
    assert os.path.exists('data_tmp.csv') is False


def test_save_report_with_default_name():
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
    report_generator = make_report_generator(
        ['test_employees1.csv', 'test_employees2.csv']
    )
    report_generator.process_files()
    report_generator.make_a_performance_report()
    assert report_generator.__getattribute__("report_data")
