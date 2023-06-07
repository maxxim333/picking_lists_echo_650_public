'''THIS CODE WORKS UNDER ASSUMPTIONS THAT:
3. EVERY CONTROL PLATE HAS THE SAME COMPOUNDS IN THE SAME WELLS AND
4. EMPTY WELLS OF THE COMPOUND PLATE ARE ALSO "DISPENSED" INTO ONE OF THE WELLS IN THE ASSAY PLATE

'''

################# Import pip ############################
import pip


################# Install packages if not already installed ###########
#######################################################################
def import_or_install(package): #Function that searches for a package and  installs it if doesnt exist
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


####################Import stuff from other scripts#############################
from pyqt_test5 import Grid
from pyqt_test5 import generate_grid


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


################# User-supplied info #####################
###########################################################
# Specify plate layouts. Automatically reformat layouts if user inputs the most frequent plates 384, 96 or 1536-well plates
layout_ap = input("What kind of Assay Plates are we using (96, 384, 1536)?")
layout_cp = input("What kind of Compound Plates are we using (96, 384, 1536)?")
layout_control = input("What kind of Control Plates are we using (96, 384, 1536)?")

################# Processed user-supplied info #####################
##########################################################
#Reprocess layout
if layout_ap == "384":
    layout_ap = [16, 24]
elif layout_ap == "96":
    layout_ap = [8, 12]
elif layout_ap == "1536":
    layout_ap = [32, 48]

if layout_cp == "384":
    layout_cp = [16, 24]
elif layout_cp == "96":
    layout_cp = [8, 12]
elif layout_cp == "1536":
    layout_cp = [32, 48]

if layout_control == "384":
    layout_control = [16, 24]
elif layout_control == "96":
    layout_control = [8, 12]
elif layout_control == "1536":
    layout_control = [32, 48]


# Call the mbox function and store the result in a variable
result = messagebox.askyesno('Select wells', 'Do you have a CSV file you want to upload')
# Check the value of the result variable and execute the appropriate code block
if result == True:
    # Code to execute if "OK" is pressed
    input_directory = input("Write directory of the input csv (instead of / you should use \\\\ . For example: C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\input\\input4_dif_vol.csv). Click ENTER to use default directory ") or "C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\input\\input4_dif_vol.csv"
    ap_control_wells_negative = extract_element_from_csv(0)  # location of controls in assay plate
    ap_control_wells_control1 = extract_element_from_csv(1)  # Where the "first type of control has to go in the assay plates
    ap_control_wells_control2 = extract_element_from_csv(2)  # Whee the second type of controls has to go in the assay plates
    control_control_wells_negative = extract_element_from_csv(3)  # Where are negative controls located in the control plates
    control_control_wells_control1 = extract_element_from_csv(4)  # Where are controls of type 1 located in the control plates
    control_control_wells_control2 = extract_element_from_csv(5)  # Where are controls of type 2 located in the control plates
    compound_wells_to_be_dispensed = extract_element_from_csv(6)  # Location of compound wells in the compound plates
    print(compound_wells_to_be_dispensed)
    orientation = (extract_element_from_csv(12)[14]+extract_element_from_csv(12)[16]+extract_element_from_csv(12)[18])  # dispensing pattern of control plate, compound plate and assay plate (in this order). Values can be "c" for column or "r" for row-wise
    volume_neg_control = extract_element_from_csv(12)[6] # volume to be dispensed
    volume1 = extract_element_from_csv(13)[1]  # volume to be dispensed
    volume2 = extract_element_from_csv(14)[1]  # volume to be dispensed
    volume_compuestos = extract_element_from_csv(15)[1]  # volume to be dispensed


    total_num_cmpd_source_plates = int(extract_element_from_csv(12)[10])  # Total number of compound plates
    total_num_assay_plates = int(extract_element_from_csv(12)[8])  # Total number of assay plates
    total_num_control_plates = int(extract_element_from_csv(12)[12]) # total number of control plates
    pass

else:
    # Code to execute if "No" is pressed
    Mbox('Select wells', 'Select wells that will have negative controls in the assay plates', 1)
    ap_control_wells_negative = generate_grid(layout_ap[0], layout_ap[1])  # location of controls in assay plate
    Mbox('Select wells', 'Select wells that will have Control Type 1 in the assay plates', 1)
    ap_control_wells_control1 = generate_grid(layout_ap[0], layout_ap[1]) #Where the "first type of control has to go in the assay plates
    Mbox('Select wells', 'Select wells that will have Control Type 2 in the assay plates', 1)
    ap_control_wells_control2 = generate_grid(layout_ap[0], layout_ap[1]) # Whee the second type of controls has to go in the assay plates

    Mbox('Select wells', 'Select wells that will have negative controls in the control plates', 1)
    control_control_wells_negative = generate_grid(layout_control[0], layout_control[1]) #Where are negative controls located in the control plates
    Mbox('Select wells', 'Select wells that will Controls Type 1 in the control plates', 1)
    control_control_wells_control1 = generate_grid(layout_control[0], layout_control[1]) #Where are controls of type 1 located in the control plates
    Mbox('Select wells', 'Select wells that will Controls Type 2 in the control plates', 1)
    control_control_wells_control2 = generate_grid(layout_control[0], layout_control[1]) #Where are controls of type 2 located in the control plates

    Mbox('Select wells', 'Select wells that will contain COMPOUNDS in the COPMPOUND plate', 1)
    compound_wells_to_be_dispensed = generate_grid(layout_cp[0], layout_cp[1])  # Location of compound wells in the compound plates

    orientation = input("Write dispensing pattern for control plates, compound plates and assay plates, respectively. r for row-wise and c for column-wise (example: rrr or rrc)")  # dispensing pattern of control plate, compound plate and assay plate (in this order). Values can be "c" for column or "r" for row-wise
    orientation = [f"{x}" for x in orientation]


    volume_neg_control = input("Write the volume per well OF THE NEGATIVE CONTROLS to be dispensed in nL ")  # volume to be dispensed
    volume1 = input("Write the volume per well OF THE CONTROL 1 to be dispensed in nL ")  # volume to be dispensed
    volume2 = input("Write the volume per well OF THE CONTROL 2 to be dispensed in nL ")  # volume to be dispensed
    volume_compuestos = input("Write the volume per well OF THE COMPOUNDS to be dispensed in nL ")  # volume to be dispensed


    total_num_cmpd_source_plates = int(input("How many compound source plates? "))  # Total number of compound plates
    total_num_assay_plates = int(input("How many assay plates? "))  # Total number of assay plates
    total_num_control_plates = int(input("How many control plates? "))  # total number of control plates
    pass

output_directory=input("Write the output directory (instead of / you should use \\\\ . For example: C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\csvs")  or "C:\\Users\\mvaskin\\PycharmProjects\\pickinglists\\csvs"

#ap_control_wells_negative=["9"] #Where the negative controls have to go in the assay plates
#ap_control_wells_control1=["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"] #Where the "first type of control has to go in the assay plates
#ap_control_wells_control2=["I1", "J1", "K1", "L1", "M1", "N1", "O1", "P1"] #Whee the second type of controls has to go in the assay plates
ap_control_wells = ap_control_wells_negative+ap_control_wells_control1+ap_control_wells_control2  # location of controls in assay plate
print(ap_control_wells)

#control_control_wells_negative=["A11", "A12"] #Where are negative controls located in the control plates
#control_control_wells_control1=["B"] #Where are controls of type 1 located in the control plates
#control_control_wells_control2=["C"] #Where are controls of type 2 located in the control plates
control_control_wells = control_control_wells_negative+control_control_wells_control1+control_control_wells_control2 #location of control wells in control plate
print(control_control_wells)

#compound_wells_to_be_dispensed=["1","2", "3", "4", "5", "6", "7", "8", "9", "10", "11"] #Location of compound wells in the compound plates


#orientation = ["c", "c", "r"]  # dispensing pattern of control plate, compound plate and assay plate (in this order). Values can be "c" for column or "r" for row-wise

#volume = 30  # volume to be dispensed



#total_num_cmpd_source_plates = 9  # Total number of compound plates

#total_num_assay_plates = 9  # Total number of assay plates

#total_num_control_plates = 2  # total number of control plates


########### Innitialiseed variables  ################
######################################################
#This dictionary will be used for the function of alphanumeric to numeric conversion
dest_to_num_dict = {ch: i for i, ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ', start=1)}
dest_to_num_dict['AA'] = 27
dest_to_num_dict['AB'] = 28
dest_to_num_dict['AC'] = 29
dest_to_num_dict['AD'] = 30
dest_to_num_dict['AE'] = 31
dest_to_num_dict['AF'] = 32


########### Functions with Formulas ###########
###############################################
def alphanum_to_num(input_strings, which_plate): #This function converts alphanumeric well notation to numeric one, assuming row-wise order (A1 is 1, A2 is 2). Takes as input the well itself and which plate it belongs to. The plate it belongs to is important to infer the layout and therefore the numeration of wells
    array_of_converted_wells = []

    if which_plate == "assay":
        layout = layout_ap
    if which_plate == "compound":
        layout = layout_cp
    if which_plate == "control":
        layout = layout_control

    total_n_cols = layout[1] #total number of columns is inferred from plate layout that is itself inferred from user-supplied "which_plate" variable

    for input_string in input_strings:
        letters = ""
        numbers = ""
        for char in input_string: #Separate each well notation into numerical and alphabetical characters. Adds every alphabetical character to newly created variable "letters" and digital characters to "numbers"
            if char.isdigit():
                numbers += char
            else:
                letters += char

        letters = int(dest_to_num_dict[letters]) #Convert letters to numbers following the value/key pairs of dest_to_num_dict dictionary

        converted_well = ((letters - 1) * int(total_n_cols) + int(numbers)) #This formula gives the number of well
        array_of_converted_wells.append(converted_well)

    return sorted(array_of_converted_wells)


########### Special function to convert to numeric column-wise. Will be used mostly for the assay well numbers ########
def alphanum_to_num_columnwise(input_strings, which_plate): #This is mostly the same as alphanum_to_num function but the formula in the end is different
    array_of_converted_wells = []

    if which_plate == "assay":
        layout = layout_ap
    if which_plate == "compound":
        layout = layout_cp
    if which_plate == "control":
        layout = layout_control

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
def expand_columns_and_rows(list_to_expand, which_plate):
    # create empty lists to store the numerical, alphabetical, and alphanumeric strings. Takes as argument the list of strings to expand and which plate they belong to (to know the layout and therefore number of columns and rows)
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

    #Define the alphabet which will depend on the amount of rows, which in turn depends on which plate we are talking about
    if which_plate == "assay":
        layout = layout_ap
        if layout_ap == [16, 24] or layout_ap == [32, 48]:
            alphabet = 'ABCDEFGHIJKLMNOP'
            if layout_ap == [32, 48]:
                alphabet = alphabet + 'QRSTUVWXYZ!$%&+*'
        if layout_ap == [8, 12]:
            alphabet = 'ABCDEFGH'

    if which_plate == "compound":
        layout = layout_cp
        if layout_cp == [16, 24] or layout_cp == [32, 48]:
            alphabet = 'ABCDEFGHIJKLMNOP'
            if layout_cp == [32, 48]:
                alphabet = alphabet + 'QRSTUVWXYZ!$%&+*'
        if layout_cp == [8, 12]:
            alphabet = 'ABCDEFGH'

    if which_plate == "control":
        layout = layout_control
        if layout_control == [16, 24] or layout_control == [32, 48]:
            alphabet = 'ABCDEFGHIJKLMNOP'
            if layout_control == [32, 48]:
                alphabet = alphabet + 'QRSTUVWXYZ!$%&+*'
        if layout_control == [8, 12]:
            alphabet = 'ABCDEFGH'

    # iterate over the numbers in the numerical_strings list. It appends each letter of the alphabet to each number in the list of strings
    for num in numerical_strings:
        # iterate over the letters of the alphabet
        for letter in alphabet:
            # concatenate the number and letter and add them to the result list
            result.append(letter + (num))

    #This is the other way around: for each letter in the list of string, append numbers from 1 to whatever the number of columns is
    for let in alphabetical_strings:
        for number in range(1, layout[1] + 1):
            # concatenate the number and letter and add them to the result list
            result.append(str(let) + str(number))

    result = result + alphanumeric_strings
    result = [string.replace("!", "AA").replace("$", "AB").replace("%", "AC").replace("&", "AD").replace("+", "AE").replace("*", "AF") for string in result]
    return list(dict.fromkeys(result))

############### Convert numeric to alphanumeric ################
def numeric_to_alphanumeric(numeric, which_plate, canonical): #Canonical = True forces to interpret dispensing as row-wise, independently of previously user-supplied orientation values
    ###### Extract orientation of dispensing #####
    if which_plate == "control":
        orientation_internal = orientation[0]
        layout=layout_control
    if which_plate == "compound":
        orientation_internal = orientation[1]
        layout = layout_cp
    if which_plate == "assay":
        orientation_internal = orientation[2]
        layout = layout_ap
    if canonical == "True":  # This is added for when I want to force the orientation to be row-wise independently from the plate type. Mostly unused legacy line.
        orientation_internal = "r"

    total_number_rows = layout[0]
    total_number_columns = layout[1]

    if orientation_internal == "c": #If dispensing is column-wise, do this:
        letter = numeric % layout[0]
        if letter == 0:
            letter = total_number_rows
        else:
            letter = numeric % layout[0]
        number_internal = int((numeric - letter + total_number_rows) / total_number_rows)

    if orientation_internal == "r": #If dispensing is row-wise, do this:
        letter = numeric / total_number_columns
        letter = int(math.ceil(letter))
        number_internal = numeric - ((letter - 1) * total_number_columns)

    if number_internal < 10: #This line is needed to add 0 in front of a number, which is the right input for ECHO (i.e. A01 instead of "A1").
        number_internal = str("0")+str(number_internal)

    letter = ([key for key in dest_to_num_dict.keys()][letter - 1])
    return str((str(letter) + str(number_internal)))




# Expand and convert wells where controls should go to numeric values
ap_control_wells = (expand_columns_and_rows(ap_control_wells, "assay"))  # Expands columns and rows
if orientation[2]=="r":
    ap_control_wells_numeric = alphanum_to_num(ap_control_wells, "assay")  # Convert wells where controls should go to numeric values
if orientation[2]=="c":
    ap_control_wells_numeric = alphanum_to_num_columnwise(ap_control_wells, "assay")

#Expand and convert list of where the control wells are located:
control_control_wells = (expand_columns_and_rows(control_control_wells, "control"))
if orientation[0]=="r":
    control_control_wells_numeric = alphanum_to_num(control_control_wells, "control")
if orientation[0]=="c":
    control_control_wells_numeric = alphanum_to_num_columnwise(control_control_wells, "control")

#Expand and convert the list of which are the compound wells to be dispensed in the compound plate
compound_wells_to_be_dispensed_expanded = (expand_columns_and_rows(compound_wells_to_be_dispensed, "compound"))
if orientation[1]=="r":
    compound_wells_to_be_dispensed_expanded = alphanum_to_num(compound_wells_to_be_dispensed_expanded, "compound")
if orientation[1]=="c":
    compound_wells_to_be_dispensed_expanded = alphanum_to_num_columnwise(compound_wells_to_be_dispensed_expanded, "compound")

#Create a fixed expanded and converted list of which compounds wells are to be dispensed in the compound plate
#This is needed because further down in the loop, the list compound_wells_to_be_dispensed_expanded will be iteratively changed but the original list is still needed
compound_wells_to_be_dispensed_expanded_fixed=(expand_columns_and_rows(compound_wells_to_be_dispensed, "compound"))
if orientation[1]=="r":
    compound_wells_to_be_dispensed_expanded_fixed = alphanum_to_num(compound_wells_to_be_dispensed_expanded_fixed, "compound")
if orientation[1]=="c":
    compound_wells_to_be_dispensed_expanded_fixed = alphanum_to_num_columnwise(compound_wells_to_be_dispensed_expanded_fixed, "compound")

#Which are the compound wells to be dispensed (difference of all wells minus the ap_control_wells_numeric). These are different from the compound_wells_to_be_dispensed_expanded because it ignores the fact that there are empty wells
compound_wells_in_ap = [i for i in range(1, (layout_ap[0]*layout_ap[1])+1)]
compound_wells_in_ap =  [x for x in compound_wells_in_ap if x not in ap_control_wells_numeric]

#Since there are 3 types of control wells, i need to expand and rename them all.  I need to do this for the wells from CONTROL plate and AP
ap_control_wells_negative = (expand_columns_and_rows(ap_control_wells_negative, "assay"))
ap_control_wells_control1 = (expand_columns_and_rows(ap_control_wells_control1, "assay"))
ap_control_wells_control2 = (expand_columns_and_rows(ap_control_wells_control2, "assay"))
if orientation[2]=="r":
    ap_control_wells_negative_numeric = alphanum_to_num(ap_control_wells_negative, "assay")
    ap_control_wells_control1_numeric = alphanum_to_num(ap_control_wells_control1, "assay")
    ap_control_wells_control2_numeric = alphanum_to_num(ap_control_wells_control2, "assay")
if orientation[2]=="c":
    ap_control_wells_negative_numeric = alphanum_to_num_columnwise(ap_control_wells_negative, "assay")
    ap_control_wells_control1_numeric = alphanum_to_num_columnwise(ap_control_wells_control1, "assay")
    ap_control_wells_control2_numeric = alphanum_to_num_columnwise(ap_control_wells_control2, "assay")

control_control_wells_negative = (expand_columns_and_rows(control_control_wells_negative, "control"))
control_control_wells_control1 = (expand_columns_and_rows(control_control_wells_control1, "control"))
control_control_wells_control2 = (expand_columns_and_rows(control_control_wells_control2, "control"))
if orientation[0]=="r":
    control_control_wells_negative_numeric = alphanum_to_num(control_control_wells_negative, "control")
    control_control_wells_control1_numeric = alphanum_to_num(control_control_wells_control1, "control")
    control_control_wells_control2_numeric = alphanum_to_num(control_control_wells_control2, "control")
if orientation[0]=="c":
    control_control_wells_negative_numeric = alphanum_to_num_columnwise(control_control_wells_negative, "control")
    control_control_wells_control1_numeric = alphanum_to_num_columnwise(control_control_wells_control1, "control")
    control_control_wells_control2_numeric = alphanum_to_num_columnwise(control_control_wells_control2, "control")

########### Innitialiseed variables  ################ #This might be redundant block of code. Didnt delete for stability purposes
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
wells_per_plate = layout_ap[0] * (layout_ap[1])  # How many wells in total in each plate

# Calculate total number of assay wells that will be surveyed. It doesnt depend on the amount of empty wells. Each well will be queried and if its supposed to be empty, it will be skipped
total_assay_wells = total_num_assay_plates * wells_per_plate

################ Counters #####################################
###############################################################
used_cp_wells = 1 #Current well being processed from CP

used_cp = 1 #Current CP being processed

used_ap_wells = 1 #Current well being processed from AP

used_ap = 1 #Current AP being processed

used_control_wells = 1 #Current well being processed from control plate

used_control_plates = 1 #Current control plate being processed


#####################################LOOP###################################
############################################################################
with  open('{}\\controls.csv'.format(output_directory), "w") as controls_csv: #Write here where your control picking list should be
    controls_csv.write("sep=,\n")

    ########################### Enter the loop #############################################
    for j in range(0, total_assay_wells): #Will run the loop J times, J being the total wells given by number of wells per AP multiplied by number of APs.
        if used_ap_wells in ap_control_wells_numeric: #Is the AP well currently being processed in the list of AP wells destined to be used for any of the 3 controls?
            if used_ap_wells in ap_control_wells_negative_numeric: #If yes, is it destined for negative control?
                volume_to_print=volume_neg_control
                current_control_well_to_use=control_control_wells_negative_numeric[0] #Pick the first element from the control_control_wells_negative_numeric list. This is the well from the control plate to be dispensed right now

                if len(ap_control_wells_negative_numeric) == 1: #If this was the last well of current AP destined to control, repopulate the list of wells to be used for control is AP
                    ap_control_wells_negative_numeric.pop(0)
                    if orientation[2] == "r":
                        ap_control_wells_negative_numeric = alphanum_to_num(ap_control_wells_negative, "assay")
                    if orientation[2] == "c":
                        ap_control_wells_negative_numeric = alphanum_to_num_columnwise(ap_control_wells_negative, "assay")
                else:
                    ap_control_wells_negative_numeric.pop(0) #If not, just remove the first element of the list (because this well has just been processed.

                if len(control_control_wells_negative_numeric) == 1: #If this was the last well of current control plate that has negative control well, repopulate the list of negative control wells in the control plate
                    control_control_wells_negative_numeric.pop(0)
                    if orientation[0] == "r":
                        control_control_wells_negative_numeric = alphanum_to_num(control_control_wells_negative, "control")
                    if orientation[0] == "c":
                        control_control_wells_negative_numeric = alphanum_to_num_columnwise(control_control_wells_negative, "control")
                else:
                    control_control_wells_negative_numeric.pop(0)

            #Same as two previous if/else statements but for control 1
            if used_ap_wells in ap_control_wells_control1_numeric:
                volume_to_print = volume1
                current_control_well_to_use = control_control_wells_control1_numeric[0]

                if len(ap_control_wells_control1_numeric) == 1:
                    ap_control_wells_control1_numeric.pop(0)
                    if orientation[2] == "r":
                        ap_control_wells_control1_numeric = alphanum_to_num(ap_control_wells_control1, "assay")
                    if orientation[2] == "c":
                        ap_control_wells_control1_numeric = alphanum_to_num_columnwise(ap_control_wells_control1, "assay")
                else:
                    ap_control_wells_control1_numeric.pop(0)

                if len(control_control_wells_control1_numeric) == 1:
                    control_control_wells_control1_numeric.pop(0)
                    if orientation[0] == "r":
                        control_control_wells_control1_numeric = alphanum_to_num(control_control_wells_control1, "control")
                    if orientation[0] == "c":
                        control_control_wells_control1_numeric = alphanum_to_num_columnwise(control_control_wells_control1, "control")
                else:
                    control_control_wells_control1_numeric.pop(0)

            # Same as two previous if/else statements but for control 2
            if used_ap_wells in ap_control_wells_control2_numeric:
                volume_to_print = volume2
                current_control_well_to_use = control_control_wells_control2_numeric[0]

                if len(ap_control_wells_control2_numeric) == 1:
                    ap_control_wells_control2_numeric.pop(0)
                    if orientation[2] == "r":
                        ap_control_wells_control2_numeric = alphanum_to_num(ap_control_wells_control2, "assay")
                    if orientation[2] == "c":
                        ap_control_wells_control2_numeric = alphanum_to_num_columnwise(ap_control_wells_control2, "assay")
                else:
                    ap_control_wells_control2_numeric.pop(0)

                if len(control_control_wells_control2_numeric) == 1:
                    control_control_wells_control2_numeric.pop(0)
                    if orientation[0] == "r":
                        control_control_wells_control2_numeric = alphanum_to_num(control_control_wells_control2, "control")
                    if orientation[0] == "c":
                        control_control_wells_control2_numeric = alphanum_to_num_columnwise(
                            control_control_wells_control2, "control")
                else:
                    control_control_wells_control2_numeric.pop(0)

            #Write to csv/print
            print("Controls" + str(used_control_plates) + "," + str(numeric_to_alphanumeric(current_control_well_to_use, "control", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume_to_print) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False")))
            print("Controls" + str(used_control_plates) + "," + str(current_control_well_to_use) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume_to_print) + "," + str(used_ap_wells))
            controls_csv.write("Controls" + str(used_control_plates) + "," + str(numeric_to_alphanumeric(current_control_well_to_use, "control", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume_to_print) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False") + "\n"))

            #If the last element of list of ALL control wells from control plates has been used, repopulate that list
            if len(control_control_wells_numeric) == 1:
                control_control_wells_numeric.pop(0)
                if orientation[0]=="r":
                    control_control_wells_numeric = alphanum_to_num(control_control_wells, "control")
                if orientation[0] == "c":
                    control_control_wells_numeric = alphanum_to_num_columnwise(control_control_wells, "control")
            else:
                control_control_wells_numeric.pop(0)

        #If module of AP already used divided by total wells per AP is 0, add 1 to used AP and used control plates, reset the used AP and control wells to 0
        if used_ap_wells % wells_per_plate == 0:
            used_ap += 1
            used_ap_wells = 0
            used_control_plates += 1
            used_control_wells = 0

        if used_control_plates>total_num_control_plates: #If all the control plates has been used, reset the control plate counter to 1, essentially meaning re-use the control plates from now on
            used_control_plates = 1
            used_control_wells = 0

        #Add 1 to used wells, both AP and control
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

with  open('{}\\compound.csv'.format(output_directory), "w") as compound_csv: #Where you want your compound picking list to be located
    compound_csv.write("sep=,\n")
    ########################### Enter the loop #############################################
    for j in range(0, total_assay_wells):
        if used_ap_wells in compound_wells_in_ap:
            current_compound_well_to_use=compound_wells_to_be_dispensed_expanded[0]
            print("CP[" + str(used_cp)+ "]" + "," + str(numeric_to_alphanumeric(current_compound_well_to_use, "compound", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume_compuestos) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False")))
            print("CP[" + str(used_cp)+ "]" + "," + str(current_compound_well_to_use) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume_compuestos) + "," + str(used_ap_wells))
            compound_csv.write("CP["  + str(used_cp)+ "]" + "," + str(numeric_to_alphanumeric(current_compound_well_to_use, "compound", "False")) + "," + "AP[" + str(used_ap) + "]" + "," + str(volume_compuestos) + "," + str(numeric_to_alphanumeric(used_ap_wells, "assay", "False") + "\n"))
            used_cp_wells += 1

            if len(compound_wells_to_be_dispensed_expanded) == 1:
                compound_wells_to_be_dispensed_expanded.pop(0)
                compound_wells_to_be_dispensed_expanded = (expand_columns_and_rows(compound_wells_to_be_dispensed, "compound"))
                if orientation[1] == "r":
                    compound_wells_to_be_dispensed_expanded = alphanum_to_num(compound_wells_to_be_dispensed_expanded, "compound")
                if orientation[1] == "c":
                    compound_wells_to_be_dispensed_expanded = alphanum_to_num_columnwise(compound_wells_to_be_dispensed_expanded, "compound")
            else:
                compound_wells_to_be_dispensed_expanded.pop(0)

        if used_ap_wells % wells_per_plate == 0:
            used_ap += 1
            used_ap_wells = 0

        if (used_cp_wells-1) == len(compound_wells_to_be_dispensed_expanded_fixed):
            used_cp += 1
            used_cp_wells = 1

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


#delete_first_line_csv('{}\\controls.csv'.format(output_directory))
#delete_first_line_csv('{}\\compound.csv'.format(output_directory))