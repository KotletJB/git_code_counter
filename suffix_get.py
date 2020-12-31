import json

lls = []
with open('Programming_Languages_Extensions.json') as f:
    file = json.loads(f.read())
    for element in file:
        try:
            ls = element['extensions']
            for ex in ls:
                lls.append(ex)
        except:
            pass
print(tuple(lls))