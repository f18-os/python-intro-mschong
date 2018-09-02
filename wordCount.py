import sys       
import re   

input = sys.argv[1]
output = sys.argv[2]
dict = {}
list = []

with open(input, 'r') as inputF:
	for line in inputF:
		words = filter(None, re.split("[.,'!?:;\- \n\"]+", line))
		for item in words:
			if item.lower() not in dict:
				dict[item.lower()] = 1
				list.append(item.lower())
			else:
				dict[item.lower()] += 1
list.sort()

outputF = open(output, 'w')
for item in list:
	outputF.write(item + " " + str(dict[item]) + "\n")
outputF.close()