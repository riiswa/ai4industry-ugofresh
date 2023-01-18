import json, SentenceGeneratorFactory
import classes_parser

data = classes_parser.parse("./Donnees.xlsx")
with open("json_data.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(data, indent=4, ensure_ascii=False))
builder = SentenceGeneratorFactory.UgoFreshSentenceGeneratorFactory().generate()
print(json.dumps(builder.buildSentences(data, count=10000), indent=4, ensure_ascii=False))