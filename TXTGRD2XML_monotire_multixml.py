#------------------------------------------------------------------------------------
# XML Generator for praat users working on the Pangloss collection
# https://pangloss.cnrs.fr/
# This Python script READS INFORMATION FROM 
# (i) A PRAAT TEXTGRID (sentences)
# AND WRITES THE OUTPUT TO AN XML FILE
# September 2020
#-----------------------------------------------------------------------------------

# Written by Maxime FILY, Université Grenoble Alpes
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
#point de départ = monotire monoxml
#06/04/2022 : Ajout d'une sortie xml pour chaque type de donnée : Seule et Phrases Guidées
#07/04/2022 : test pré_écriture pour ordonner les entrée et mettre l'occurence "vedette" en premier.
#14/04/2022 : Correction d'un bug de boucle qui fermait le fichier sur une indentation trop profonde et causait par conséquent l'overwrite de données précédemment écrite
#20/04/2022 : Fiabilisation par ajout de replace aux endroits clés (tests, écriture sur fichier)
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
fileNAME = '/home/fily/Documents/lexical_data/liste_1616_lemmes.txt'
os.chdir(dirNAME)

#generic metadata ("no" case)
ident = "crdo-NRU_unspecified_recording"
lngG = "NRU"
eng_desc = "unspecified"


#Definition of the case-insensitive strings of interest
T_string = re.compile("EN", re.IGNORECASE)
G_string = re.compile("gloss", re.IGNORECASE)
P_string = re.compile("phonol", re.IGNORECASE)
C_string = re.compile("comment", re.IGNORECASE)
F_string = re.compile("phonet", re.IGNORECASE)
Fr_string = re.compile("FR", re.IGNORECASE)
Ch_string = re.compile("CH", re.IGNORECASE)

#output

outNAME1 = textGRD + '_TEXT.xml'
outNAME2 = textGRD + '_LIST.xml'
metaNAME = textGRD + "_metadata.txt"
print("the data generated through standard input are recorded in " + metaNAME )

fcsv = textGRD + "_tsp.csv"
gcsv = textGRD + "_comm.csv"
#ménage
if os.path.exists(dirNAME + "/" + fcsv):
    os.remove(dirNAME + "/" + fcsv)
if os.path.exists(dirNAME + "/" + gcsv):
    os.remove(dirNAME + "/" + gcsv)
if os.path.exists(dirNAME + "/" + outNAME1):
    os.remove(dirNAME + "/" + outNAME1)
if os.path.exists(dirNAME + "/" + outNAME2):
    os.remove(dirNAME + "/" + outNAME2)
    
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
    
#frame sentence option
print("Is there a frame sentence for the guided part (y/n) ?")
answer = input()
if ((answer == "Y") or (answer == "y")):
    print('please enter the sentence in IPA/ortho/any language (use "..." to indicate word place)')
    time.sleep(1)
    sentence = input()
else: 
    time.sleep(1)
    sentence = " "



#ouverture fichiers de travail
out1 = codecs.open(outNAME1,'w',encoding='UTF-8')
out2 = codecs.open(outNAME2,'w',encoding='UTF-8')


#Donnees generales
out1.write('<?xml-stylesheet type="text/xsl" href="view_text.xsl"?>\n')
out1.write('<TEXT id="')
out1.write(ident)
out1.write('" xml:lang="')
out1.write(lngG)
out1.write('">\n')
out1.write('\t<HEADER>\n')
out1.write('\t\t<TITLE xml:lang="eng">')
out1.write(eng_desc)
out1.write('</TITLE>\n')
out1.write('\t\t<SOUNDFILE href="')
out1.write(dirNAME)
out1.write('/')
out1.write(textGRD)
out1.write('.wav" />\n')
out1.write('\t</HEADER>\n')

#Donnees generales
out2.write('<?xml-stylesheet type="text/xsl" href="view_text.xsl"?>\n')
out2.write('<WORDLIST id="')
out2.write(ident.replace('"',"'"))
out2.write('" xml:lang="')
out2.write(lngG.replace('"',"'"))
out2.write('">\n')
out2.write('\t<HEADER>\n')
out2.write('\t\t<TITLE xml:lang="eng">')
out2.write(eng_desc.replace('"',"'"))
out2.write('</TITLE>\n')
out2.write('\t\t<SOUNDFILE href="')
out2.write(dirNAME.replace('"',"'"))
out2.write('/')
out2.write(textGRD.replace('"',"'"))
out2.write('.wav" />\n')
out2.write('\t</HEADER>\n')

#Tier identification for the program. The markers for tier_name are hardcoded on this version
#For customization, the user may change the tier names below to match his/her TextGrid_file
#USER MODIFICATION START
###################################################################################################
#Donnees linguistiques balisees
grid = textgrids.TextGrid(grd)
grid.tier_to_csv('numitem', fcsv)
grid.tier_to_csv('comment', gcsv)


# fichier temporel pour les numitem
fich_exploit = open(fcsv, encoding="utf8")
fich_lu = csv.reader(fich_exploit, delimiter = ';')
liste_numitem_pre = list(fich_lu)
fich_exploit.close()
#liste_numitem = [[0 * len(liste_numitem_pre)],[0 * len(liste_numitem_pre)],[0 * len(liste_numitem_pre)]]
liste_numitem = []
# fichier retrié : création
# hich_exploit = open(hcsv, encoding="utf8")
# fichier temporel pour les commentaires

gich_exploit = open(gcsv, encoding="utf8")
gich_lu = csv.reader(gich_exploit, delimiter = ';')
giste_lue_pre = list(gich_lu)
gich_exploit.close()

#giste_lue = [[0 * len(giste_lue_pre)],[0 * len(giste_lue_pre)],[0 * len(giste_lue_pre)]]
giste_lue = []

c=0
for k in range(len(liste_numitem_pre)):
    print(liste_numitem_pre[k][0])
    if (liste_numitem_pre[k][0].replace(" ","") == ""): 
        pass
    elif (liste_numitem_pre[k][0].split("_")[1] == "PB"):
        liste_numitem.append(liste_numitem_pre[k])
        giste_lue.append(giste_lue_pre[k])
        c += 1
for k in range(len(liste_numitem_pre)):
    if (liste_numitem_pre[k][0].replace(" ","") == ""): 
        pass
    elif (liste_numitem_pre[k][0].split("_")[1] == "N"):
        liste_numitem.append(liste_numitem_pre[k])
        giste_lue.append(giste_lue_pre[k])
        c += 1
for k in range(len(liste_numitem_pre)):
    if (liste_numitem_pre[k][0].replace(" ","") == ""): 
        pass
    elif (liste_numitem_pre[k][0].split("_")[1] == "A"):
        liste_numitem.append(liste_numitem_pre[k])
        giste_lue.append(giste_lue_pre[k])
        c += 1
for k in range(len(liste_numitem_pre)):
    if (liste_numitem_pre[k][0].replace(" ","") == ""): 
        pass
    elif (liste_numitem_pre[k][0].split("_")[1] == "U"):
        liste_numitem.append(liste_numitem_pre[k])
        giste_lue.append(giste_lue_pre[k])
        c += 1
for k in range(len(liste_numitem_pre)):
    if (liste_numitem_pre[k][0].replace(" ","") == ""): 
        pass
    elif (liste_numitem_pre[k][0].split("_")[1] == "B"):
        liste_numitem.append(liste_numitem_pre[k])
        giste_lue.append(giste_lue_pre[k])
        c += 1
#OK
#print(liste_numitem)


# tableau avec infos complètes
tab_exploit = open(fileNAME, encoding="utf8")
tab_lu = csv.reader(tab_exploit, delimiter = '\t')
tabLIST = list(tab_lu)
tab_exploit.close()

#set to null some displayed var
NAFword = " "
NAPword = " "
FRtrad = " "
ENtrad = " "
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
    if tabLIST[0][j] == "Note perso":
        ind_note = j



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
    try:
        note = tabLIST[i][ind_note]
    except (NameError, IndexError) as e:
        pass
    if (len(liste_numitem_pre) - len(giste_lue_pre)) == 0:
        for k in range(len(liste_numitem)):
            try:
                indice_textgrid = liste_numitem[k][0].replace(" ","")
                indice_UID = int(liste_numitem[k][0].split("_")[0].replace(" ",""))
                indice_NAT = str(liste_numitem[k][0].split("_")[1].replace(" ",""))
                indice_CTX = str(liste_numitem[k][0].split("_")[2].replace(" ",""))
            except ValueError:
                print("error on " + liste_numitem[k][0] + "at definition stage")
                pass
#            indice_textgrid = 0
#            print("IT " + indice_textgrid.split("_")[0])
#            print('NUMIT' + str(numitem))
            if (indice_UID == numitem) :
#
#PARTIE CONSACREE AU(X) XML AU FORMAT <WORDLIST>
#
#
                if (indice_CTX == "PG") :
                    if (indice_NAT == "PB" or indice_NAT == "N" or indice_NAT == "A" or indice_NAT == "U" or indice_NAT == "B") :
                        out2.write('\t\t<W id="W')
                        out2.write(str(numitem).replace(' ','') + "_" + str(liste_numitem[k][1]))
                        out2.write('">\n')
                        out2.write('\t\t\t<AUDIO start="')
                        out2.write(str(liste_numitem[k][1]))
                        out2.write('" end="')
                        out2.write(str(liste_numitem[k][2]))
                        out2.write('" />\n')
                        try:
                            out2.write("\t\t\t<FORM kindOf='phone'>")
                            out2.write(sentence.split("...")[0] + " + [")
                            out2.write(str(NAFword).replace('"',"'"))
                            out2.write("] + " + sentence.split("...")[1])
                            out2.write('</FORM>\n')
                        except:
                            pass
                        try:
                            out2.write("\t\t\t<FORM kindOf='phono'> /")
                            out2.write(str(NAPword).replace('"',"'"))
                            out2.write('/ </FORM>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<TRANSL xml:lang="fr">')
                            out2.write(str(FRtrad).replace('"',"'"))
                            out2.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<TRANSL xml:lang="zh">')
                            out2.write(str(CHtrad).replace('"',"'"))
                            out2.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<TRANSL xml:lang="en">')
                            out2.write(str(ENtrad).replace('"',"'"))
                            out2.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<NOTE xml:lang="fr" message=" UID (+renvois): ')
                            out2.write(str(itemferlus0).replace('"',"'"))
                            out2.write(" ("+str(renvoi)+")")
                            out2.write(' ; ')
                            str_modif = giste_lue[k][0].replace('"',"'").replace('&','and').replace("gloss:","G:").replace("phonol:","P:").replace("phonet:","S:").replace("comment:","C:")
                            out2.write(str_modif.replace('"',"'"))
                            out2.write(' ; ' + str(comm).replace('"',"'"))# + ' ; note perso :' + str(note).replace('"',"'"))
                            out2.write('"/>\n')
                        except:
                            pass
                        out2.write('\t\t</W>\n')
                elif (indice_CTX == "S") :
                    if (indice_NAT == "PB" or indice_NAT == "N" or indice_NAT == "A" or indice_NAT == "U" or indice_NAT == "B") :
                        out2.write('\t\t<W id="W')
                        print(str(numitem).replace('"',"'"))
                        out2.write(str(numitem).replace('"',"'") + "_" + str(liste_numitem[k][1]))
                        out2.write('">\n')
                        out2.write('\t\t\t<AUDIO start="')
                        out2.write(str(liste_numitem[k][1]))
                        out2.write('" end="')
                        out2.write(str(liste_numitem[k][2]))
                        out2.write('" />\n')
                        try:
                            out2.write("\t\t\t<FORM kindOf='phone'>")
                            out2.write(str(NAFword).replace('"',"'"))
                            out2.write('</FORM>\n')
                        except:
                            pass
                        try:
                            out2.write("\t\t\t<FORM kindOf='phono'>")
                            out2.write(str(NAPword).replace('"',"'"))
                            out2.write('</FORM>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<TRANSL xml:lang="fr">')
                            out2.write(str(FRtrad).replace('"',"'"))
                            out2.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<TRANSL xml:lang="zh">')
                            out2.write(str(CHtrad).replace('"',"'"))
                            out2.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<TRANSL xml:lang="en">')
                            out2.write(str(ENtrad).replace('"',"'"))
                            out2.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out2.write('\t\t\t<NOTE xml:lang="fr" message=" UID (+renvois): ')
                            out2.write(str(itemferlus0).replace('"',"'"))
                            out2.write(" ("+str(renvoi)+")")
                            out2.write(' ; ')
                            str_modif = giste_lue[k][0].replace('"',"'").replace('&','and').replace("gloss:","G:").replace("phonol:","P:").replace("phonet:","S:").replace("comment:","C:")
                            out2.write(str_modif.replace('"',"'"))
                            out2.write(' ; ' + str(comm).replace('"',"'"))# + ' ; note perso :' + str(note).replace('"',"'"))
                            out2.write('"/>\n')
                        except:
                            pass
                        out2.write('\t\t</W>\n')
#
#PARTIE CONSACREE AU(X) XML AU FORMAT <SENTENCE>
#
#
                elif (indice_CTX == "PC") :
                    if (indice_NAT == "PB" or indice_NAT == "N" or indice_NAT == "A" or indice_NAT == "U" or indice_NAT == "B") :
#required tiers
#                        out1.write('\t\t<NOTE xml:lang="en" message="UID = ')
#                        out1.write(str(liste_numitem[k][0]))
#                        out1.write('"/>\n')
                        out1.write('\t<S id="S')
                        out1.write(str(liste_numitem[k][0]).replace(" ","") + "_" + str(liste_numitem[k][1]))
                        out1.write('">\n')
                        out1.write('\t\t<AUDIO start="')
                        out1.write(str(liste_numitem[k][1]))
                        out1.write('" end="')
                        out1.write(str(liste_numitem[k][2]))
                        out1.write('" />\n')

                    #Début définition des entrées commentaires
                        str_modif = F_string.sub("phonet",C_string.sub("comment",P_string.sub("phonol",G_string.sub("gloss",str(giste_lue[k][0])))))
#                    print("str " + str_modif)
#                    print("strc " + str(str_modif.count(";")))
#Begin of variable reset
                        glocont = " "
                        phocont = " "
                        phicont = " "
                        engcont = " "
                        fracont = " "
                        chicont = " "
                        comcont = " "

                        for i in range((str_modif.count(";")+1)):
#End of variable reset
                            typeof = str_modif.split(";")[i]
                            print(typeof)
                            print(typeof.split(":")[0].replace(" ",""))
                            if typeof.split(":")[0].replace(" ","") == "gloss":
                                glocont = str_modif.split(";")[i].replace(" :",":").replace("gloss:","")
                            elif typeof.split(":")[0].replace(" ","") == "phonol":
                                phocont = str_modif.split(";")[i].replace(" :",":").replace("phonol:","")
                            elif typeof.split(":")[0].replace(" ","") == "phonet":
                                phicont = str_modif.split(";")[i].replace(" :",":").replace("phonet:","").append(" - ")
                            elif typeof.split(":")[0].replace(" ","") == "EN":
                                engcont = str_modif.split(";")[i].replace(" :",":").replace("EN:","")
                            elif typeof.split(":")[0].replace(" ","") == "FR":
                                fracont = str_modif.split(";")[i].replace(" :",":").replace("FR:","")
                            elif typeof.split(":")[0].replace(" ","") == "CH":
                                chicont = str_modif.split(";")[i].replace(" :",":").replace("CH:","")
                            elif typeof.split(":")[0].replace(" ","") == "comment":
                                comcont = str_modif.split(";")[i].replace(" :",":").replace("comment:","")
                            else: 
                                comcont = str_modif
                        try:
                            out1.write('\t\t<FORM kindOf="phone">')
                            out1.write(phicont + " Recording quality: " + indice_NAT)
                            out1.write('</FORM>\n')
                        except:
                            pass
                        try:
                            out1.write('\t\t<FORM kindOf="phono">')
                            
                            out1.write(phocont.replace('"',"'"))
                      #  print(phocont)
                            out1.write('</FORM>\n')            
                        except:
                            pass
                        try:
                            out1.write('\t\t<FORM kindOf="transliter">')
                            out1.write(glocont.replace('"',"'"))
                 #       print(glocont)
                            out1.write('</FORM>\n')
                        except:
                            pass
                        try:
                            out1.write('\t\t<TRANSL xml:lang="fr">')
                            out1.write(fracont.replace('"',"'"))
                            out1.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out1.write('\t\t<TRANSL xml:lang="en">')
                            out1.write(engcont.replace('"',"'"))
                            out1.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out1.write('\t\t<TRANSL xml:lang="zh">')
                            out1.write(chicont.replace('"',"'"))
                            out1.write('</TRANSL>\n')
                        except:
                            pass
                        try:
                            out1.write('\t\t<NOTE xml:lang="fr" message=" commentaire GRD : ')
                            out1.write(comcont.replace('"',"'"))
                            out1.write("; entry of interest: ")
                            out1.write(str(indice_UID))
                            out1.write("/")
                            out1.write(NAFword.replace('"',"'"))
                            out1.write("/ (")
                            out1.write(NAPword.replace('"',"'")) 
                            out1.write(") /ph/ (cit), ")
                            out1.write(ENtrad.replace('"',"'"))
                            out1.write(" (EN), ")
                            out1.write(FRtrad.replace('"',"'"))
                            out1.write(" (FR)")
                            out1.write('"/>\n')
                        except:
                            pass
#End of the tiers transposition

                        out1.write("\t</S>\n")
                else: 
                    print("non-matching expression : _" + indice_CTX + "_ (CTX)")
                    pass
            else:
                pass
    else :
        print("The tiers don't have the same number of intervals. Please correct")
        sys.exit()
out1.write('</TEXT>\n')
out2.write('</WORDLIST>\n')
out1.close()
out2.close()
