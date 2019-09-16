################### Genetic Algorithm for protien structures: Version 0.1 alpha ###########################
    
    This program finds the fitness of a chromosome represented as a string of 'h' and 'p' characters
    Input files are provided.  They demonstrate how a file should be setup to be used by the program

    To run: 
        1. Download
        2. run main.py
        3. requires Python 3+
        4. requires tkinter library
            
    Features:
     1. Text Field "File Name": box to input the data file to analyze (requires full path)
     2. Text Field "Custom Seq": Not operational at this point (supposed to let the user enter a custom sequence)
     3. Button "Load File": loads the file from the "File name" field text
     4. Button "Load Custom": Not operational at this point (load in custom sequences)
     5. ProgressBar: Extremely buggy. (chopped out of production due to time constraints)
     6. Text display box: Displays the statistics of the current chromosome 
     7. Buttons "Next" & "Prev": move to the next/previous chromosome loaded into the program
     8. Parameter dropdown menus: customize the algorithm by setting the parameters
     9. Button "Write solutions to file": writes the stats and order of the chromosome to a file
     10. Button "Run Algorithm": Finds the best fitness (that it can) using the dropdown parameters
     11. Structure canvas: Draws the protein structure on the screen

     Disclaimer:
     **This project is an infant and is loaded with bugs and logic that is just waiting to be optimized

    Bugs/Issues: (There are a lot of them)
        1. Two places in the algorithm where Value Errors occur for an unknown reason (caught with exception handling)
        2. The Process bar is not working  correctly anc stops functioning while processes are still working
        3. Not mullti-threaded so nothing is responsive while the algorithm is running
        4. The text display does not refresh properly after the algorithm has run.  The user has to move to a different 
            chromosomes and return for all of the data to appear
        5. The runtime is slow
        6. The fitness threshold is rarely found.  (Disapointing but out of time)
        7. Ocasionally the tail end of the chromosome has an imposible mutation.  It is a bug in the logic due to lack of
            testing (diagonal connection)
        8. The text display box can be altered with the keyboard
        9. some features not setup
        **There are probably many more

    Latest Version of code can be found on GitHub:
        https://github.com/ResoTheRed/Genetic_Algorithm_Protein_Structures
