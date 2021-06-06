#------------------------------------------------------------------------------------
# XML Generator for praat users working on the Pangloss collection
# https://pangloss.cnrs.fr/
# This Python script READS INFORMATION FROM 
# (i) AN EXCEL SPREADSHEET (CONVERTED TO CSV FILE)
# (ii) A PRAAT TEXT GRID (itemized)
# AND WRITES THE OUTPUT TO AN XML FILE
# September 2020
#-----------------------------------------------------------------------------------

# Written by Maxime FILY, UGA
# NOANOA Project 2020

# Instruction
# 1- before launching, please make sure that your input is in one directory only
# 2- Enter the work directory (where the inputs are)
# 3- Enter the .TextGrid name WITHOUT the extension for variables consistency
# 4- The programm assumes that textgrid and audio files bear the same name. If not, you have to change the file name in the output HEADER

# 5- the linguistic input originate from 2 files with the SAME name :
#     - my_file.txt (translations, gloses, etc.)
#     - my_file.TextGrid ; see below
#               * the Textgrid file requires two tiers (numitem and comment),
#               but it can accept other tiers, although they will simply be ignored
#               * numitem formats are imposed : start with d (decimal), plus (optionally) "_" followed 
#               with any number of ASCII characters
# 6- the xml in the output does not contain any markup as to which viewing option is assumed because it depends on the formalism of the destination website
# and should therefore be added by the Pangloss team (the two first lines of an xml, usually).


import sys
import textgrids
import os, time
import os.path
import codecs
import io
import struct
from collections import OrderedDict, namedtuple
import csv
import glob
import re

#initialisations, ecriture meta
print("enter the work directory (where your textgrid is located)")
dirNAME = input()
print("this is your work directory : " + dirNAME)
print("enter the name of your textgrid (without extension)")
textGRD = input()
print("this is your textgrid : " + textGRD)
print("enter the name of your project (template : crdo-NRU_recording_identifier)")
ident = input()
print("this is your project : " + ident)
print("enter the language code (in glottolog)")
lngG = input()
print("enter the language name (e.g. Yongning Na)")
lngN = input()
print("language selected : " + lngN + ", glottolog id = " + lngG)
print("enter recording description (english)")
eng_desc = input()
print("recording description: " + eng_desc)
print("saisir la description de l'enregistrement (optionnel):")
fra_desc = input()
print("description de l'enregistrement : " + fra_desc)
print("请您输入记录品简介(自选):")
cmn_desc = input()
print("记录品简介 : " + cmn_desc)
print("enter the name of the editor : ")
editor = input()
print("enter the name of the depositor : ")
depositor = input()
print("enter the name of the researcher : ")
researcher = input()
print("enter the name of the interviewer : ")
interviewer = input()
print("enter the name of the speaker : ")
speaker = input()
print("enter the place of recording (in English) : ")
locEN = input()
print("enter the place of recording (official postal address) : ")
locOA = input()
print("enter the GPS coordinates of the place of recording : ")
locGPS = input()
print("enter the date of recording : ")
dateREC = input()
print("enter the format of recording (wav or mp3) : ")
formT = input()
print("enter the type of data treated (Sound, EGG, sound + EGG, etc.)  : ")
typeT = input()
print("enter the type of license via asociated URL (e.g. cc-by-nc) : ")
URLL = input()
print("enter the license's access rights (free, unmodified, quote) : ")
typeL = input()
print("thank you")
time.sleep(1)
print("For information, we will be working with " + textGRD + ".wav")
time.sleep(1)

#input
grd = textGRD + '.TextGrid'
fileNAME = textGRD + '.txt'
os.chdir(dirNAME)


#output
fcsv = textGRD + "_tsp.csv"
outNAME = textGRD + '.xml'
metaNAME = textGRD + "_metadata.txt"
print("the data generated through standard input are recorded in " + metaNAME )


#ménage
if os.path.exists(dirNAME + "/" + fcsv):
    os.remove(dirNAME + "/" + fcsv)
if os.path.exists(dirNAME + "/" + outNAME):
    os.remove(dirNAME + "/" + outNAME)
if os.path.exists(dirNAME + "/" + metaNAME):
    os.remove(dirNAME + "/" + metaNAME)


#metadata
meta = codecs.open(metaNAME,'w',encoding='UTF-8')
meta.write("recording ID: " + ident + "\n")
meta.write("description (EN): " + eng_desc + "\n")
meta.write("description (FR): " + fra_desc + "\n")
meta.write("description (ZH): " + cmn_desc + "\n")
meta.write("Textgrid Name: " + grd + '\n')
meta.write("Editor: " + editor + "\n")
meta.write("Depositor: " + depositor + "\n")
meta.write("Researcher: " + researcher + "\n")
meta.write("Interviewer: " + interviewer + "\n")
meta.write("speaker (contributor): " + speaker   + "\n")      
meta.write("Location (EN): " + locEN + "\n")
meta.write("Location (ZH): " + locOA + "\n")
meta.write("Location (GPS): " + locGPS + "\n")
meta.write("Date of the recording: " + dateREC + "\n")
meta.write("Format : " + formT + "\n")
meta.write("Type of data: " + typeT + "\n")
meta.write("copyright type: " + URLL + "\n")
meta.write("access rights: " + typeL + "\n")
meta.write("object: " + lngN + "\n")
meta.write("glottolog ID: " + lngG + "\n")
meta.write("WAV ID: " + textGRD + ".wav\n")
meta.close()

#Donnees generales
out = codecs.open(outNAME,'w',encoding='UTF-8')
out.write('<WORDLIST id="')
out.write(ident)
out.write('" xml:lang="')
out.write(lngG)
out.write('">\n')
out.write('\t<HEADER>\n')
out.write('\t\t<TITLE xml:lang="eng">')
out.write(eng_desc)
out.write('</TITLE>\n')
out.write('\t\t<SOUNDFILE href="')
out.write(textGRD)
out.write('" />\n')
out.write('\t</HEADER>\n')


#Donnees linguistiques balisees
grid = textgrids.TextGrid(grd)
grid.tier_to_csv('numitem', fcsv)

# fichier temporel (timesteps)
fich_exploit = open(fcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_lue = list(fich_lu)
fich_exploit.close()

# tableau avec infos complètes
tab_exploit = open(fileNAME, encoding="utf8")
tab_lu = csv.reader(tab_exploit, delimiter = '\t')
tabLIST = list(tab_lu)
tab_exploit.close()
#print(str(tabLIST[:][0]) + "!" + str(len(tabLIST[:][0])) + "!" + str(tabLIST[0][0]))
for j in range(len(tabLIST[:][0])):
    if tabLIST[0][j] == "numitem":
        ind_item = j
    if tabLIST[0][j] == "FR":
        ind_FR = j
    if tabLIST[0][j] == "EN":
        ind_EN = j
    if tabLIST[0][j] == "CH":
        ind_CH = j
    if tabLIST[0][j] == "Phonol":
        ind_NAC = j
    if tabLIST[0][j] == "Fcit":
        ind_NAF = j
    if tabLIST[0][j] == "OTHER_Phonol":
        ind_OTC = j
    if tabLIST[0][j] == "OTHER_Fcit":
        ind_OTF = j
    if tabLIST[0][j] == "Renvois":
        ind_renvois = j
    if tabLIST[0][j] == "Commentaire":
        ind_comm = j

for i in range(1,len(tabLIST)):
    try:
        numitem = int(tabLIST[i][ind_item])
    except (NameError, IndexError) as e:
        pass
    try:
        FRtrad = tabLIST[i][ind_FR]
    except (NameError, IndexError) as e:
        pass
    try:
        ENtrad = tabLIST[i][ind_EN]
    except (NameError, IndexError) as e:
        pass
    try:
        CHtrad = tabLIST[i][ind_CH]
    except (NameError, IndexError) as e:
        pass
    try:
        NAFword = tabLIST[i][ind_NAF]
    except (NameError, IndexError) as e:
        pass
    try:
        OTCword = tabLIST[i][ind_OTC]
    except (NameError, IndexError) as e:
        pass
    try:
        OTFword = tabLIST[i][ind_OTF]
    except (NameError, IndexError) as e:
        pass
    try:
        renvoi = tabLIST[i][ind_renvois]
    except (NameError, IndexError) as e:
        pass
    try:
        comm = tabLIST[i][ind_comm]
    except (NameError, IndexError) as e:
        pass
    for k in range(len(liste_lue)):
        try:
            indice_textgrid = int(liste_lue[k][0].split("_")[0])
        except ValueError:
            indice_textgrid = 0
        if (indice_textgrid - numitem) == 0:
            out.write('\t\t<W id="item#')
            out.write(str(liste_lue[k][0])) 
            out.write('">\n')
            out.write('\t\t\t<AUDIO start="')
            out.write(str(liste_lue[k][1]))
            out.write('" end="')
            out.write(str(liste_lue[k][2]))
            out.write('" />\n')
            out.write("\t\t\t<FORM kindOf='phono'>")
            try:
                out.write(str(NAFword))
            except:
                pass
            out.write('</FORM>\n')
            out.write('\t\t\t<NOTE xml:lang="Fcit" message="')
            try:
                out.write(str(NACword))
            except:
                pass
            out.write('"/>\n')
            out.write('\t\t\t<TRANSL xml:lang="fr">')
            try:
                out.write(str(FRtrad))
            except:
                pass
            out.write('</TRANSL>\n')
            out.write('\t\t\t<TRANSL xml:lang="zh">')
            try:
                out.write(str(CHtrad))
            except:
                pass
            out.write('</TRANSL>\n')
            out.write('\t\t\t<TRANSL xml:lang="en">')
            try:
                out.write(str(ENtrad))
            except:
                pass
            out.write('</TRANSL>\n')
            out.write('\t\t\t<NOTE xml:lang="Fcit" message="')
            try:
                out.write(str(comm))
            except:
                pass
            out.write('"/>\n')
            out.write('\t\t</W>\n')
out.write('</WORDLIST>\n')
out.close()
