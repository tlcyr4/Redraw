from __future__ import print_function
import sys
keep = "-k" in sys.argv

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

line2 = f2.readline()
tokens2 = line2.split("\t")

for line1 in f1:
    tokens1 = line1.strip("\n").split("\t")
    while tokens2[0] < tokens1[0]:
        line2 = f2.readline()
        if line2 == "":
            break
        tokens2 = line2.strip("\n").split("\t")
    while tokens2[0] == tokens1[0]:
        tokens1 += tokens2[1:]
        line2 = f2.readline()
        if line2 == "":
            break
        tokens2 = line2.strip("\n").split("\t")
    output = "\t".join(tokens1).replace("\n","")
    print(output)
    # sys.stdout.write(line1)
    # print()
    # if "\n" in output:
        # sys.stderr.write("wtf\n")
