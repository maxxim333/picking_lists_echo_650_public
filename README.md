# picking_lists_public
Script to automatically generate picking lists for Echo 650 Acoustic Liquid Dispenser


## Purpose
We have an automated Echo 650 protocol, combined with a robotic arm, that dispenses liquid from Control and Compound plates into an assay plate. In order to function, the process needs a picking lists with exact instructions of how to dispense each liquid from/to where and how much. This script is designed to work with standard plates of library of compounds, so for example, when working with 384 compound libraries plates, compounds are located in every well except those in columns 1,2,23 and 24.

This script is designed to make the generation of picking lists as flexible and as easy as possible.

## What is needed:
·Python3.10. 

·Pip package installer: The code already contains the instruction to check if necessary libraries exist and if not, it installs them via pip

·All the files from this repository

## Versions
#picking_lists_v3.4.3

This is the "simplified" version. It assumes a variety of things:
1. You have only one type of controls
2. All the plates are the same format (either all 96 or all 384)
3. There are as many assay/destination plates as there are compound plates
4. The sum of control and compound wells in the assay plates must be equal to the total number of wells in the plate. In other words, something has to be dispensed in every well.
5. All the volumes to be dispensed are the same

Usage:
1. Launch script with python3.10. When launched for the first time, it will take a while since it will be installing libraries necessary for it to work.
2. User input will be asked where you have to write which kind of plates you are working with. Write and press ENTER
3. A window "Select Wells" will appear. It will ask you wether you want to manually give instruction to the script or you can upload a CSV file with instruction

3a. If you want to use the CSV version, use the "input.csv" file as template just change what is needed to be changed, save the file and press "Yes" in the "Select Wells" window.

3b. If you want to manually set up the conditions, press "No". Three windows will appear asking you to 1 - select where are the controls well located in the assay plate; 2 - Where are the control wells located in the control plate; 3 - where are compounds supposed to be located in the destinaion plate. Then, in the script will also ask you to provide the dispensing pattern (row-wise or column wise); an input of 3 letters is needed, corresponding to the dispensing pattern of control, compound and assay plates. For example, "rrr" means row-wise for every plate. This doesnt affect much of anything so if you are confused just write "rrr" here. Next thing it will ask you is the volume in nL to be dispensed. Write and press ENTER. It will ask you for the total number of compound, assay and control plates.

4. The code is pretty much done. Now the last thing the script will ask you is the output directory. If you are using windows, remember to use double backslash (\\) instead of /.
5. The script should generate two CSV files, one for dispensing instructions of controls and another for compounds.


#picking_lists_v4.3.3.
This is the "Full" version. Works with any type of dispensing logic and plate layouts. 
1. Asks you for plate formats, of control, compound and destination plates.
2. Asks you if you have a CSV input file. Uses the "input4_dif_vol.csv" as input.
3. If you want to introduce all the variables manually, click "No" when asked if there is a CSV input file
4. Select wells where negative controls will go in the assay plates
5. Select wells where control 1 and control 2 will go in assay plates (two separate prompt windows will appear for each control). You can also click ENTER without selecting anything.
6. Same thing for the contol plate. Show the programs where each of the controls are located in the control plate
7. Select the wells of the COMPOUND plate that contain compounds
8. Write the dispensing pattern (rrr,ccc,ccr,rrc etc...)
9. Write the volume per well OF THE NEGATIVE CONTROLS to be dispensed in nL 
10. Write the volume per well OF THE CONTROL 1 to be dispensed in nL
11. Write the volume per well OF THE CONTROL 2 to be dispensed in nL 
12. Write the volume per well OF THE COMPOUNDS to be dispensed in nL 
13. Write how many compound plates there are
14. Write how many assay plates there are
15. Write how many control plates there are
16. Write output directory. If you are using windows, remember to use double backslash (\\) instead of /.
