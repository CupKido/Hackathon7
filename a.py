import os
# Read the contents of each text file into a list
lines = []
for file in os.listdir(r'C:\Users\Saar\Documents\school\courses\Hackathon7') :
    if 'Test11' in file or 'Test12' in file:
        with open(file, 'r') as f:
            lines.extend(f.readlines())

print(f'num of lines:\t{len(lines)}')

# Parse the index and text from each line
indexed_lines = []
for line in lines:
    try:
        index, text = line.strip().split(' ', 1)
    except:
        continue
    indexed_lines.append((int(index), text))

# Sort the list of tuples by the index
sorted_lines = sorted(indexed_lines, key=lambda x: x[0])

# Write the sorted list to a new text file
with open(r'C:\Users\Saar\Documents\school\courses\Hackathon7\sorted_lines.txt', 'w') as f:
    for index, text in sorted_lines:
        f.write('{}: {}\n'.format(index, text))

