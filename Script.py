#!/usr/bin/python3
import os
import pandas as pd
import subprocess
import re
import time
import matplotlib.pyplot as plt

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
        elif check_continue(f"you have found {search_num} sequences, do you wanna continue?"):
            print("downloading...... in a second~")
            break
        else:
            print("Since you don't want to continue, you are going to exit in 3 seconds. See you next time~")
            time.sleep(3)
            exit()
    os.system(f"esearch -db protein -query '{protein_ask}[Protein Name] AND {taxonomy_ask}[Organism]' | efetch -format fasta > {protein_ask}_{taxonomy_ask}_ori.fa")
    return print(f"\n###{protein_ask}_{taxonomy_ask}_ori.fa### has been successfully downloaded to your current working directory")

def pullseq(protein_name, taxonomy_name, n = 150):
    os.system("cp /localdisk/data/BPSM/ICA2/pullseq .")
    os.system(f"./pullseq -i {protein_name}_{taxonomy_name}_ori.fa -m {n} > {protein_name}_{taxonomy_name}.fa")
    if n < 2:
        return print(f"\nIt seems that you don't want to make a screening to the sequences, the sequences are stored in file: ## {protein_name}_{taxonomy_name}.fa ## now")
    else:
        return print(f"\nThe sequences that shorter than {n} are thrown away from the original file, the rest of them are stored in file: ## {protein_name}_{taxonomy_name}.fa ## now")

# main processes of the program
if __name__ == '__main__':
    # get 2 inputs from identify function and store them in 2 variables
    # protein = "pyruvate_dehydrogenase"   taxonomy = "ascomycete_fungi" taxonomy = "mammals"
    protein, taxonomy = identify()
    #download the related file
    download_file(protein, taxonomy)

    if check_continue(f"\nSince there might be some sequences you find too short to be significant, would you like to screen them by a minimum sequence length?"):
        min_len = int(input("\tplease input the minimal length you want[default = 150]: "))
    else:
        min_len = 0
    pullseq(protein, taxonomy, min_len)


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
                    acc_num = ""
                else:
                    acc_num = acc_num.group(1)
                organism = re.search(r"\[(.*)]", file_line)
                if organism == None:
                    organism = ""
                else:
                    organism = organism.group(1)
                acc_nums.append(acc_num)
                species.append(organism)
            else:
                current_seq += file_line.strip()
        seqs.append(current_seq)

    #get the unduplicated species list, and the number of them, then show them to the user
    seqlen = []
    i = 0
    for seq in seqs:
        seqlen.append(len(seq))
    species_unrep_num = len(set(species))
    species_unrep = list(set(species))
    if check_continue(f"\n...\n...\nThere are {species_unrep_num} unduplicated species in the file you just downloaded, which are stored in a list, do you want to check them?"):
        for spe in sorted(species_unrep):
            print(spe)
    
    #put all the data into a dictionary
    all_data = {"Accession Number": acc_nums, "organisms" : species, "length of sequences" : seqlen, "Sequences" : seqs}
    df_all_data = pd.DataFrame(all_data)
    if check_continue("\n...\n...\n...\nAll the data has been organized in a form now, containing the accession numbers, species names, sequence length and the sequence, do you wanna generate a tsv file?"):
        if check_continue("\ndo you want to sort by the species?"):
            df_all_data.sort_values('organisms', ascending = True, inplace = True)
            df_all_data.to_csv("all_data_you_searched.tsv", sep = '\t', header = True)
            print("\ntsv file named 'all_data_you_searched.tsv' has been generated in the current working dictionary")


    # 1, use pullseq to discard the sequences that are too short(150 maybe)
    # 2, maybe find another way for further sequences screening
    # 3, output the similarity plot and the distance matrix
    # 4, write a loop to get motifs of each sequence
    # 5, 


    if check_continue("with all the data prepared, do you want to make a multiple sequences alignment and following analysis? (no for quit)"):
        print("\n\tprocessing...please wait...")
        # use clustalo to do MSA
        os.system(f"clustalo -i {protein}_{taxonomy}.fa -o {protein}_{taxonomy}_aligned.fa")
        print(f"\nA MSA alignment file named {protein}_{taxonomy}_aligned.fa has been generated to the current working dictionary\n\n")
        # get an input to ask the winsize user want
        winsize = int(input("please designate a winsize[integer, default = 4] for similarity plot generation(The larger this value is, the smoother the plot will be): "))
        os.system(f"plotcon {protein}_{taxonomy}_aligned.fa -winsize {round(winsize)} -graph png")
        print("\nSimilarity plot for aligned sequences has been generaged to your current directory\n")
        # ask the user if they want take a look at the plot
        if check_continue("do you want to view the plot?"):
            # show the image to the user with matplotlib.pyplot
            print("please wait, processing...")
            image = plt.imread("plotcon.1.png")
            plt.imshow(image)
            plt.show()
        # generate distance matrix or not?
        if check_continue("I can also generate a distance matrix between each 2 sequences, do you want it?"):
            method = input("please select the correction methods for proteins you want[0:(Uncorrected); 1:(Jukes-Cantor); 2:(Kimura Protein)]: \n\t")
            os.system(f"distmat {protein}_{taxonomy}_aligned.fa -protmethod {method} {protein}_{taxonomy}.distmat")
        #scan the protein of motifs
        try: 
            os.mkdir(f"{protein}_{taxonomy}_scaned_motif_files")   # make a new directory to store motif files
        except FileExistsError:
            print(f"folder {protein}_{taxonomy}_scaned_motif_files is already exist")
        except:
            pass
        os.chdir(f"{protein}_{taxonomy}_scaned_motif_files")   # change to the dir
        os.system("touch scan_motif.tem")   # make a new file to stroe temporary data
        for acc_num, organism, seq in zip(acc_nums, species, seqs):
            with open("scan_motif.tem", 'w') as current_seq_file:
                current_seq_file.write(">" + acc_num + " ")
                current_seq_file.write(organism + "\n")
                current_seq_file.write(seq + "\n")
            os.system(f"patmatmotifs scan_motif.tem {acc_num}.patmatmotifs")  # store the information to each file
            os.system(f"touch {acc_num}_info.motif")  # make a new file to store motif sequences for current sequence 
            with open(f"{acc_num}_info.motif", 'a') as motif_file:  # loop to find each motif indexes
                with open(f"{acc_num}.patmatmotifs", 'r') as motif_file_ori:
                    for each_line in motif_file_ori:
                        if each_line.startswith("S"):
                            motif_start_search = re.search("[\d]+", each_line)
                            if motif_start_search == None:
                                continue
                            else:
                                motif_start = int(motif_start_search.group(0))
                        if each_line.startswith("E"):
                            motif_end_search = re.search("[\d]+", each_line)
                            if motif_end_search == None:
                                continue
                            else:
                                motif_end = int(motif_end_search.group(0))
                            motif_file.write("Motif sequence:\n\n")
                            motif_file.write(f"{seq[motif_start-1:motif_end-1]}\n\n\n")
            print(f"Motif sequences of protein {acc_num} has been saved in file {acc_num}_info.motif")
        os.system("rm scan_motif.tem")
        os.chdir("..")

    if check_continue("Do you want to check the secondary structure of all the sequences:"):
        os.system(f"garnier {protein}_{taxonomy}.fa secondary_structure.garnier")
        print("a secondary structure information file has been generated in the current directory\n\n")

    print("Thank you for using my script! byebye! :-)")










