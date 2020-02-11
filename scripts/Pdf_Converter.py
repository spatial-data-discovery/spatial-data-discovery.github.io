
"""
Author: Matthew Cusick

Date: 2/10/2020

Description: Converts file.docx to file.pdf

To Do: Make this a looping function for any number of conversions

Input: absolute file path of .docx file and absolute file path of desired .pdf file

Output: .pdf file

Example output file name: MattWorkNotes.pdf

Example input: python Pdf_Converter.py C:\\Users\\Name\\Dir\\FileName.docx C:\\Users\\Name\\Dir\\FileName.pdf (Using single backslashes)
"""
# Standard modules
import sys, os, time, argparse

# pip install pywin32; https://pypi.org/project/pywin32/
import win32com.client

def convertToPDF(in_file, out_file):

    # Microsoft formatting code. 17 means PDF. Can change this integer to change file conversion.
    # I.e. 8 for standard HTML format, or 12 for XML document format.
    wdFormatPDF = 17

    # Creates instance of word
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = True

    # To make SURE nothing goes wrong
    time.sleep(3)

    # Assigns word document to be converted
    doc = word.Documents.Open(in_file)

    # Converts to PDF
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()

    word.Visible = False
    word.Quit() 

if __name__ == "__main__":

    p = argparse.ArgumentParser(description='Converting docX to PDF')
    p.add_argument('input', help = "Absolute file path for existing .docx file")
    p.add_argument('output', help = "Absolute file path for desired .pdf file")
    args = p.parse_args()
    convertToPDF(args.input, args.output)