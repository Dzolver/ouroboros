import csv
list_of_lists = []
xlist = [1,2,3]
titles = []
abstracts = []
#get first column only without header
with open('exampleData.csv','r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(str(row)+'\n')
            line_count += 1
        else:
            titles.append(row[0])
            abstracts.append(row[1])
            print(str(row[0])+'\n')
            line_count += 1
    print(f'Processed {line_count} lines.')

print(titles)
print(abstracts)