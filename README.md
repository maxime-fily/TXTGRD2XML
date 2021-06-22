# TXTGRD2XML
WARNING : the package Praat-textgrids v1.4 or later is required for this scripts : 
https://github.com/Legisign/Praat-textgrids

These are Python scripts dedicated to converting textgrids into xml files for Pangloss (https://pangloss.cnrs.fr/).
  There are two different scripts dedicated to the work of linguists:
TXTGRD2XML_input-txt.py which converts word lists, elicited and annotated in a textgrid, into an xml file
TXTGRD2XML_multi-tires.py which converts sentences, elicited and annotated in a textgrid, into an xml file
  Herebelow is reproduced the Header of each of the files, so that the user can refer to a protocol for the execution of the program :

I) WORD LISTS (TXTGRD2XML_input-txt.py)
     Instructions
 1- before launching, please make sure that your input is in one directory only
 2- Enter the work directory (where the inputs are)
 3- Enter the .TextGrid name WITHOUT the extension for variables consistency
 4- The programm assumes that textgrid and audio files bear the same name. If not, you have to change the file name in the output HEADER
 5- the linguistic input originate from 2 files with the SAME name :
     - my_file.txt (translations, gloses, etc.)
     - my_file.TextGrid ; see below
               * the Textgrid file requires two tiers (numitem and comment),
               but it can accept other tiers, although they will simply be ignored
               * numitem formats are imposed : start with d (decimal), plus (optionally) "_" followed 
               with any number of ASCII characters
 6- the xml in the output does not contain any markup as to which viewing option is assumed because it depends on the formalism of the destination website
 and should therefore be added by the Pangloss team (the two first lines of an xml, usually).

II) SENTENCES (TXTGRD2XML_multi-tires.py)
  Instructions
 1- before launching, please make sure that your input is in one directory only
 2- Enter the work directory (where the inputs are)
 3- Enter the .TextGrid name WITHOUT the extension for variables consistency
 3- The programm assumes that textgrid and audio files bear the same name. If not, you have to change the file name in the output HEADER
 4- the linguistic input originate from one file : the .TextGrid ;
           * the .Textgrid file requires 3 tiers (numitem, surface phonol, gloss),
           but it can accept other tiers, such as phonetic, ENGLISH, FRENCH, CHINESE, tone pattern
           * numitem formats are imposed : start with d (decimal), plus (optionally) "_" followed 
           with any number of ASCII characters
 5- the xml in the output does not contain any markup as to which viewing option is assumed because it depends on the formalism of the destination website and should therefore be added by the Pangloss team (the two first lines of an xml, usually).
