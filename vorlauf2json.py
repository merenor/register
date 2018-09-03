import json

names = []
counter = 0

# read names from a vorlaufregister-file
with open("vorlauf.txt", 'r', encoding="utf-8") as f:
    for line in f:
        if '  ' in line.strip():
            try:
                name,pages = line.split("  ", 1)
            except:
                print("FEHLER bei Trennung von {}".format(line))
        else:
            name = line
            pages = None

        stripped_list = []

        if pages:
            for p in pages.split(", "):
                try:
                    page = int(p.strip())
                except:
                    print("Fehler mit '{}' bei {}".format(p, name))
                    page = None

                if page:
                    stripped_list.append(page)


        names.append({'name': name.strip(), 'pages': stripped_list})

with open("vorlauf.json", "w") as f:
    f.write(json.dumps(names))
