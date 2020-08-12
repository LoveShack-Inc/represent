import PyPDF2

file = open('2020SV-00052-R00HB06004-SV.PDF', 'rb')

fileReader = PyPDF2.PdfFileReader(file)

page = fileReader.getPage(0)
page_content = page.extractText()
print(page_content.encode('utf-8'))