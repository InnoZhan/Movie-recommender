import json

with open('data_file.json', 'r') as myfile:

    data=myfile.read()

    with open("new.json", "w") as write_file:
        write_file.write(json.dumps(json.loads(data), sort_keys=True, indent=4))