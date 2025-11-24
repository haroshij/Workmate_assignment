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

temp_result = dict()

for csv_file in args.files:
    with open(csv_file, encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row["position"] not in temp_result:
                temp_result[row["position"]] = list()
            temp_result[row["position"]].append(float(row["performance"]))

for position, ratings in temp_result.items():
    ratings_sum = sum(ratings)
    rating_count = len(ratings)
    average_rating = round(ratings_sum / rating_count, 2)
    temp_result[position] = average_rating

temp_result = sorted(temp_result.items(), key=lambda x: x[1], reverse=True)

result = list()
for n, group in enumerate(temp_result, 1):
    result.append({'': n, 'position': group[0], 'performance': group[1]})


with open(args.report, 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=['', 'position', 'performance'])
    csv_writer.writeheader()
    csv_writer.writerows(result)


# if __name__ == '__main__':
#     main()
