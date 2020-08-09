import csv
from tempfile import NamedTemporaryFile
import shutil

list_ids = {}

with open('lists/list_ids.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    for line in csvFile[1:]:
        list_ids[line[0]] = line[1]

def get_max_id(filepath):
    m = 0
    with open('lists/list_ids.csv', mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        for line in csvFile[1:]:
            if line and line[0]:
                m = max(m, int(line[0], 16))
    return m


for subdir, dirs, files in os.walk("/lists/"):
    for file in files:
        filepath = subdir + os.sep + file
        if file.endswith('.csv'):
            list_id = int(list_ids[file[:-4]], 16)
            m = max(get_max_id(filepath) - list_id, 0)
            filename = filepath
            tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

            with open(filename, 'r', newline='') as csvFile, tempfile:
                reader = csv.reader(csvFile, delimiter=',', quotechar='"')
                writer = csv.writer(tempfile, delimiter=',', quotechar='"')

                for row in reader:
                    if row:
                        if not row[0]:
                            row[0] = hex(list_id + m)
                            m += 1
                    writer.writerow(row)

            shutil.move(tempfile.name, filename)

