import json, SentenceGeneratorFactory
import classes_parser
import tkinter as tk
from tkinter import filedialog
import sys

root = tk.Tk()
root.withdraw()

nb = 100
if len(sys.argv) == 2:
    nb = int(sys.argv[1])

file_path = filedialog.askopenfilename(filetypes=["excel .xlsx"])

data = classes_parser.parse(file_path)

json_class_path = filedialog.asksaveasfilename(filetypes=["json .json"])
with open(json_class_path, "w", encoding="utf-8") as file:
    file.write(json.dumps(data, indent=4, ensure_ascii=False))
builder = SentenceGeneratorFactory.UgoFreshSentenceGeneratorFactory().generate()

json_class_path = filedialog.asksaveasfilename(filetypes=["json .json"])
with open(json_class_path, "w", encoding="utf-8") as file:
    file.write(json.dumps(builder.buildSentences(data, count=nb), indent=4, ensure_ascii=False))