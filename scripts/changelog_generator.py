from datetime import date
import subprocess, sys
import argparse
import os
import re

#Stackoverflow code to change from utf16 to utf8. WMIC generates utf16 for installed programs list,
#which doesnt work for what I'm trying to do.
def correctSubtitleEncoding(filename, newFilename, encoding_from='UTF-16', encoding_to='UTF-8'):
    with open(filename, 'r', encoding=encoding_from) as fr:
        with open(newFilename, 'w', encoding=encoding_to) as fw:
            for line in fr:
                fw.write(line[:-1]+'\r')

def updateOld(old, oldLines, new, newLines):
    #close and reopen in write mode to replace file contents.
    old.close()
    old = open("oldchangelog.txt", "w")
    for i in range(len(newLines)):
        old.write(newLines[i])


#Begin Program by parsing args. Should only be help.
cmdarg = argparse.ArgumentParser(description = "Updates Changelog. You will need powershell execution permissions.")
args = cmdarg.parse_args()

#get the local directory for use in this program.
dir_path = os.getcwd()
dir_path += r"\p.ps1"
dir_path = repr(dir_path)

#For log
pslogPath = os.getcwd()
pslogPath += r"\PSlog.txt"
pslogPath = repr(pslogPath)

#create a powershell script in the current directory
powershellScript = open("p.ps1", "w")
#populate that file with the command to get the list of programs
powershellScript.write("Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion | Format-Table -AutoSize > " + pslogPath)
#finished with the file, and we can't keep it open now or it will be in use when we try to execute it.
powershellScript.close()

#Get path to the above script
psScriptpath = os.getcwd()
psScriptpath += r'\p.ps1'

#First generate a new up to date list of programs.
#"C:\\Users\\elkel\\Desktop\\UtilScript\\p.ps1"
p = subprocess.Popen(["powershell.exe",
              psScriptpath],
              stdout=sys.stdout)
p.communicate()



#Since we should be running this after the installed programs list generator,
#and that should generate a file with the date, this will access that file.
#Then the others are easy enough to get.
try:
    old = open("oldchangelog.txt", "r+")
except:
    old = open("oldchangelog.txt", "w")
    old.close()
    old = open("oldchangelog.txt", "r+")

correctSubtitleEncoding("PSlog.txt", "new.txt")
new = open("new.txt", "r+")

try:
    log = open("changelog.txt", "a")
except:
    log = open("changelog.txt", "w")
    log.close()
    log = open("changelog.txt", "a")
    
#Get the list of lines for comparison
oldLines = old.readlines()
newLines = new.readlines()

#For first time runs, we should fill the changelog with all of the contents from the newLines list.
if len(oldLines) == 0:
    log.write("Begin Tracking " + str(date.today()))
    for i in range(len(newLines)):
        log.write(newLines[i])
    updateOld(old, oldLines, new, newLines)
    exit()


#The magic area. Goes through and checks every line, stripping all space characters and comparing them.
#If spaces are not removed, the comparison fails.

log.write("\n\nUPDATES AS OF " + str(date.today()) + ":")

anyChanges = False

for i in range(len(newLines)):
    if newLines[i].replace(' ', '') != oldLines[i].replace(' ', ''):
        anyChanges = True
        #Check to see if this is an entirely new program or just an updated version of an old one.
        #If it is new, put it in the changelog as such and skip to the next line
        for j in range(3):
            if newLines[i][j] != oldLines[i][j]:
                print("Here I am")
                log.write("\nNEW PROGRAM: " + newLines[i])
                del(newLines[i])
                break


        print("NOT SAME, updating")
        print(newLines[i])
        print(oldLines[i])
        #write to changelog
        log.write("\n" + newLines[i])
        #Change the line that represents an update
        oldLines[i] = newLines[i]

if anyChanges == False:
    log.write("\n No Changes")

updateOld(old, oldLines, new, newLines)
