#!/usr/bin/python3
import os
import pandas as pd
import subprocess
import re

# let use input the protein name and taxonomy group name that they want to use
def identify():
    while True:
        protein_in = "_".join(input("please input your protein name\n\t").split())
        taxonomy_in = "_".join(input("please input the taxonomic group you want to analyse\n\t").split())
        if protein_in == "" or taxonomy_in == "":
            print("\n\nYou missed at least one input, I CAN'T create something out of nothing ,sorry! Please try again!!!\n\n")
            continue
        else:
            break
    return taxonomy_in, protein_in

# prepare a check function to see if the user want to continue or not
def check_continue(information):
    user_info = input(information + " [yes/no]\n\t")
    if user_info.upper().startswith("Y"):
        return True
    else:
        return False

# function that download the .fa files from database with os.system()
def download_file(protein_ask = "pyruvate_dehydrogenase", taxonomy_ask = "ascomycete_fungi"):
    os.system(f"esearch -db protein -query '{protein_ask}[Protein Name] AND {taxonomy_ask}[Organism]' \
    | efetch -format fasta > {protein_ask}_{taxonomy_ask}.fa")
    return print(f"\t###{protein_ask}_{taxonomy_ask}.fa### has been successfully downloaded to current working directory")

 # find the number of protein sequences that esearch found in advance and tell the user
result_bin = subprocess.check_output(f"esearch -db protein -query '{protein_ask}[Protein Name] AND {taxonomy_ask}[Organism]'", shell = True)
result_readable = result_bin.decode("utf-8")
re.findall(r"<Count>(.*?)</Count>", result_readable)

# main process of the program
if __name__ == '__main__':
    # get 2 inputs from identify function and store them in 2 variables
    # protein = "pyruvate_dehydrogenase"   taxonomy = "ascomycete_fungi" taxonomy = "mammals"
    protein, taxonomy = identify()

    if protein == "" or taxonomy == "":
        protein = "pyruvate_dehydrogenase"
        taxonomy = "ascomycete_fungi"
#         print("you have input nothing, while I can't create something out of nothing, here is an example with \
# protein is \"pyruvate dehydrogenase\" and taxonomy is \"ascomycete fungi\"")

    # download_file(protein, taxonomy)


    # open the file that just been downloaded, generate a list of species names , list of each seq, and the length of each of them
    with open(f"{protein}_{taxonomy}.fa") as my_file:
        species = []
        acc_nums = []
        seqs = []
        current_seq = ""
        for file_line in my_file:
            if file_line.startswith(">"):
                if current_seq != "":
                    seqs.append(current_seq)
                current_seq = ""
                acc_num = re.search(r">([^\s]*)", file_line).group(1)
                organism = re.search(r"\[(.*)]", file_line).group(1)
                acc_nums.append(acc_num)
                species.append(organism)
            elif current_seq == "":
                current_seq = file_line.strip()
            else:
                current_seq += file_line.strip()
        seqs.append(current_seq)

    seqlen = []
    i = 0
    for seq in seqs:
        seqlen.append(len(seq))
    species_unrep_num = len(set(species))
    species_unrep = list(set(species))


    # 1.check if the organism and protein names are correct(tell the user that the result of search)

    # 2, pullseq
    # 3,


    all_data = {"Accession Number": acc_nums, "organisms" : species, "Sequences" : seqs, "length of sequences" : seqlen}

    answer = check_continue(f"there are {species_unrep_num} species in total, "
                   f"which are list below:\n\t{species_unrep}\n\ndo you want to continue")


    os.system(f"clustalo -i {protein}_{taxonomy}.fa -o {protein}_{taxonomy}_aligned.fa --distmat-out=distance_matrix.mat --full")

    # get an input to ask the winsize user want
    os.system(f"plotcon {protein}_{taxonomy}_aligned.fa -winsize {winsize} -graph pdf")
    print("")

    os.system(f"patmatmotifs ")
    


    # with open("%s_%s.fa" % (protein, taxonomy)) as thefile:
    #     seq = {}
    #     seqlen = {}
    #     for eachline in thefile:
    #         if eachline.startswith(">"):
    #             protein = re.search(r"\[(.*)]", eachline).group(1)
    #             seq[protein] = ''
    #         else:
    #             seq[protein] += eachline.replace("\n", '').strip()
    #         seqlen[protein] = len(seq[protein])
    #         seq[protein] = seq[protein].split()


with open(f"{protein}_{taxonomy}.fa") as my_file:
    species = []
    acc_nums = []
    seqs = []
    current_seq = ""
    for file_line in my_file:
        if file_line.startswith(">"):
            if current_seq != "":
                seqs.append(current_seq)
            current_seq = ""
            acc_num = re.search(r">([^\s]*)", file_line).group(1)
            organism = re.search(r"\[(.*)]", file_line).group(1)
            acc_nums.append(acc_num)
            species.append(organism)
        elif current_seq == "":
            current_seq = file_line.strip()
        else:
            current_seq += file_line.strip()
    seqs.append(current_seq)








