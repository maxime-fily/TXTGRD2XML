#------------------------------------------------------------------------------------
# XML Generator for praat users working on the Pangloss collection
# https://pangloss.cnrs.fr/
# This Python script READS INFORMATION FROM 
# (i) AN EXCEL SPREADSHEET (CONVERTED TO CSV FILE TABULAR SEP)
# (ii) A PRAAT TEXT GRID (itemized)
# AND WRITES THE OUTPUT TO AN XML FILE
# September 2020
#-----------------------------------------------------------------------------------

# Written by Maxime FILY, UGA
# NOANOA Project 2020

# Instructions
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
#####################################################
#Historique des modifications
#01/02/2022 : Refonte du format d'écriture des metadonnees
#02/02/2022 : modification de l'identifiant des mots par ajout de la balise temporelle
#03/02/2022 : ajout des commentaires praat et excel en plus des infos d'UID III_Ferlus
#24/03/2022 : réorganisation des notes commentaires pour faire apparaître la glose en premier
#24/03/2022 : passage aux formes officielles phone ortho et transliter
#20/04/2022 : retrait dans la partie ménage de la commande d'effacement du fichier de métadonnées, car à chaque test il est inchangé et qu'il est assez long à écrire
#26/04/2022 : ajout de la tête d'identifiant W aux mots

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


# ecriture donnees utilisateur
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
fileNAME = '/home/fily/Documents/lexical_data/liste_1616_lemmes.txt'
os.chdir(dirNAME)
audioINFOS = '/home/fily/Documents/acoustic_data/audio_info_curated.txt'

#Definition of the case-insensitive strings of interest
T_string = re.compile("EN", re.IGNORECASE)
G_string = re.compile("gloss", re.IGNORECASE)
P_string = re.compile("phonol", re.IGNORECASE)
C_string = re.compile("comment", re.IGNORECASE)
F_string = re.compile("phonet", re.IGNORECASE)
Fr_string = re.compile("FR", re.IGNORECASE)
Ch_string = re.compile("CH", re.IGNORECASE)




#generic metadata ("no" case)
ident = "crdo-NRU_unspecified_recording"
lngG = "NRU"
eng_desc = "unspecified"

#output
fcsv = textGRD + "_tsp.csv"
gcsv = textGRD + "_comm.csv"
outNAME = textGRD + '.xml'
metaNAME = textGRD + "_metadata.txt"

#ménage
if os.path.exists(dirNAME + "/" + fcsv):
    os.remove(dirNAME + "/" + fcsv)
if os.path.exists(dirNAME + "/" + gcsv):
    os.remove(dirNAME + "/" + gcsv)
if os.path.exists(dirNAME + "/" + outNAME):
    os.remove(dirNAME + "/" + outNAME)


# ecriture metadonnees
print("do you wish to input the metadata for this recording? (y/n)")
answer = input()
if (answer == "Y") or (answer == "y"):
    print("enter the name of your project (template : crdo-NRU_recording_identifier)")
    ident = input()
    print("this is your project : " + ident)
    print("enter the language code (ISO-639-3)")
    lngG = input()
    print("enter the language name as given in glottolog")
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
    print("enter the name of the interviewer(s), as a semicolumn-separated list: lastname, firstname")
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
    meta.write("recording ID\tFile Location\tFile name (with extension)\tMain title (plus 2-letter language code)\tOther title (plus 2-letter language code)\t language code (3-letter code)\tOther languages on the recording or used for annotations (3-letter code)\tPlace of recording\tLatitude\tLongitude\tdate (YYYY-MM-DD)\tDepositor\tResearcher(s) (format : Last1,First1 ; Last2, First2, ... ; Lastn, Firstn)\tSpeaker(s) (format : Last1,First1 ; Last2, First2, ... ; Lastn, Firstn)\tSponsor(s) (format : Last1,First1 ; Last2, First2, ... ; Lastn, Firstn)\tOther contributors ( + role)\tDuration\tSummary\tInstitute\tAccess right\tLicense (if public)\tCopyright\tCollection (e.g. Lacito, Langues de FRance, ..., autres)\tAssociated files with audio (xml, pdf, doc, textgrid)\tDocument type (lexicon, text, lists in carrier sentences)\tDiscourse category (dialogue, narrative, questionnaires)\trecording medium (K7, DAT, WAV, etc)\tAdditional information\n")
    meta.write(ident + "\t")
    meta.write(dirNAME + "\t")
    meta.write(textGRD + ".wav\t")
    meta.write(eng_ttl + " (en)\t")
    meta.write(eng_desc + " (en);" + fra_desc + " (fr);" + cmn_desc + " (zh)\t")
    meta.write(lngG + "\t")
    meta.write(lngH + "\t")
    meta.write(locEN + " (eng. toponym)" + locOA + " (official post address)\t")
    meta.write(latGPS + "\t")
    meta.write(lonGPS + "\t")
    meta.write(dateREC + "\t")
    meta.write(depositor + "\t")
    meta.write(researcher + "\t")
    meta.write(speaker   + "\t")
    meta.write(sponsor + "\t")
    meta.write(interviewer   + " (interviewer)\t")   
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
    meta.write("glottolog name of the language recorded: " + lngN + "\n")
    meta.close()
    print("the data generated through standard input are recorded in " + metaNAME )
#Donnees generales
out = codecs.open(outNAME,'w',encoding='UTF-8')
out.write('<?xml-stylesheet type="text/xsl" href="view_text.xsl"?>\n')
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
out.write(dirNAME)
out.write('/')
out.write(textGRD)
out.write('.wav" />\n')
out.write('\t</HEADER>\n')


#Donnees linguistiques balisees
grid = textgrids.TextGrid(grd)
grid.tier_to_csv('numitem', fcsv)
grid.tier_to_csv('comment', gcsv)


# fichier temporel pour les numitem
fich_exploit = open(fcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_lue = list(fich_lu)
fich_exploit.close()

# fichier temporel pour les commentaires
gich_exploit = open(gcsv, encoding="utf8")
gich_lu = csv.reader(gich_exploit, delimiter = ';')
giste_lue = list(gich_lu)
gich_exploit.close()


# tableau avec infos complètes
tab_exploit = open(fileNAME, encoding="utf8")
tab_lu = csv.reader(tab_exploit, delimiter = '\t')
tabLIST = list(tab_lu)
tab_exploit.close()
#print(str(tabLIST[:][0]) + "!" + str(len(tabLIST[:][0])) + "!" + str(tabLIST[0][0]))
for j in range(len(tabLIST[:][0])):
    if tabLIST[0][j] == "UID":
        ind_ferlus0 = j
    if tabLIST[0][j] == "numero_FERLUS":
        ind_ferlus1 = j
    if tabLIST[0][j] == "paquet(I_EFEO,II_SOAS,III_Ferlus,IV_Pain,V_Michaud)":
        ind_ferlus2 = j
    if tabLIST[0][j] == "numitem":
        ind_item = j
    if tabLIST[0][j] == "FR":
        ind_FR = j
    if tabLIST[0][j] == "EN":
        ind_EN = j
    if tabLIST[0][j] == "CH":
        ind_CH = j
    if tabLIST[0][j] == "phonol":
        ind_NAP = j
    if tabLIST[0][j] == "phonet":
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
        itemferlus0 = tabLIST[i][ind_ferlus0]
    except (NameError, IndexError) as e:
        pass
    try:
        itemferlus1 = tabLIST[i][ind_ferlus1]
    except (NameError, IndexError) as e:
        pass
    try:
        itemferlus2 = tabLIST[i][ind_ferlus2]
    except (NameError, IndexError) as e:
        pass
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
        NAPword = tabLIST[i][ind_NAP]
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
            indice_textgrid = int(liste_lue[k][0].replace(" ","").split("_")[0])
        except ValueError:
            indice_textgrid = 0
        if (indice_textgrid - numitem) == 0:
            out.write('\t\t<W id="W')
            out.write(str(numitem) + "_" + str(liste_lue[k][1]))
            out.write('">\n')
            out.write('\t\t\t<AUDIO start="')
            out.write(str(liste_lue[k][1]))
            out.write('" end="')
            out.write(str(liste_lue[k][2]))
            out.write('" />\n')
            try:
                out.write("\t\t\t<FORM kindOf='phone'>")
                out.write(str(NAFword).replace('"',"'"))
                out.write('</FORM>\n')
            except:
                pass
            try:
                out.write("\t\t\t<FORM kindOf='phono'>")
                out.write(str(NAPword).replace('"',"'"))
                out.write('</FORM>\n')
            except:
                pass
            try:
                out.write('\t\t\t<TRANSL xml:lang="fr">')
                out.write(str(FRtrad).replace('"',"'"))
                out.write('</TRANSL>\n')
            except:
                pass
            try:
                out.write('\t\t\t<TRANSL xml:lang="zh">')
                out.write(str(CHtrad).replace('"',"'"))
                out.write('</TRANSL>\n')
            except:
                pass
            try:
                out.write('\t\t\t<TRANSL xml:lang="en">')
                out.write(str(ENtrad).replace('"',"'"))
                out.write('</TRANSL>\n')
            except:
                pass
            try:
                out.write('\t\t\t<NOTE xml:lang="fr" message=" UID : ')
                out.write(str(itemferlus0))
                out.write(' ; commentaire textgrid : ')
                str_modif = giste_lue[k][0].replace('"',"'").replace('&','and').replace("gloss:","G:").replace("phonol:","P:").replace("phonet:","S:").replace("comment:","C:")
                out2.write(str_modif)
                out2.write(' ; commentaire tableau : ' + str(comm).replace('"',"'") + ' ; note perso :' + str(note).replace('"',"'"))
                out2.write('"/>\n')
            except:
                pass
            out.write('\t\t</W>\n')
out.write('</WORDLIST>\n')
out.close()
