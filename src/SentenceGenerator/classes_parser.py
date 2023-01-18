import pandas as pd

def parse(path):
    classes = {}
    class_index = 0
    instances = {}
    sheet = pd.ExcelFile(path)
    pages = pd.read_excel(sheet, sheet_name=None)
    for page in pages:
        for y in range(len(pages[page])):
            for i in range(len(pages[page].columns)):
                column = pages[page].columns[i]
                if(i == 0):
                    classes[str(class_index)] = {
                        "label":str(pages[page][column][y]),
                        "type":page
                    }
                elif(str(pages[page][column][y]) != 'nan'):
                    instances[str(pages[page][column][y])]=str(class_index)
            class_index+=1
    return {"classes":classes, "instances":instances}