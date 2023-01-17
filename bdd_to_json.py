import json

json_file = []
with open("BDD_Test", 'r') as f:
    for l in f.readlines():
        if l == "":
            continue
        l = l.replace('\n', '')
        json_file.append({
            "sentence": l,
            "tags": []
        })

with open("training_data.json", 'w') as f:
    f.write(json.dumps(json_file, indent=2))
