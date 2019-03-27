import os

# returns the name of the converted pdf
def conversion(file, fileName):
	# fileName = 'hello.mid'

	# substitute this with the place where MuseScore is stored
	cmd = "/Applications/MuseScore\ 3.app/Contents/MacOS/mscore -o "

	# creating the name for the pdf
	pdfName = "'" + fileName[:fileName.find('.')] + '.pdf' "' "
	cmd = cmd + pdfName + "'" + fileName + "'"

	# making the system call with the command for conversion
	os.system(cmd)

	return pdfName
