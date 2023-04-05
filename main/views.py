import re

from django.shortcuts import render, redirect
from .models import MyModel
from pdfminer.high_level import extract_text, extract_pages
import tabula
from .forms import UploadFileForm


# Create your views here.
def index(request):
    TMP_DIC = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_upload = MyModel(pdf_file=uploaded_file)
            file_upload.save()
            # process the uploaded file here
            # return render(request, 'success.html')

            filename = MyModel.objects.last().id # getting the current upload file name from the DB and
            filepath = MyModel.objects.get(id=filename) # getting the file name
            filepath_PDF = filepath.pdf_file.url # getting the path

            actual_file_path = 'K:/Computer Science (My life)/My Work Station/Django/Project 2/PDFExtractor'+ filepath_PDF

            try: # reading the pdf
                table = tabula.read_pdf(actual_file_path, encoding='cp1252')
                text = extract_text(actual_file_path)
                txtList = text.split('\n')
                newtxt = []
                for words in txtList:
                    # print(words)
                    if words == '':
                        continue
                    newtxt.append(words.strip()) # append and remove additional whitespaces

                reco = newtxt[17]
                print(filepath_PDF)
                try:
                    df = table[0].dropna()

                    df2 = table[1] # dataframe
                    table_headers = []  # store the tables headers
                    leftside = []
                    rightside = []
                    rules_buttom = []

                    middle_Table = []
                    buttom_Table = []
                    pattern = r'\d+\.\d+'  # define a regular expression pattern that matches decimal values
                    for i in df2:
                        if not str(i).startswith('Unnamed'):
                            modified = str(i).split(' ')  # format header
                            if len(table_headers) < 1:
                                table_headers.append(modified)

                    for i in df2.values:
                        # print(i[0])
                        leftside.append([i[0]])
                        rightside.append([str(i[2]) + str(i[4])])
                    del leftside[0]

                    footerTable = leftside[22:27]
                    for i in range(0, len(footerTable)):
                        value = footerTable[i]
                        footerTable[i] = str(value[0]).split(' ')
                    del footerTable[1]
                    # print(footerTable)

                    for i in range(0, len(leftside)):
                        data = leftside[i]
                        # print(leftside[i])
                        if str(data[0]).startswith('9th') or str(data[0]).startswith('10th') or str(data[0]).startswith(
                                '11th') or str(
                            data[0]).startswith('12th'):
                            data1 = str(data[0])
                            if 'e' in list(data1):
                                replace = data1.replace('e', 'e ,')
                                leftside[i] = replace.split(',')
                        # if data[0] == 'nan':
                        #     continue
                        matches = re.findall(pattern,
                                             str(data[0]))  # use the findall() function to find all matches in the string
                        if len(matches) == 0:
                            continue
                        # print(matches[0])
                        # print(leftside[i])
                        if matches[0] in data[0]:
                            modified_data = data[0].replace(matches[0], ',' + matches[0] + ',')
                            leftside[i] = modified_data.split(',')



                    for i in leftside:
                        if str(i[0]) == 'nan':
                            del i[0]

                    # print(leftside)

                    # print(leftside)
                        # elif
                    # print(rule_data)
                    # print(leftside)

                    # print(rightside)

                    for i in range(0, len(rightside)):
                        data = rightside[i]
                        # print(leftside[i])
                        if str(data[0]).startswith('9th') or str(data[0]).startswith('10th') or str(data[0]).startswith(
                                '11th') or str(
                            data[0]).startswith('12th'):
                            data1 = str(data[0])
                            if 'e' in list(data1):
                                replace = data1.replace('e', 'e ,')
                                rightside[i] = replace.split(',')
                        # if data[0] == 'nan':
                        #     continue
                        matches = re.findall(pattern,
                                             str(data[0]))  # use the findall() function to find all matches in the string
                        if len(matches) == 0:
                            continue
                        # print(matches[0])

                        if matches[0] in data[0]:
                            modified_data = data[0].replace(matches[0], ',' + matches[0] + ',')
                            rightside[i] = modified_data.split(',')



                    del rightside[0]
                    for i in rightside:
                        if str(i[0]) == 'nan':
                            del i[0]

                    middle_Table = leftside[:18]
                    buttom_Table = leftside[18:]
                    rrmiddle_table = rightside[:17]
                    rmiddle_table = rightside[18:]
                    modiRmiddle = []
                    for i in range(0, len(rmiddle_table)):
                        t =rmiddle_table[i]
                        if t[0] == 'nannan':
                            continue

                        modiRmiddle.append(rmiddle_table[i])

                    for i in range(0,len(modiRmiddle)):
                        value = modiRmiddle[i]
                        modiRmiddle[i] = value[0].replace('nan', '')

                    # print(modiRmiddle)
                    # print(rightside)

                    button_headers = []
                    # print(middle_Table)

                    headers = buttom_Table[1]
                    buttom_Table[1] = headers[0].split(' ')
                    modi = buttom_Table[1]   # re-structure the tables

                    button_headers.append(modi[0])
                    button_headers.append(modi[1] + ' ' + modi[2])
                    button_headers.append(modi[3] + ' ' + modi[2])
                    button_headers.append(modi[5] + ' ' + modi[6])
                    value = buttom_Table[0]
                    button_headers.append(value[0])
                    # print(button_headers)

                    # print(rightside)
                    del buttom_Table[1]
                    del buttom_Table[2]
                    del buttom_Table[3]
                    del buttom_Table[1]


                    signature = buttom_Table[5:]
                    newsign = []
                    for i in signature:
                        for j in i:
                            newsign.append(j)
                    print(newsign)

                    return render(request, "main/index.html",
                                  {"dataframe": df, "header_list": table_headers, 'leftside': middle_Table,
                                   'rightside': rrmiddle_table,
                                   'form': form, 'pdf': filepath_PDF, 'bheader': button_headers, 'footer':footerTable, "infotable":modiRmiddle, 'signature':newsign, 'record':reco})
                except IndexError:
                    redirect('error')

            except FileNotFoundError:
                redirect('index')
    else:
        form = UploadFileForm()

    return render(request, "main/index.html", {'form': form})


def incorrect(request):
    return render(request, "main/incorrect.html", {})