# TXTGRD2XML

WARNING : the package Praat-textgrids v1.4 or later is required for this script : 

https://github.com/Legisign/Praat-textgrids, by @Legisign

These are Python scripts dedicated to converting textgrids into xml files for Pangloss (https://pangloss.cnrs.fr/).

There are two different scripts dedicated to the work of linguists:

`TXTGRD2XML_monotire-monoxml.py` which converts word lists, elicited and annotated in a textgrid, into one xml file (WORDLIST).

`TXTGRD2XML_multitires-monoxml.py` which converts sentences, transcribed and annotated in a multitier textgrid, into one xml file with several lines per utterance (TEXT).

`TXTGRD2XML_monotire-multixml.py` which converts word lists and sentences, elicited and annotated in a textgrid, into 2 xml files (WORDLIST and TEXT).

Herebelow is reproduced the Header of each of the files, so that the user can refer to a protocol for the execution of the program :


I) WORD LISTS (`TXTGRD2XML_monotire-monoxml.py`)
     Instructions
     
 1- before launching, please make sure that your input is in one directory only
 
 2- Enter the work directory (where the inputs are)
 
 3- Enter the .TextGrid name WITHOUT the extension for variables consistency
 
 4- The programm assumes that textgrid and audio files bear the same name. If not, you have to change the file name in the output HEADER
 
 5- the linguistic input originate from 3 files :
     - my_file.wav (audio file)
     
     - my_file.TextGrid ; see below
     
               * the Textgrid file requires two tiers (numitem and comment),   
               but it can accept other tiers, although they will simply be ignored
               
               * numitem formats are imposed : start with d (decimal), plus (optionally) "_" followed 
               with any number of ASCII characters
               
      - liste_1616_lemmes.txt : a tab-separated .txt file which contains the lexical information for each item  present in textgrid 'numitem' slot.
               
 6- the xml in the output does not contain any markup as to which viewing option is assumed because it depends on the formalism of the destination website
 and should therefore be added by the Pangloss team (the two first lines of an xml, usually).

II) SENTENCES (`TXTGRD2XML_multitires-monoxml.py`)

  Instructions
  
 1- before launching, please make sure that your input is in one directory only
 
 2- Enter the work directory (where the inputs are)
 
 3- Enter the .TextGrid name WITHOUT the extension for variables consistency
 
 3- The programm assumes that textgrid and audio files bear the same name. 
 
If not, you have to change the file name in the output HEADER

 4- the linguistic input originate from one file : the .TextGrid 
 
           * the .Textgrid file requires 3 tiers (numitem, surface phonol, gloss),
           but it can accept other tiers, such as phonetic, ENGLISH, FRENCH, CHINESE, tone pattern
           
           * numitem formats are imposed : start with d (decimal), plus (optionally) "_" followed
           with any number of ASCII characters
           
 5- the xml in the output does not contain any markup as to which viewing option is assumed because it depends on the formalism of the destination website and should therefore be added by the Pangloss team (the two first lines of an xml, usually).

III) WORD LISTS AND SENTENCES



# Copyright
Copyright © 2020–21 Maxime Fily maxime.fily@gmail.com

This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
