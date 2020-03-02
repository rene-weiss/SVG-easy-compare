# SVG-easy-compare
A small Python 3 script which batch compares SVG files contained in two folders.

## Introduction

I wrote this script because I had lots of SVG files that have been optimized and I needed to compare the result with the original files and tell me which ones were "too" different from the original (I had a 0.75% tolerance, because of optimization, it's barely visible), because the optimization made some errors.

**I do not claim that this is the best code ever, I'm still learning Python and I wanted to share my work, to help people looking for a solution to compare two vector files. Feel free to suggest changes if you think it can help others to better understand the script. The goal is to share a code that beginners can understand.**

## How does it work (as for now)

#### Basic explanation :
To compare .SVG files, the script basically converts all the .SVG files into 300dpi PNG files, creates a "diffimage", which is a mask showing in white which areas of the 2 SVGs are different. Then, the script counts how many white pixels there are and that gives us with a small conversion the difference percentage. The results are printed out in a logfile.

#### Longer explanation : 
It takes a folder as an input. This folder must contain two folders, each containing the same amount of .SVG files with the same names, and nothing else, otherwise, you could get errors from the script.
A very simple (and ugly) user interface made with Tkinter prompts the user into choosing that folder.

It then works with easy steps :
- It creates 3 folders : a "png" folder for each folder containing SVGs (2 total) and a "diffimages" folder in the main folder.
- It converts all the .SVG files in each folder and puts the output in their respective "png" folder.
- It then creates a mask file with the two corresponding .PNG files and stores it in the "diffimages" folder under the same name as the original.
- It counts how many white pixels there are in each diffimage and stores the data.
- It checks if the file trigger the threshold
- It creates a log containing the percentage of difference for each couple of files and indicates if it triggered the threshold.
- It "cleans" the folders by deleting the two "png" folders and deleting the diffimages of the files which passed the test.

## Dependencies

The script has been tested only on ArchLinux, so the name of the dependencies can vary between distros. I give here only the names for ArchLinux, feel free to tell me the packages names for the other distros so I can add them.

#### System dependencies :
- "*inkscape*", to export .SVG to .PNG in command line,
- "*opencv2*" (**AUR**), used to count the white pixels,
- "*imagemagick*", used to create the diffimages,
- "*mpg123*", used to play the error sound (optionnal, but usefull for debugging)

#### Python dependencies :
I installed those directly on my system to use with the system interpreter:
- "*python-opencv-python*" (**AUR**)

Tkinter should come bundled with your system.
This script also uses "*glob*", "*os*" and "*datetime*".

# Feel free to help me to improve this script for those in need, but remmeber to keep it easy to understand.
