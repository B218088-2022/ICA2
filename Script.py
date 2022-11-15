#!/usr/bin/python3
import os
import pandas as pd
import subprocess
import re

# let use input the protein name and taxonomy group name that they want to use
def identify():
    protein = "_".join(input("please input your protein name\n\t").split())
    taxonomy = "_".join(input("please input the taxonomic group you want to analyse\n\t").split())
    return protein, taxonomy

# prepare a check function to see if the user want to continue or not
def check_continue(information):
    user_info = input(information + " [yes/no]\n\t")
    if user_info.upper().startswith("Y"):
        return True
    else:
        return False

protein, taxonomy = identify()

os.system("esearch -db protein -query '%s[Protein Name] AND %s[Organism]' | efetch -format fasta > %s_%s.fa" % (protein, taxonomy, protein, taxonomy))

if __name__ == '__main__':
    with open("%s_%s.fa" % (protein, taxonomy)) as my_file:
        species_list = []
        for file_line in my_file:
            if file_line.startswith(">"):
                organism = re.search(r"\[(.*)]", file_line).group(1)
                species_list.append(organism)

    with open("pyruvate_dehydrogenase_mammals.fa") as thefile:
        seq = {}
        seqlen = {}
        for eachline in thefile:
            if eachline.startswith(">"):
                protein = re.search(r"\[(.*)]", eachline).group(1)
                seq[protein] = ''
            else:
                seq[protein] += eachline.replace("\n", '').strip()
            seqlen[protein] = len(seq[protein])
            seq[protein] = seq[protein].split()










