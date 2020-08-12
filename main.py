import PyPDF2

file = open('2020SV-00052-R00HB06004-SV.PDF', 'rb')

fileReader = PyPDF2.PdfFileReader(file)

page = fileReader.getPage(0)
page_content = page.extractText() # .encode('utf-8')
page_content = page_content.replace('\n', '')
# print(page_content)
separator = 'The following is the roll call vote:'
after_separator = page_content.split(separator, 1)[1]
# print(after_separator)
# post_split = after_separator.split('  ')
# print(post_split)

