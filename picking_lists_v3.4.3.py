'''THIS CODE WORKS UNDER ASSUMPTIONS THAT:
1. AP ARE REPLICAS OF SOURCE PLATE AND CONTROL PLATES,
2. THE NUMBER OF WELLS PROCESSED
IN ASSAY PLATE IS ALWAYS EQUAL TO NON-EMPTY WELLS OF CONTROL PLATE,
3. EVERY CONTROL PLATE HAS THE SAME COMPOUNDS IN THE SAME WELLS AND
4. EMPTY WELLS OF THE COMPOUND PLATE ARE ALSO "DISPENSED" INTO ONE OF THE WELLS IN THE ASSAY PLATE

ESSENTIALLY IT WORKS FOR ALL THE "REPLICA" SCENARIOS OF THE SCREENING PROTOCOLS

!FOR NOW ONLY TESTED ON 384 against 384 AND 96 plates!!!

'''

################# Import pip ############################
import pip


####################Import stuff from other scripts#############################
from pyqt_test5 import Grid
from pyqt_test5 import generate_grid

################# Install packages if not already installed ###########
#######################################################################
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])


import_or_install("varname")
import_or_install("csv")
import_or_install("math")
import_or_install("ctypes")
import_or_install("thinter")



################# Import libraries #######################
##########################################################
from varname import nameof
import csv
import math
import ctypes
from collections import defaultdict
from tkinter import messagebox




from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt

################# User-supplied info #####################
##########################################################
#clicked_cells = generate_grid()
#print(clicked_cells)

######### Create a function to display message#########
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

#Create a function that takes csvs as input
def extract_element_from_csv(element_number):
    columnscsv = defaultdict(list)
    with open(input_directory) as f:
        reader = csv.reader(f)
        next(reader)  # skip the header row
        for row in reader:
            # Split the first element of the row on the semicolon delimiter
            first_element = row[0].split(";")[element_number]
            columnscsv[0].append(first_element)
            columnscsv[0] = list(filter(None, columnscsv[0]))

    return columnscsv[0]
    print(columnscsv[0])

# Specify plate layouts. Automatically reformat layouts if user inputs the most frequent plates 384, 96 or 1536-well plates
layout = input("What kind of plates are we using (96, 384, 1536)?")

print(layout)

if layout == "384":
    layout_provisional = [16, 24]
elif layout == "96":
    layout_provisional = [8, 12]
elif layout == "1536":
    layout_provisional = [32, 48]

# Call the mbox function and store the result in a variable
result = messagebox.askyesno('Select wells', 'Do you have a CSV file you want to upload')
# Check the value of the result variable and execute the appropriate code block
if result == True:
    # Code to execute if "OK" is pressed
    input_directory = input("Write directory of the input csv (instead of / you should use \\\\ . For example: C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\input\\input.csv). Click ENTER to use default directory ") or "C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\input\\input.csv"
    ap_control_wells = extract_element_from_csv(0)
    control_control_wells = extract_element_from_csv(1)  # location of controls in assay plate #location of control wells in control plate
    compound_wells_to_be_dispensed = extract_element_from_csv(2)  # Location of compound wells in the compound plates
    orientation = (extract_element_from_csv(14)+extract_element_from_csv(16)+extract_element_from_csv(18))
    volume = (extract_element_from_csv(6))[0]
    total_num_cmpd_source_plates = int((extract_element_from_csv(10))[0])
    total_num_assay_plates= int((extract_element_from_csv(8))[0])
    total_num_control_plates = int((extract_element_from_csv(12))[0])
    pass
else:
    # Code to execute if "Cancel" is pressed
    Mbox('Select wells', 'Select wells that will have controls in the assay plates', 1)
    ap_control_wells = generate_grid(layout_provisional[0], layout_provisional[1])  # location of controls in assay plate
    Mbox('Select wells', 'Select wells that will have controls in control plates', 1)
    control_control_wells = generate_grid(layout_provisional[0], layout_provisional[1])  # location of controls in assay plate #location of control wells in control plate
    Mbox('Select wells', 'Select wells that will have compounds in compound plates', 1)
    compound_wells_to_be_dispensed = generate_grid(layout_provisional[0], layout_provisional[1])  # Location of compound wells in the compound plates
    orientation = input("Write dispensing pattern for control plates, compound plates and assay plates, respectively. r for row-wise and c for column-wise (example: rrr or rrc)")  # dispensing pattern of control plate, compound plate and assay plate (in this order). Values can be "c" for column or "r" for row-wise
    orientation = [f"{x}" for x in orientation]
    volume = input("Write the volume per well to be dispensed in nL ")  # volume to be dispensed
    total_num_cmpd_source_plates = int(input("How many compound source plates? "))  # Total number of compound plates
    total_num_assay_plates = int(input("How many assay plates? "))  # Total number of assay plates
    total_num_control_plates = int(input("How many control plates? "))  # total number of control plates
    pass


output_directory=input("Write the output directory (instead of / you should use \\\\ . For example: C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\csvs")  or "C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\csvs"
print(output_directory)

########### Innitialiseed variables  ################
######################################################
dest_to_num_dict = {ch: i for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ', start=1)}
dest_to_num_dict['AA'] = 27
dest_to_num_dict['AB'] = 28
dest_to_num_dict['AC'] = 29
dest_to_num_dict['AD'] = 30
dest_to_num_dict['AE'] = 31
dest_to_num_dict['AF'] = 32


########### Functions with Formulas ###########
###############################################
def alphanum_to_num(input_strings):
    array_of_converted_wells = []

    total_n_cols = layout[1]

    for input_string in input_strings:
        letters = ""
        numbers = ""
        for char in input_string:
            if char.isdigit():
                numbers += char
            else:
                letters += char

        letters = int(dest_to_num_dict[letters])

        converted_well = ((letters - 1) * int(total_n_cols) + int(numbers))
        array_of_converted_wells.append(converted_well)

    return sorted(array_of_converted_wells)


########### Special function to convert to numeric column-wise. Will be used mostly for the assay well numbers ########
def alphanum_to_num_columnwise(input_strings):
    array_of_converted_wells = []
    rownum=layout[0]
    for input_string in input_strings:
        letters = ""
        numbers = ""
        for char in input_string:
            if char.isdigit():
                numbers += char
            else:
                letters += char

        col_index = int(dest_to_num_dict[letters])
        num = (int(numbers) - 1) * rownum + int(col_index)

        array_of_converted_wells.append(num)
    return sorted(array_of_converted_wells)



############### Expands columns and numbers into wells (transforms A into A1, A2, A3 etc... and 1 into A1, B1, C1 etc...)
def expand_columns_and_rows(list_to_expand):
    # create empty lists to store the numerical, alphabetical, and alphanumeric strings
    numerical_strings = []
    alphabetical_strings = []
    alphanumeric_strings = []

    # iterate through the list of strings
    for s in list_to_expand:
        # check if the string is numerical
        if s.isnumeric():
            numerical_strings.append(s)
        # check if the string is alphabetical
        elif s.isalpha():
            alphabetical_strings.append(s)
        # if it's not numerical or alphabetical, it must be alphanumeric
        else:
            alphanumeric_strings.append(s)

    # create an empty list to store the resulting strings
    result = []
    if layout == [16, 24]:
        alphabet = 'ABCDEFGHIJKLMNOP'
    if layout == [8, 12]:
        alphabet = 'ABCDEFGH'
    # iterate over the numbers in the numerical_strings list
    for num in numerical_strings:
        # iterate over the letters of the alphabet
        for letter in alphabet:
            # concatenate the number and letter and add them to the result list
            result.append(letter + (num))

    for let in alphabetical_strings:
        for number in range(1, layout[1] + 1):
            # concatenate the number and letter and add them to the result list
            result.append(str(let) + str(number))

    result = result + alphanumeric_strings
    return list(dict.fromkeys(result))


############### Convert numeric to alphanumeric ################
def numeric_to_alphanumeric(numeric, which_plate, canonical):
    ###### Extract orientation of dispensing #####
    if which_plate == "control":
        orientation_internal = orientation[0]
    if which_plate == "compound":
        orientation_internal = orientation[1]
    if which_plate == "assay":
        orientation_internal = orientation[2]
    if canonical == "True":  # This is added for when I want to force the orientation to be row-wise independently from the plate type
        orientation_internal = "r"

    total_number_rows = layout[0]
    total_number_columns = layout[1]

    if orientation_internal == "c":
        letter = numeric % layout[0]
        if letter == 0:
            letter = total_number_rows
        else:
            letter = numeric % layout[0]
        number_internal = int((numeric - letter + total_number_rows) / total_number_rows)

    if orientation_internal == "r":
        letter = numeric / total_number_columns
        letter = int(math.ceil(letter))
        number_internal = numeric - ((letter - 1) * total_number_columns)

    #Add zero to the numbers less than 10 (e.g. A2 will become A02 but A10 will stay A10
    #if number_internal < 10:
     #   number_internal = str("0")+str(number_internal)

    letter = ([key for key in dest_to_num_dict.keys()][letter - 1])
    return str((str(letter) + str(number_internal)))


################# Processed user-supplied info #####################
##########################################################
if layout == "384":
    layout = [16, 24]
elif layout == "96":
    layout = [8, 12]
elif layout == "1536":
    layout = [32, 48]

# Convert wells where controls should go to numeric values
ap_control_wells = (expand_columns_and_rows(ap_control_wells))  # Expands columns and rows
if orientation[2]=="r":
    ap_control_wells_numeric = alphanum_to_num(ap_control_wells)  # Convert wells where controls should go to numeric values
if orientation[2]=="c":
    ap_control_wells_numeric = alphanum_to_num_columnwise(ap_control_wells)

print("here")
print(control_control_wells)
# Where the control wells are located:
control_control_wells = (expand_columns_and_rows(control_control_wells))
print(control_control_wells)
if orientation[0]=="r":
    control_control_wells_numeric = alphanum_to_num(control_control_wells)
if orientation[0]=="c":
    control_control_wells_numeric = alphanum_to_num_columnwise(control_control_wells)
print(control_control_wells_numeric)


#Which are the compound wells to be dispensed in the compound plate
compound_wells_to_be_dispensed_expanded = (expand_columns_and_rows(compound_wells_to_be_dispensed))
if orientation[1]=="r":
    compound_wells_to_be_dispensed_expanded = alphanum_to_num(compound_wells_to_be_dispensed_expanded)
if orientation[1]=="c":
    compound_wells_to_be_dispensed_expanded = alphanum_to_num_columnwise(compound_wells_to_be_dispensed_expanded)


#Which are the compound wells to be dispensed (difference of all wells minus the ap_control_wells_numeric)
compound_wells_in_ap = [i for i in range(1, (layout[0]*layout[1])+1)]
compound_wells_in_ap =  [x for x in compound_wells_in_ap if x not in ap_control_wells_numeric]

########### Innitialiseed variables  ################
######################################################
dest_to_num_dict = {ch: i for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ', start=1)}
dest_to_num_dict['AA'] = 27
dest_to_num_dict['AB'] = 28
dest_to_num_dict['AC'] = 29
dest_to_num_dict['AD'] = 30
dest_to_num_dict['AE'] = 31
dest_to_num_dict['AF'] = 32

############## Variables Setting ############################
#############################################################
# Calculate wells per plate by multiplying total number of cols and rows
wells_per_plate = layout[0] * (layout[1])  # How many wells in total in each plate

# Calculate total number of assay wells that will be surveyed. It doesnt depend on the amount of empty wells. Each well will be queried and if its supposed to be empty, it will be skipped
total_assay_wells = total_num_assay_plates * wells_per_plate
print(total_assay_wells)

################ Counters #####################################
###############################################################
used_cp_wells = 1

used_cp = 1

used_ap_wells = 1

used_ap = 1

used_control_wells = 1

used_control_plates = 1

#####################################LOOP###################################
############################################################################
with  open('{}\\controls.csv'.format(output_directory), "w") as controls_csv:
    controls_csv.write("sep=,\n")

    ########################### Enter the loop #############################################
    for j in range(0, total_assay_wells):
        if used_ap_wells in ap_control_wells_numeric:
            current_control_well_to_use=control_control_wells_numeric[0]
            print("Controls" + str(used_control_plates) + "," + str(numeric_to_alphanumeric(current_control_well_to_use, "control", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False")))
            print("Controls" + str(used_control_plates) + "," + str(current_control_well_to_use) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume) + "," + str(used_ap_wells))
            controls_csv.write("Controls" + "," + str(numeric_to_alphanumeric(current_control_well_to_use, "control", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False") + "\n"))

            if len(control_control_wells_numeric) == 1:
                control_control_wells_numeric.pop(0)
                if orientation[0]=="r":
                    control_control_wells_numeric = alphanum_to_num(control_control_wells)
                if orientation[0] == "c":
                    control_control_wells_numeric = alphanum_to_num_columnwise(control_control_wells)
            else:
                control_control_wells_numeric.pop(0)

        if used_ap_wells % wells_per_plate == 0:
            used_ap += 1
            used_ap_wells = 0
            used_control_plates += 1
            used_control_wells = 0

        if used_control_plates>total_num_control_plates:
            used_control_plates = 1
            used_control_wells = 0

        used_control_wells += 1
        used_ap_wells += 1


################ Counters #####################################
###############################################################
used_cp_wells = 1

used_cp = 1

used_ap_wells = 1

used_ap = 1

used_control_wells = 1

used_control_plates = 1
with  open('{}\\compound.csv'.format(output_directory), "w") as compound_csv:
    compound_csv.write("sep=,\n")
    ########################### Enter the loop #############################################
    for j in range(0, total_assay_wells):
        if used_ap_wells in compound_wells_in_ap:
            current_compound_well_to_use=compound_wells_to_be_dispensed_expanded[0]
            print("CP[" + str(used_cp) + "]," + str(numeric_to_alphanumeric(current_compound_well_to_use, "compound", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False")))
            print("CP[" + str(used_cp) + "]," + str(current_compound_well_to_use) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume) + "," + str(used_ap_wells))
            compound_csv.write("CP[" + str(used_cp) + "]," + str(numeric_to_alphanumeric(current_compound_well_to_use, "compound", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False") + "\n"))

            if len(compound_wells_to_be_dispensed_expanded) == 1:
                compound_wells_to_be_dispensed_expanded.pop(0)
                compound_wells_to_be_dispensed_expanded = (expand_columns_and_rows(compound_wells_to_be_dispensed))
                if orientation[1] == "r":
                    compound_wells_to_be_dispensed_expanded = alphanum_to_num(compound_wells_to_be_dispensed_expanded)
                if orientation[1] == "c":
                    compound_wells_to_be_dispensed_expanded = alphanum_to_num_columnwise(compound_wells_to_be_dispensed_expanded)
            else:
                compound_wells_to_be_dispensed_expanded.pop(0)

        if used_ap_wells % wells_per_plate == 0:
            used_ap += 1
            used_ap_wells = 0
            used_cp += 1
            used_cp_wells = 0



        used_cp_wells += 1
        used_ap_wells += 1

def delete_first_line_csv(filename):
    with open(filename, "r") as file:
        # read the file as a list of lines
        lines = file.readlines()

    # remove the first line from the list of lines
    lines = lines[1:]

    with open(filename, "w") as file:
        # write the remaining lines to the file
        file.writelines(lines)


delete_first_line_csv('{}\\controls.csv'.format(output_directory))
delete_first_line_csv('{}\\compound.csv'.format(output_directory))