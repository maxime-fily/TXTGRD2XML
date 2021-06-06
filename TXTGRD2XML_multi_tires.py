#------------------------------------------------------------------------------------
# XML Generator for praat users working on the Pangloss collection
# https://pangloss.cnrs.fr/
# This Python script READS INFORMATION FROM 
# (i) AN EXCEL SPREADSHEET (CONVERTED TO CSV FILE)
# (ii) A PRAAT TEXT GRID (itemized)
# AND WRITES THE OUTPUT TO AN XML FILE
# September 2020
#-----------------------------------------------------------------------------------

# Written by Maxime FILY, Université Grenoble Alpes
# Project : Pangloss
#

# Instruction
# 1- before launching, please make sure that your input is in one directory only
# 2- Enter the work directory (where the inputs are)
# 3- Enter the .TextGrid name WITHOUT the extension for variables consistency
# 3- The programm assumes that textgrid and audio files bear the same name. If not, you have to change the file name in the output HEADER
# 4- the linguistic input originate from one file : the .TextGrid ;
#           * the .Textgrid file requires 3 tiers (numitem, surface phonol, gloss),
#           but it can accept other tiers, such as phonetic, ENGLISH, FRENCH, CHINESE, tone pattern
#           * numitem formats are imposed : start with d (decimal), plus (optionally) "_" followed 
#           with any number of ASCII characters
# 5- the xml in the output does not contain any markup as to which viewing option is assumed because it depends on the formalism of the destination website
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
os.chdir(dirNAME)


#output
fcsv = textGRD + "_numitem.csv"
g0csv = textGRD + "_Nafon.csv"
g1csv = textGRD + "_Napho.csv"
g2csv = textGRD + "_Naton.csv"
g3csv = textGRD + "_gloss.csv"
hcsv = textGRD + "_CH.csv"
icsv = textGRD + "_EN.csv"
jcsv = textGRD + "_FR.csv"
kcsv = textGRD + "_comm.csv"
outNAME = textGRD + '.xml'
metaNAME = textGRD + "_metadata.txt"
print("the data generated through standard input are recorded in " + metaNAME )

#ménage
if os.path.exists(dirNAME + "/" + fcsv):
    os.remove(dirNAME + "/" + fcsv)
if os.path.exists(dirNAME + "/" + g0csv):
    os.remove(dirNAME + "/" + g0csv)
if os.path.exists(dirNAME + "/" + g1csv):
    os.remove(dirNAME + "/" + g1csv)
if os.path.exists(dirNAME + "/" + g2csv):
    os.remove(dirNAME + "/" + g2csv)
if os.path.exists(dirNAME + "/" + g3csv):
    os.remove(dirNAME + "/" + g3csv)
if os.path.exists(dirNAME + "/" + hcsv):
    os.remove(dirNAME + "/" + hcsv)
if os.path.exists(dirNAME + "/" + icsv):
    os.remove(dirNAME + "/" + icsv)
if os.path.exists(dirNAME + "/" + jcsv):
    os.remove(dirNAME + "/" + jcsv)
if os.path.exists(dirNAME + "/" + kcsv):
    os.remove(dirNAME + "/" + kcsv)    
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


#ouverture fichier de travail
out = codecs.open(outNAME,'w',encoding='UTF-8')

#Donnees generales
out.write('<TEXT id="')
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


#Tier identification for the program. The markers for tier_name are hardcoded on this version
#For customization, the user may change the tier names below to match his/her TextGrid_file
#USER MODIFICATION START
###################################################################################################
grid = textgrids.TextGrid(grd)
grid.tier_to_csv('numitem', fcsv)
try:
    grid.tier_to_csv('phonetic', g0csv)
except: 
    pass
grid.tier_to_csv('surface phonol', g1csv)
try:
    grid.tier_to_csv('tone pattern', g2csv)
except: 
    pass
grid.tier_to_csv('gloss', g3csv)
try:
    grid.tier_to_csv('CHINESE', hcsv)   #Or any language used for tier name
except: 
    pass
try:
    grid.tier_to_csv('ENGLISH', icsv)   #Or any language used for tier name
except: 
    pass
try:
    grid.tier_to_csv('FRENCH', jcsv)    #Or any language used for tier name
except: 
    pass
try:
    grid.tier_to_csv('comment', kcsv)   #I almost made this tier obligatory but changed my mind.
except: 
    pass
#USER MODISFICATION FINISH

fich_exploit = open(fcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_numitem = list(fich_lu)
fich_exploit.close()
fich_exploit = open(g0csv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_Na0 = list(fich_lu)
fich_exploit.close()
fich_exploit = open(g1csv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_Na1 = list(fich_lu)
fich_exploit.close()
fich_exploit = open(g2csv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_Na2 = list(fich_lu)
fich_exploit.close()
fich_exploit = open(g3csv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_Na3 = list(fich_lu)
fich_exploit.close()
fich_exploit = open(hcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_CH = list(fich_lu)
fich_exploit.close()
fich_exploit = open(icsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_EN = list(fich_lu)
fich_exploit.close()
fich_exploit = open(jcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_FR = list(fich_lu)
fich_exploit.close()
fich_exploit = open(kcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_Comm = list(fich_lu)
fich_exploit.close()


if (((len(liste_Na0) - len(liste_numitem)) == 0) or ((len(liste_Na0) == 0))) and ((len(liste_Na1) - len(liste_numitem)) == 0) and ((len(liste_Na2) - len(liste_numitem)) == 0) and ((len(liste_Na3) - len(liste_numitem)) == 0) and ((len(liste_CH) - len(liste_numitem)) == 0) and ((len(liste_EN) - len(liste_numitem)) == 0) and ((len(liste_FR) - len(liste_numitem)) == 0) and ((len(liste_Comm) - len(liste_numitem)) == 0) :

    for k in range(len(liste_numitem)):
        try:
            indice_textgrid = int(liste_numitem[k][0].split("_")[0])
        except ValueError:
            indice_textgrid = 0
        if indice_textgrid != 0:
            out.write('\t<S id="S')
            out.write(str(liste_numitem[k][0]))
            out.write('">\n')
#required tiers
            out.write('\t\t<NOTE xml:lang="en" message="UID = ')
            out.write(str(liste_numitem[k][0]))
            out.write('"/>\n')
            out.write('\t\t<AUDIO start="')
            out.write(str(liste_numitem[k][1]))
            out.write('" end="')
            out.write(str(liste_numitem[k][2]))
            out.write('" />\n')
            out.write('\t\t<FORM kindOf="phono">')
            out.write(str(liste_Na1[k][0]))
            out.write('</FORM>\n')            
#optional tiers
            if (len(liste_Na0)) != 0:
                out.write('\t\t<NOTE xml:lang="Fcit" message="')
                out.write(str(liste_Na0[k][0]))
                out.write('"/>\n')
            if (len(liste_Na2)) != 0:
                out.write('\t\t<NOTE xml:lang="tone" message="')
                out.write(str(liste_Na2[k][0]))
                out.write('"/>\n')            
            if (len(liste_Na2)) != 0:
                out.write('\t\t<TRANSL xml:lang="zh">')
                out.write(str(liste_CH[k][0]))
                out.write('</TRANSL>\n')
            if (len(liste_Na2)) != 0:
                out.write('\t\t<TRANSL xml:lang="en">')
                out.write(str(liste_EN[k][0]))
                out.write('</TRANSL>\n')
            if (len(liste_Na2)) != 0:
                out.write('\t\t<TRANSL xml:lang="fr">')
                out.write(str(liste_FR[k][0]))
                out.write('</TRANSL>\n')
            if (len(liste_Comm)) != 0:
                out.write('\t\t<NOTE xml:lang="comm" message="')
                out.write(str(liste_Comm[k][0]))
                out.write('"/>\n')
            #start writing at word level (required tier)
            sentence = str(liste_Na1[k][0])
            wordliste = sentence.split()
            gloss = str(liste_Na3[k][0])
            glossliste = gloss.split()
            if ((len(wordliste) - len(glossliste)) == 0) :
                for m in range(len(wordliste)) :
                    out.write('\t\t<W>')
                    out.write('\t\t\t<FORM>')
                    out.write(wordliste[m])
                    out.write('</FORM>\n')
                    out.write('\t\t\t<TRANSL xml:lang="en">')
                    out.write(glossliste[m])
                    out.write('</TRANSL>\n')
                    out.write('\t\t</W>\n')
            else :
                print("gloss and phonol tiers don't have the same number of entries")
                print("current item is the interval " + liste_numitem[k][1] + ";" + liste_numitem[k][2])
                print("please check")
                sys.exit()
            out.write("\t</S>\n")
    out.write('</TEXT>\n')
        
else :
    print("The tiers don't have the same number of intervals. Please correct")
    sys.exit()
out.close()
