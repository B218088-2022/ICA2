#!/usr/bin/python3
import os
import pandas as pd
import subprocess
import re
import time

# let user input the protein name and taxonomy group name that they want to use, test if user has input nothing or not, if there is nothing input, notify the user.
def identify():
    while True:
        protein_in = "_".join(input("please input your protein name\n\t").split())
        taxonomy_in = "_".join(input("please input the taxonomic group you want to analyse\n\t").split())
        if protein_in == "" or taxonomy_in == "":
            print("\n\nYou missed at least one input, I CAN'T create something out of nothing ,sorry! Please try again!!!\n\n")
            continue
        else:
            return protein_in, taxonomy_in
    
# prepare a check function to see if the user want to continue or not, if user didn't input something right, notify user 
def check_continue(information = "do you want to continue? \n\t"):
    while True:
        user_info = input(information + " [yes/no]\n\t")
        if user_info.upper().startswith("Y"):
            return True
        elif user_info.upper().startswith("N"):
            return False
        else: 
            print("\n\tyou didn't input correctly, please input 'yes' or 'no'! \t")

# function that download the .fa files from database with os.system()
def download_file(protein_ask = "pyruvate_dehydrogenase", taxonomy_ask = "ascomycete_fungi"):
    while True:
        result_readable = subprocess.check_output(f"esearch -db protein -query '{protein_ask}[Protein Name] AND {taxonomy_ask}[Organism]'", shell = True).decode("utf-8")
        search_num = re.search(r"<Count>(.*?)</Count>", result_readable).group(1)
        if int(search_num) >= 1000:
            print("\nSorry but there are too many sequences found based on your search criteria, which is hard to process, could you please try again?\n")
            protein_ask, taxonomy_ask = identify()
            continue
        elif answer = check_continue(f"you have found {search_num} sequences, do you wanna continue?"):
            print("downloading...... in a second~")
            break
        else:
            print("Since you don't want to continue, you are going to exit in 3 seconds. See you next time~")
            time.sleep(3)
            exit()
    os.system(f"esearch -db protein -query '{protein_ask}[Protein Name] AND {taxonomy_ask}[Organism]' | efetch -format fasta > {protein_ask}_{taxonomy_ask}.fa")
    return print(f"\n###{protein_ask}_{taxonomy_ask}.fa### has been successfully downloaded to your current working directory")

def pullseq(filename, n = 150):
    os.system(f"./pullseq -i {filename} -m {n}")


# main processes of the program
if __name__ == '__main__':
    # get 2 inputs from identify function and store them in 2 variables
    # protein = "pyruvate_dehydrogenase"   taxonomy = "ascomycete_fungi" taxonomy = "mammals"
    protein, taxonomy = identify()
    #download the related file
    download_file(protein, taxonomy)



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
                acc_num = re.search(r">([^\s]*)", file_line)
                if acc_num == None:
                    acc_num = "-"
                else:
                    acc_num = acc_num.group(1)
                organism = re.search(r"\[(.*)]", file_line)
                if organism == None:
                    organism = "-"
                else:
                    organism = organism.group(1)
                # 如果没有搜索到相应的内容，进行置空处理(分两步处理，先搜索，判断是否为none，不是none再group，是的话置为'-')
                acc_nums.append(acc_num)
                species.append(organism)
            else:
                current_seq += file_line.strip()
        seqs.append(current_seq)

    seqlen = []
    i = 0
    for seq in seqs:
        seqlen.append(len(seq))
    species_unrep_num = len(set(species))
    species_unrep = list(set(species))
    if not check_continue(f"there are {species_unrep_num} species in total, which are list below:\n\t{sorted(species_unrep)}\n\ndo you want to continue"):
        print("Since you don't want to continue, you are going to exit in 3 seconds. See you next time~")
        time.sleep(3)
        exit()
    
    #put all the data into a dictionary
    all_data = {"Accession Number": acc_nums, "organisms" : species, "length of sequences" : seqlen, "Sequences" : seqs}
    df_all_data = pd.DataFrame(all_data, na_values = ['-'])
    if check_continue("\n...\n...\n...\nAll the data has been organized in a form, do you wanna generate a tsv file?"):
        df_all_data.to_csv("all_data_you_searched.tsv", sep = '\t', header = True)
        print("\ntsv file named 'all_data_you_searched.tsv' has been generated in the current working dictionary")
    

    # 2, pullseq
    # 3,

    os.system(f"clustalo -i {protein}_{taxonomy}.fa -o {protein}_{taxonomy}_aligned.fa --distmat-out={protein}_{taxonomy}_distmat.mat --full")

    # get an input to ask the winsize user want
    os.system(f"plotcon {protein}_{taxonomy}_aligned.fa -winsize {winsize} -graph pdf")
    print("")




    os.system(f"patmatmotifs {protein}_{taxonomy_single.fa} {current_acc_num}.patmatmotifs -full")

    
    










