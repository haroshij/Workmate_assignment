import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--files",
    type=str,
    default=None,
    help="Employee performance files",
    nargs="*"  # необходимо для приёма нескольких имён файлов
)
parser.add_argument(
    "--report",
    type=str,
    default=None,
    help="Job performance report"
)
args = parser.parse_args()
print(args)

result = dict()

for csv_file in args.files:
    with open(csv_file) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            print(row)

# if __name__ == '__main__':
#     main()
