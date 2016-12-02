import os
import re

paths_pos = ("reviews/part1/pos", "reviews/par2/pos")
paths_neg = ("reviews/part1/neg", "reviews/par2/neg")
out_file  = "frases.arff"

files_pos = []
files_neg = []

#replace = ((',', ' '), ('.', ' '), ("'ve", " have"), ("n't", " not"),
#           ("i am", "i_am"), ("<br>", " "), ("<br />", " "),
#           ("<br/>", " "), ("'", "_"), ('-', ' '), ('"', ' '),
#           (';', ' '), ('(', ' '), (')', ' '), ('!', ' '),
#           ('?', ' '), (':', ' '), ('*', ' '))
#

replace = (("'ve", " have"), ("n't", " not"),
           ("i am", "i_am"), ("<br>", " "), ("<br />", " "),
           ("<br/>", " "), ("_", " "), ("'", "_"))

re1 = re.compile("[^a-z_]+") # Remove chars malucos, pontuacao e varios espacos juntos

for path in paths_pos:
    for dirname, subdirs, filenames in os.walk(path):
        for filename in filenames:
            files_pos.append(os.path.join(dirname, filename))

for path in paths_neg:
    for dirname, subdirs, filenames in os.walk(path):
        for filename in filenames:
            files_neg.append(os.path.join(dirname, filename))

arff = open(out_file, "w")
arff.write("@RELATION imdb\n")
arff.write("@ATTRIBUTE review STRING\n")
arff.write("@ATTRIBUTE class  {P, N}\n")
arff.write("@DATA\n")

# List , class
def write_list(l, c):
    for fn in l:
        f = open(fn)
        s = f.read()
        f.close()
        s = s.lower()
        for fnd, repl in replace:
            s = s.replace(fnd, repl)

        s = re1.sub(" ", s)
        s = "'" + s + "'," + c + "\n"
        arff.write(s)

write_list(files_pos, "P")
write_list(files_neg, "N")
arff.close()
