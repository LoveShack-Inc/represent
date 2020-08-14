import PyPDF2
import re

file = open('2020SV-00052-R00HB06004-SV.PDF', 'rb')

fileReader = PyPDF2.PdfFileReader(file)

page = fileReader.getPage(0)
page_content = page.extractText()
page_content = page_content.replace('\n', '')
separator = 'The following is the roll call vote:'
after_separator = page_content.split(separator, 1)[1]
after_separator += '\n'

reg_1 = re.compile('( Y | N )(.*?)(?= Y | N | \n)')
reg_result = re.findall(reg_1, after_separator)
reg_2 = re.compile('[a-zA-Z ]')

vote_list = []

for i in range(len(reg_result)):
    t1 = reg_result[i][0]
    t2 = "".join(re.findall(reg_2, reg_result[i][1])).strip()
    vote_list.append((t1, t2))

hi = 0
