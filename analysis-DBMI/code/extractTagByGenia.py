# -*- coding: utf-8 -*-

import subprocess
import csv
import codecs

def geniaHelper(writer, sent):
	sent = sent.replace("\"", "")
	p = subprocess.Popen(['echo "' + sent + '" | ./geniatagger'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = p.communicate()
	#result = "\"" + sent + "\",";
	tempOut = str(out, 'utf-8')
	array = tempOut.splitlines()
	words = ""
	posTags = ""
	for itemlist in array:
		item = itemlist.split("\t")
		if len(item) == 5:
			words += item[0] + "|"
			posTags += item[2] + "|"
	words = words[:-1]
	posTags = posTags[:-1]
	sent = "'" + sent + "'"
	words = "'" + words + "'"
	posTags = "'" + posTags + "'"
	writer.writerow([sent, words, posTags])
	#result += "\"" + words + "\","
	#result += "\"" + posTags + "\""


def main():
	with codecs.open('NOT-headings.txt', "r", encoding='utf-8', errors='ignore') as file:
		lines = file.read().splitlines()
	with open('result.csv', 'w') as outfile:
		fieldnames = ['\'headings\'', '\'words\'', '\'POStags\'']
		writer = csv.writer(outfile, delimiter = ',')
		writer.writerow(fieldnames)
		print(len(lines))
		i = 0
		for line in lines:
			if line != "":
				geniaHelper(writer, line)
				i = i + 1
				print(i)
	print("Success....")


if __name__ == '__main__':
	main()


