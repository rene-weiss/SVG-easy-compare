""" A simple script to check if 2 SVG files have significative visual differences.

This script compares 2 .SVG files by exporting these files in .PNG, creating a mask showing the differences in the
two vector images, counting the white pixels and calculate the difference. It then puts the output data in a logfile.
See README.md for more information.


This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

Copyright 2020 Lucile-Alice MEILER
"""

__author__ = "Lucile-ALice MEILER"
__date__ = "2020/03/02"
__deprecated__ = False
__license__ = "GPLv3 only"
__version__ = "0.0.1"


# Written and tested under ArchLinux with the system Python 3.8 interpreter.

from tkinter import *  # Tkinter
from tkinter import filedialog  # From Tkinter
from tkinter import ttk  # from Tkinter
from datetime import datetime
import glob
import cv2  # from OpenCV2 and OpenCV-Python
import os

# Also, make sure that :
# - 'Inkscape',
# - 'opencv2',
# - 'mpg123',
# - 'python-opencv-python',
# - 'ImageMagick'
# are installed on the system.

# GLOBALS
global dpi  # int
global threshold  # float
global file_percentage  # dict : Contains the file name with associated difference percentage.
global folder_1  # str
global folder_2  # str

# VARS
dpi = 300
threshold = 0.75


# Initiates the main program :
def init(folder_0):
    folder_0_directories = os.listdir(folder_0)

    # Checks if there are 2 directories in folder_0 :
    if len(folder_0_directories) > 2:
        error(error_text="More than 2 directories found in the work directory ! Please check the file tree !",
              is_critical=True)
    if len(folder_0_directories) < 2:
        error(error_text="Missing folders in the work directory ! Please check the file tree !",
              is_critical=True)
    if len(folder_0_directories) == 2:
        info(info_text="Found 2 folders !")

    # Checks if the 2 sub-folders contains the same number of files with the same names :
    folder_1_content = glob.glob(folder_0 + "/" + folder_0_directories[0] + "/*.svg")
    folder_2_content = glob.glob(folder_0 + "/" + folder_0_directories[1] + "/*.svg")
    if len(folder_1_content) != len(folder_2_content):
        error(error_text="The 2 folders don't contain the same amount of files ! Please check the file tree !",
              is_critical=True)
    # This needs some corrections but it works without...
    # if folder_1_content != folder_2_content:
    #    error(error_text="The 2 folders don't contain the same files ! Please check the file tree !",
    #          is_critical=True)
    else:
        info(info_text="The 2 folders have the same structure.")

    # Stores variables for later use:
    folder_1 = folder_0 + "/" + folder_0_directories[0]
    folder_2 = folder_0 + "/" + folder_0_directories[1]
    file_names = folder_1_content
    for index in range(len(file_names)):
        file_names[index] = file_names[index].replace(folder_1 + '/', '')

    total_file_nb = len(file_names)

    # Creates the work folders:
    create_tree(folder_0, folder_0_directories, file_names)

    main(folder_0, folder_1, folder_2, file_names, total_file_nb)


# Creates the work folders as follows :
#
# folder_0
#     |[] folder_1 (should exist)
#     |     |[] png (created folder)
#     |     | SVG files
#     |
#     |[] folder_2 (should exist)
#     |     |[] png (created folder)
#     |     | SVG files
#     |
#     |[] diffimages (created folder)
#     | logfile.txt (created at the end of the program)
#
def create_tree(folder_0, folder_0_directories, file_names):
    info(info_text="Creating sub-directories...")
    # Creating the 'png' sub-folders in each previously found folders :
    for folder in folder_0_directories:
        path = folder_0 + "/" + folder + "/png"
        os.system('mkdir "' + path + '"')
        # Check :
        present = os.listdir(folder_0 + "/" + folder)
        if len(present) - len(file_names) > 1:
            error(error_text="Too much sub-directories in \"" + folder + "\"! Please check the file tree !",
                  is_critical=True)
        if len(present) - len(file_names) < 1:
            error(error_text="Failed to create the folder in \"" + folder + "\"! Please check the file tree !",
                  is_critical=True)
        else:
            info(info_text="Created folder :" + path)
    # Creating the 'diffimages' folder in folder_0 :
    path = folder_0 + "/diffimages"
    os.system('mkdir "' + path + '"')
    # Check :
    present = os.listdir(folder_0)
    if len(present) == 2:
        error(error_text="Failed to create the folder in \"" + folder_0 + "\"! Please check the file tree !",
              is_critical=True)
    else:
        info(info_text="Created folder :" + path)


# Permanently delete the created folders & files but keeps the diffimages of the files that failed the tests.
def destroy_tree(folder_0, failed_files, total_file_nb, file_names):
    present_directories = os.listdir(folder_0)
    # Cleaning list :
    for index in range(len(present_directories)-1):
        if present_directories[index] == "diffimages":
            present_directories.pop(index)
        if present_directories[index] == "logfile.txt":
            present_directories.pop(index)
    # Deleting the /png folders :
    path = folder_0 + "/" + present_directories[0] + "/png"
    os.system("rm -r '" + path + "'")
    path = folder_0 + "/" + present_directories[1] + "/png"
    os.system("rm -r '" + path + "'")
    # Check :
    for index in range(len(present_directories)-1):
        folder_content = os.listdir(folder_0 + "/" + present_directories[index])
        if len(folder_content) == total_file_nb:
            info(info_text="The folder " + folder_0 + "/" + present_directories[
                index] + "/png has been deleted with all its content.")
        else:
            error(error_text="The folder" + folder_0 + "/" + present_directories[index] + "/png has not been deleted.",
                  is_critical=False)

    # Converting "files_names" with the correct file extension:
    file_names_png = list()
    for index in range(len(file_names)):
        file_names_png.append(file_names[index].replace(".svg", ".png"))

    # Keeping the diffimages of the failed files :
    failed_pass = 0
    for index in range(total_file_nb):
        if failed_files.count(file_names[index]) == 1:
            failed_pass = failed_pass + 1
        else:
            path = folder_0 + "/diffimages/" + file_names_png[index]
            os.system("rm '" + path + "'")
    # Check :
    diffimages_content = glob.glob(folder_0 + "/diffimages/*.png")
    if len(diffimages_content) == len(failed_files):
        info(info_text="All the passed diffimages were deleted successfully !")
    if len(diffimages_content) > len(failed_files):
        error(error_text="Not all required files were deleted !", is_critical=False)
    if len(diffimages_content) < len(failed_files):
        error(error_text="Too much files were deleted !", is_critical=False)


# Creates the logfile according to which files passed the test and those which failed.
def create_logfile(folder_0, failed_files, file_names, file_percentage):
    try:
        with open(folder_0 + "/logfile.txt", 'w') as log:
            for file in file_names:
                text_line = file + " : " + str(file_percentage[file])
                if failed_files.count(file) > 0:
                    text_line = text_line + "\t\t\t\tTEST FAILED !\n"
                else:
                    text_line = text_line + "\n"
                log.write(text_line)
    except EnvironmentError as open_error:
        error(error_text="The logfile could not be created !",
              is_critical=True)
    log.close()
    info(info_text="The logfile has been successfully created !")


# Converts to PNG all the files of a given folder and puts them in the corresponding folder.
def svg_to_png(folder, file_names):
    output_folder = folder + "/png/"
    for file in file_names:
        png_file = file.replace(".svg", ".png")
        input_file = folder + "/" + file
        output_file = output_folder + png_file
        os.system('inkscape -f "' + input_file + '" -d ' + str(dpi) + ' -e "' + output_file + '"')
    # Check :
    if len(glob.glob(folder + "/*.svg")) != len(glob.glob(output_folder + "/*.png")):
        error(error_text="There was an error during conversion into .png !",
              is_critical=True)
    else:
        info(info_text="All the files in " + folder + "were successfully converted to .png in " + output_folder + " !")


# Creates a black and white mask with the difference between 2 given PNG files
# and stores it in the folder_0/diffimages folder.
def create_mask(diffimage_path, image_1_path, image_2_path):
    command = "compare  -metric rmse '" + image_1_path + "' '" + image_2_path + \
              "' -compose Src -highlight-color White -lowlight-color Black '" + diffimage_path + "'"
    os.system(command)


# Counting the amount of white pixels in the mask (= difference between the 2 files)
# Returns the difference percentage.
def white_pixels_percentage(diffimage_path):
    image = cv2.imread(diffimage_path, 0)
    count = cv2.countNonZero(image)
    percentage = count * 100 / (1600 * 1600)
    info(info_text="The image " + diffimage_path + " has been successfully processed !")
    return percentage


# Creates a simple window allowing the user to select the working directory.
def folder_asking_window():
    global main_window  # Tk
    main_window = Tk()
    # Directory variable
    global work_directory_path  # str
    work_directory_path = StringVar()

    title = "Choose the folders to use with the script"
    main_window.title(title)
    main_window.resizable(False, False)
    main_window.geometry("222x130")

    # Contents in main_window :
    Label(main_window, text="      ").grid(column=0, row=1, rowspan=10)
    Label(main_window, text="      ").grid(column=0, row=0, columnspan=20)
    Label(main_window, text="      ").grid(column=1, row=2, rowspan=2)
    Label(main_window, text="      ").grid(column=3, row=2, rowspan=2)

    # "Select working directory" button :
    ttk.Button(main_window, text="Select the work folder", command=browse_button_working_directory).grid(column=1,
                                                                                                         row=1)
    # Displays the selected folder :
    Label(main_window, text="Selected work folder :").grid(column=1, row=3)
    Entry(main_window, textvariable=work_directory_path).grid(column=1, row=4)

    Label(main_window, text="      ").grid(column=2, row=4
                                           )
    # "Start" button :
    ttk.Button(main_window, text="Start the program", command=exit_window).grid(column=1, row=5)

    # Start main_window loop :
    main_window.mainloop()


# Destroys the window and start the main program.
def exit_window():
    main_window.destroy()


# Selects a working directory and stores a global variable.
def browse_button_working_directory():
    folder_name = filedialog.askdirectory()
    work_directory_path.set(folder_name)


# Prints a error string in the Python console.
def error(error_text, is_critical):
    now = datetime.now()
    print("[" + now.strftime("%H:%M:%S") + "] : ERROR : " + error_text)
    if is_critical is True:
        os.system("mpg123 -q error-edit.mp3")
        raise EnvironmentError


# Prints a information string in the Python console.
def info(info_text):
    now = datetime.now()
    print("[" + now.strftime("%H:%M:%S") + "] : INFO : " + info_text)


# Starts the main program.
def main(folder_0, folder_1, folder_2, file_names, total_file_nb):
    # Converts all the SVG to PNG files in the correct folder :
    svg_to_png(folder_1, file_names)
    svg_to_png(folder_2, file_names)

    # Creating variables :
    file_percentage = dict()

    # Creates the 'diffimages' :
    for file in file_names:
        png_file = file.replace(".svg", ".png")
        image_1_path = folder_1 + "/png/" + png_file
        image_2_path = folder_2 + "/png/" + png_file
        diffimage_path = folder_0 + "/diffimages/" + png_file

        create_mask(diffimage_path, image_1_path, image_2_path)
        # Get the percentage of white pixels in the diffimages :
        file_percentage[file] = white_pixels_percentage(folder_0 + "/diffimages/" + png_file)

    # Check if all the diffimages were created correctly :
    if len(glob.glob(folder_0 + "/diffimages/*.png")) != len(file_names):
        error(error_text="Failed to create all the diffimages ! Check the file tree !",
              is_critical=True)
    else:
        info(info_text="All the diffimages were created successfully !")

    # Check if the files are identical enough and adds them in a separate list if not :
    failed_files = list()
    for file, percentage in file_percentage.items():
        if percentage >= threshold:
            failed_files.append(file)

    # Create log
    create_logfile(folder_0, failed_files, file_names, file_percentage)

    # Cleaning
    destroy_tree(folder_0, failed_files, total_file_nb, file_names)


# Start the program :
folder_asking_window()
folder_0 = work_directory_path.get()
init(folder_0)
