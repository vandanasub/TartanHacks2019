from PyPDF2 import PdfFileReader, PdfFileMerger
# from pdf2image import convert_from_path
from analyzeImage import run
#import time
from wand.image import Image

def parse(filen):
	resString = ""
	keyPhrases = set()
	opLoc = list()
	with(Image(filename=filen)) as source: 
		images = source.sequence
		pages = len(images)
		for i in range(pages):
			n = i + 1
			newfilename = 'out' + str(n) + '.jpg'
			Image(images[i]).save(filename=newfilename)
		i = 1
		while (i <= pages):
			(res,keyPhr) = run('out' + str(i) + '.jpg', 'out'+str(i)+'.pdf')
			opLoc.append('out'+str(i)+'.pdf')
			resString = resString + res
			keyPhrases = keyPhrases.union(keyPhr)
			i+=1

	merger = PdfFileMerger()
	for pdf in opLoc:
		merger.append(pdf)
	merger.write("result.pdf")

	return (resString, keyPhrases)

print(parse("Calc.pdf"))
