#!/usr/bin/env python3

import os
import subprocess
import re 
import tqdm

list_of_subfixs = ('.py','.cpp','.hpp','.h','.c')
list_of_links_to_repos = ['https://github.com/KotletJB/file_observer.git','https://github.com/marcusva/py-sdl2.git','https://github.com/mx0c/super-mario-python.git']

Words_dict = {}
Lines = 0
Sings = 0
Words = 0

for repo in list_of_links_to_repos:
    name_of_repo = re.findall('/([0-9A-Za-z_-]+)\.git',repo)[0]
    subprocess.run(['git', 'clone', repo])

    thisdir = os.getcwd() + '/' + name_of_repo
    # r=root, d=directories, f = files
    for r, d, f in os.walk(thisdir):
        for file in f:
            if file.endswith(list_of_subfixs):
                fille = os.path.join(r, file)
                with open(fille) as f:
                    list_of_lines = f.readlines()
                    Lines += len(list_of_lines)

                    for line in list_of_lines:
                        Sings += len(line)
                        lin = line.strip().split()
                        Words += len(lin)
                        for word in lin:
                            if word not in Words_dict:
                                Words_dict[word] = 1
                            else:
                                Words_dict[word] += 1

    subprocess.run(['rm', '-rf', name_of_repo])

print('Lines:',Lines)
print('Words:',Words)
print('Sings:',Sings)
sort_dic = dict(sorted(Words_dict.items(), key= lambda item: item[1], reverse=True))
print(sort_dic)    