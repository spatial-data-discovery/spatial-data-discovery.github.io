#dna_translator.py
#
#Author: Emma Strickland
#
#Last Edit: 2020-02-10
#
#This script takes a non-template DNA sequence as an input and returns a list of the RNA codons and protein sequence that will result from transcription and translation
import argparse

#Dictionary to match codon sequences to the protein they encode for
protein_based_on_codon = {"UUU":"Phenylalanine", "UUC":"Phenylalanine", "UUA":"Leucine", "UUG":"Leucine",
                          "UCU":"Serine", "UCC":"Serine", "UCA":"Serine", "UCG":"Serine",
                          "UAU":"Tyrosine", "UAC":"Tyrosine", "UAA":"STOP", "UAG":"STOP",
                          "UGU":"Cysteine", "UGC":"Cysteine", "UGA":"STOP", "UGG":"Tryptophan",
                          "CUU":"Leucine", "CUC":"Leucine", "CUA":"Leucine", "CUG":"Leucine",
                          "CCU":"Proline", "CCC":"Proline", "CCA":"Proline", "CCG":"Proline",
                          "CAU":"Histidine", "CAC":"Histidine", "CAA":"Glutamine", "CAG":"Glutamine",
                          "CGU":"Arginine", "CGC":"Arginine", "CGA":"Arginine", "CGG":"Arginine",
                          "AUU":"Isoleucine", "AUC":"Isoleucine", "AUA":"Isoleucine", "AUG":"Methionine",
                          "ACU":"Threonine", "ACC":"Threonine", "ACA":"Threonine", "ACG":"Threonine",
                          "AAU":"Asparagine", "AAC":"Asparagine", "AAA":"Lysine", "AAG":"Lysine",
                          "AGU":"Serine", "AGC":"Serine", "AGA":"Arginine", "AGG":"Arginine",
                          "GUU":"Valine", "GUC":"Valine", "GUA":"Valine", "GUG":"Valine",
                          "GCU":"Alanine", "GCC":"Alanine", "GCA":"Alanine", "GCG":"Alanine",
                          "GAU":"Aspartic acid", "GAC":"Aspartic acid", "GAA":"Glutamic acid", "GAG":"Glutamic acid",
                          "GGU":"Glycine", "GGC":"Glycine", "GGA":"Glycine", "GGG":"Glycine"}

#Function that converts DNA sequence to RNA and protein sequence
def translate_dna(dna):
    dna = dna.upper()
    #Replacing base pairs with complement base pair
    template_strand = ""
    for letter in dna:
        if letter == "A":
            template_strand += "U" #RNA has U instead of T
        elif letter == "T":
            template_strand += "A"
        elif letter == "G":
            template_strand += "C"
        elif letter == "C":
            template_strand += "G"
    template_strand = template_strand[::-1 ] #Reverses DNA sequence to give you the template strand which RNA transcription is based on
    if len(template_strand) % 3 != 0: #Strand must be divisible by 3 to group into codons
        template_strand = template_strand[:-1]
        if len(template_strand) % 3 != 0:
            template_strand = template_strand[:-1]
    codons = [template_strand[i:i+3] for i in range(0,len(template_strand),3)] #RNA codons are groups of 3 base pairs
    proteins = [protein_based_on_codon[codons[i]] for i in range(0,len(codons))] #Use dictionary to convert condons to protein name
    for w in range(0, len(proteins)):
        if proteins[w] == 'STOP': #Identifying stop codons
            return codons[:w+1], proteins[:w+1]
    return codons, proteins

#MAIN
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes a DNA sequence and returns the RNA codons")
    parser.add_argument('input', type = str, help = "Input DNA sequence as a string")
    args = parser.parse_args()
    print(translate_dna(args.input))
