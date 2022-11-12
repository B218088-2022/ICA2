#!/usr/bin/python3
import os
import pandas as pd
import subprocess

def input():
    protein = input("please input your protein")
    taxonomy = input("please input your protein")

    return protein, taxonomy

os.system("esearch -db protein -query '%s[Protein Name] AND %s[Organism]' | efetch -format fasta > %s_%s.fa" % (protein, taxonmy, protein, taxonmy))


