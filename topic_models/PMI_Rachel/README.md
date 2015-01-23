Help and TODOs for pmi.py
==========================

In its most basic form, pmi.py takes a directory and an argument (c for create and r for read). The argument
c creates the word dictionary and matrix.

To run for creating the word dictionary and matrix: python pmi.py c --input\_path path\_to\_directory --output\_path path\_for\_output   
To run for loading the word dictionary and matrix for pmi calcs:   
   python pmi.py r --word\_dict path\_to\_dict --word\_matrix path\_to\_matrix

Current arguments are as follows (type pmi.py --help at the command line):
---------------------------------------------------------------------------

* 'action' : choices = ['c', 'r'], Creating a matrix: c, Reading a matrix: 'r'. This is a required argument.   
* '--input\_path' : The directory where the corpora files are located. This is required for an action of 'c'   
* '--output\_path' : Specifies the output path for the output files. Default is the current working directory. Can be used with 'r' and 'c' actions.   
* '--remove\_stopwords' : choices = ['y', 'n'], Choose to keep or remove stopwords when parsing the text. Default is 'y'   
* '--word\_dict' : The complete path for the word dictionary file. Required when using the 'r' action.   
* '--word\_matrix' : The complete path for the word matrix file, required when using the 'r' action.    
* '--topic\_words' : A string of the topic words that should be enclosed in double quotes and separated by spaces, required when using the 'r' action.   
* '--s' : An integer that represents the number of words that the windows moves by when creating the word matrix. Default is 1.   

Notes
====================================

The corpora\_matrix.py file has two commented lines. These are used for testing the creation of the matrix without having
to wait for all the code to run.

TODOs
==============================

1. ~~Create a command line argument for an optional output directory for the serialized word dictionary.~~ DONE
2. ~~Create a command line argument for an optional output directory for the serialized word matrix.~~ DONE
3. Create a command line argument for specifying an optional stopwords file.
4. ~~Create the code for deserializing the matrix and dictionary files.~~ DONE
5. ~~Create the code for the reading in the topic keys and the appropriate command line arguments.~~ DONE
6. ~~Create the code for computing the pmi for each topic keys word pair (make sure to handle the reverse of the word pair
   as well as the case where the word pair is not in the word matrix or dictionary)~~ DONE
7. ~~Create the code for computing the median pmi for a topic (this could be optional)~~ DONE
8. ~~Create a command line argument for an optional output directory for the pmi calculations.~~ DONE
9. Add error messaging for optional input arguments.
