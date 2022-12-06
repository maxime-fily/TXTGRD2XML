#------------------------------------------------------------------------------------
# XML Generator for praat users working on the Pangloss collection
# https://pangloss.cnrs.fr/
# This Python script READS INFORMATION FROM 
# (i) A PRAAT TEXTGRID (sentences)
# AND WRITES THE OUTPUT TO AN XML FILE
# September 2020
#-----------------------------------------------------------------------------------

# Written by Maxime FILY, Université Paris 3 Sorbonne Nouvelle
# Project : Pangloss
#

# Instructions
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

#Historique des modifications
#01/02/2022 : Refonte du format d'écriture des metadonnees
#02/02/2022 : modification de l'identifiant des mots par ajout de la balise temporelle
#03/02/2022 : ajout des commentaires praat et excel en plus des infos d'UID III_Ferlus
#24/03/2022 : réorganisation des notes commentaires pour faire apparaître la glose en premier
#24/03/2022 : passage aux formes officielles phone ortho et transliter
#24/03/2022 : limitation des langues de sortie à EN et ZH
#24/03/2022 : suppression de la tire "tone pattern"
#24/03/2022 : correction d'une erreur dans un test (longueur listes = 1 et non 0 pour une tire vide)
#22/04/2022 : retrait dans la partie ménage de la commande d'effacement du fichier de métadonnées, car à chaque test il est inchangé et qu'il est assez long à écrire
#26/04/2022 : ajout de la tête d'identifiant S aux mots

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

#initialisations
#input
grd = textGRD + '.TextGrid'
aud = textGRD + '.wav'
audioINFOS = '/home/fily/Documents/acoustic_data/audio_info_curated.txt'
os.chdir(dirNAME)

#generic metadata ("no" case)
ident = "crdo-NRU_unspecified_recording"
lngG = "NRU"
eng_desc = "unspecified"



#output
fcsv = textGRD + "_numitem.csv"
g0csv = textGRD + "_Nafon.csv"
g1csv = textGRD + "_Napho.csv"
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

# ecriture metadonnees
print("do you wish to input the metadata for this recording? (y/n)")
answer = input()
if (answer == "Y") or (answer == "y"):
    print("enter the name of your project (template : crdo-NRU_recording_identifier)")
    ident = input()
    print("this is your project : " + ident)
    print("enter the language code (in glottolog)")
    lngG = input()
    print("enter the language name (e.g. Yongning Na)")
    lngN = input()
    print("language selected : " + lngN + ", glottolog id = " + lngG)
    print("enter any other languages present in the recording (using 3-letter codes, each language separated with semicolumn)")
    lngH = input()
    print("languages used together with " + lngN + " : " + lngH)
    print("enter recording title (english)")
    eng_ttl = input()
    print("recording title: " + eng_ttl)
    print("enter recording description (english):")
    eng_desc = input()
    print("recording description : " + eng_desc)
    print("saisir la description de l'enregistrement (optionnel):")
    fra_desc = input()
    print("description de l'enregistrement : " + fra_desc)
    print("请您输入记录品简介(自选):")
    cmn_desc = input()
    print("记录品简介 : " + cmn_desc)
    print("enter the name of the editor : ")
    editor = input()
    print("enter the name of the institute : ")
    institute = input()
    print("enter the name of the depositor: firstname, lastname ")
    depositor = input()
    print("enter the name of the researcher(s), as a semicolumn-separated list: lastname, firstname")
    researcher = input()
    print("enter the name of the speaker(s), as a semicolumn-separated list: lastname, firstname")
    speaker = input()
    print("enter the name of the interviewer(s), as a semicolumn-separated list: lastname, firstname (role)")
    interviewer = input()
    print("enter the name of the sponsor(s), as a semicolumn-separated list")
    sponsor = input()
    print("enter the place of recording (in English): ")
    locEN = input()
    print("enter the place of recording (official postal address): ")
    locOA = input()
    print("enter the latitude of the place of recording: ")
    latGPS = input()
    print("enter the longitude of the place of recording: ")
    lonGPS = input()
    print("enter the date of recording (YYYY-MM-DD): ")
    dateREC = input()
    print("enter the format of recording (wav or mp3): ")
    formT = input()
    print("enter the type of annotations treated (xml, textgrids, pdf, etc): ")
    typeT = input()
    print("enter the type of license (e.g. cc-by-nc): ")
    URLL = input()
    print("enter the license's access rights (free, unmodified, quote) : ")
    typeL = input()
    print("thank you")
    time.sleep(1)
    print("For information, we will be working with " + textGRD + ".wav")
    time.sleep(1)


    #metadata
    #retrieved automatically
    tab_audio = open(audioINFOS, encoding="utf8")
    tab_ecout = csv.reader(tab_audio, delimiter = '\t')
    tabLISZ = list(tab_ecout)
    tab_audio.close()

    for j in range(1,len(tabLISZ)):
        if tabLISZ[j][0] == aud:
            duration = tabLISZ[j][1]
            discourse_type = tabLISZ[j][2]
            discourse_cat = tabLISZ[j][3]
     #retrieved from user input
    meta = codecs.open(metaNAME,'w',encoding='UTF-8')
    meta.write("recording ID\tFile Location\tFile name (with extension)\tMain title (plus 2-letter language code)\tOther title (plus 2-letter language code)\t language code (3-letter code)\tOther languages on the recording or used for annotations (3-letter code)\tPlace of recording\tLatitude\tLongitude\tdate (YYYY-MM-DD)\tDepositor\tResearcher(s) (format : Last1,First1 ; Last2, First2, ... ; Lastn, Firstn)\tSpeaker(s) (format : Last1,First1 ; Last2, First2, ... ; Lastn, Firstn)\tSponsor(s) (format : Last1,First1 ; Last2, First2, ... ; Lastn, Firstn)\tOther contributors ( + role)\tDuration\tSummary\tInstitute\tAccess right\tLicense (if public)\tCopyright\tCollection (e.g. Lacito, Langues de France, ..., autres)\tAssociated files with audio (xml, pdf, doc, textgrid)\tDocument type (lexicon, text, lists in carrier sentences)\tDiscourse category (dialogue, narrative, questionnaires)\trecording medium (K7, DAT, WAV, etc)\tAdditional information\n")
    meta.write(ident + "\t")
    meta.write(dirNAME + "\t")
    meta.write(textGRD + ".wav\t")
    meta.write(eng_ttl + " (en)\t")
    meta.write(eng_desc + " (en);" + fra_desc + " (fr);" + cmn_desc + " (zh)\t")
    meta.write(lngG + "\t")
    meta.write(lngH + "\t")
    meta.write(locEN + " (eng. toponym), " + locOA + " (official post address)\t")
    meta.write(latGPS + "\t")
    meta.write(lonGPS + "\t")
    meta.write(dateREC + "\t")
    meta.write(depositor + "\t")
    meta.write(researcher + "\t")
    meta.write(speaker   + "\t")
    meta.write(sponsor + "\t")
    meta.write(interviewer   + " (interviewer(s))\t")   
    meta.write(duration   + "\t")
    meta.write(eng_desc + "\t")
    meta.write(institute + "\t")
    meta.write(typeL + "\t")
    meta.write(URLL + "\t")
    meta.write(depositor + "\t")
    meta.write(editor + "\t")
    meta.write(typeT + "\t")
    meta.write(discourse_type + "\t")
    meta.write(discourse_cat + "\t")
    meta.write(formT + "\t")
    meta.write("other names of the language recorded: " + lngN + "\n")
    meta.close()
    print("the data generated through standard input are recorded in " + metaNAME )
    time.sleep(1)

#ouverture fichier de travail
out = codecs.open(outNAME,'w',encoding='UTF-8')

#Donnees generales
out.write('<?xml-stylesheet type="text/xsl" href="view_text.xsl"?>\n')
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
out.write(dirNAME)
out.write('/')
out.write(textGRD)
out.write('.wav" />\n')
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
#try:
#    grid.tier_to_csv('tone pattern', g2csv)
#except: 
#    pass
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

print(len(liste_numitem))
print(len(liste_Na0))
print(len(liste_Na1))
print(len(liste_Na3))
print(len(liste_CH))
print(len(liste_EN))
print(len(liste_Comm))

if (((len(liste_Na0) - len(liste_numitem)) == 0) or ((len(liste_Na0)) == 0)) and ((len(liste_Na1) - len(liste_numitem)) == 0) and ((len(liste_Na3) - len(liste_numitem)) == 0) and ((len(liste_CH) - len(liste_numitem)) == 0) and ((len(liste_EN) - len(liste_numitem)) == 0) and (((len(liste_Comm) - len(liste_numitem)) == 0) or ((len(liste_Comm)) == 0)) :

    for k in range(len(liste_numitem)):
        try:
            indice_textgrid = liste_numitem[k][0].replace(" ","")
#            indice_textgrid = int(liste_numitem[k][0].split("_")[0])
        except ValueError:
            indice_textgrid = ""
        if indice_textgrid != "":
            out.write('\t<S id="S')
            out.write(str(liste_numitem[k][0]).replace(' ',''))
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
            out.write('\t\t<FORM kindOf="phone">')
            out.write(str(liste_Na0[k][0]).replace('"',"'"))
            out.write('</FORM>\n')            
            out.write('\t\t<FORM kindOf="phono">')
            out.write(str(liste_Na1[k][0]).replace('"',"'"))
            out.write('</FORM>\n')            
            out.write('\t\t<FORM kindOf="transliter">')
            out.write(str(liste_Na3[k][0]).replace('"',"'"))
            out.write('</FORM>\n')            
#optional tiers : 1 is the length of an empty tier
            if (len(liste_CH)) != 1:
                out.write('\t\t<TRANSL xml:lang="zh">')
                out.write(str(liste_CH[k][0]).replace('"',"'"))
                out.write('</TRANSL>\n')
            if (len(liste_EN)) != 1:
                out.write('\t\t<TRANSL xml:lang="en">')
                out.write(str(liste_EN[k][0]).replace('"',"'"))
                out.write('</TRANSL>\n')
            if (len(liste_FR)) != 0:
                out.write('\t\t<TRANSL xml:lang="fr">')
                out.write(str(liste_FR[k][0]).replace('"',"'"))
                out.write('</TRANSL>\n')
            if (len(liste_Comm)) != 1:
                out.write('\t\t<NOTE xml:lang="comm" message="')
                out.write(str(liste_Comm[k][0]).replace('"',"'"))
                out.write('"/>\n')
            #start writing at word level (required tier)
#            sentence = str(liste_Na1[k][0])
#            wordliste = sentence.split()
#            gloss = str(liste_Na3[k][0])
#            glossliste = gloss.split()
#            if ((len(wordliste) - len(glossliste)) == 0) :
#                for m in range(len(wordliste)) :
#                    out.write('\t\t<W>')
#                    out.write('\t\t\t<FORM>')
#                    out.write(wordliste[m])
#                    out.write('</FORM>\n')
#                    out.write('\t\t\t<TRANSL xml:lang="en">')
#                    out.write(glossliste[m])
#                    out.write('</TRANSL>\n')
#                    out.write('\t\t</W>\n')
#            else :
#               print("gloss and phonol tiers don't have the same number of entries")
#                print("current item is the interval " + liste_numitem[k][1] + ";" + liste_numitem[k][2])
 #               print("please check")
  #              sys.exit()
            out.write("\t</S>\n")
    out.write('</TEXT>\n')
        
else :
    print("The tiers don't have the same number of intervals. Please correct")
    sys.exit()
out.close()
