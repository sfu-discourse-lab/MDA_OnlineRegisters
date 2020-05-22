import os
import subprocess
from chardet import detect

# get file encoding type
def get_encoding_type(file):
	with open(file, 'rb') as f:
		rawData = f.read()
	return detect(rawData)['encoding']

def main(corpusPath):
	directory = "./CORE_clean/" + str(corpusPath) + "/"
	for file in os.listdir(directory):
		path = directory + file
		correct_encoding = get_encoding_type(path)
		if correct_encoding == None:
			continue
		rawTag = subprocess.run(['./ark-tweet-nlp-0.3.2/runTagger.sh', path], stdout=subprocess.PIPE).stdout.decode(correct_encoding, "ignore")
		splitList = rawTag.split('\n')
		taggedFinal = ''
		for paragraph in splitList:
			i = 0
			data = paragraph.split("\t")
			## print(text)
			for word in data[0].split(" "):
				if len(word) == 0:
					continue
				taggedFinal = taggedFinal + word + "_" + data[1].split(" ")[i] + " "
				i += 1
		with open("./gimple_tagged/%s/%s_tagged.txt" % (str(corpusPath), file.split('.')[0]), "w") as output:
			 output.write(taggedFinal)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Gimple tag files in directory')
	parser.add_argument('corpusPath', type=str, help='the path to the corpus folder')
	args = parser.parse_args()
	main(args.corpusPath)
