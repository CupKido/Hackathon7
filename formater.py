file = open('Test1.txt', 'r')
new_file = open('Test11.txt', 'w')
for x in file.readlines():
    line = x.split(' ')
    if int(line[0]) >= 316 and line[1] == '1':
        line[1] = '2'
    new_file.write(' '.join(line))

file.close()
new_file.close()
