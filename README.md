# glucan
This is a blood glucose analysis tool for my girlfriend, tailored to her specific analysis methodology.  This is an experimental tool intended for her specifically to use; I make no guarantee about the correctness of this sofrware's output or its fitness for any purpose.


# Instructions
1. Make sure Python is installed.  There's a legacy version of Python floating around.  You don't want that; you want Python 3.  You can install the latest version from https://www.python.org/.  If you're not sure whether/which version of Python is installed, you can open the command prompt and enter ``python --version``.  (If you're convinced that Python is installed but this returns an error, you may need to include Python in the class path; Google will tell you more.)
2. Download this software as a zip file.  As of May 2022, there's a green "Code" button in the upper right that will let you do this.  Unzip the zip file.
3. Modify the files in the example_input directory to encode the blood glucose data you want to analyze.  For more details about their format, see the Input section below.
4. Run glucan.py.  Your computer probably comes with PowerShell installed; if so, that's probably the easiest way.  Open the folder that contains glucan.py, click on the address bar at the top of the folder view, type PowerShell (replacing the folder path), and press enter.  This starts PowerShell in the current folder.  In PowerShell, enter the command ``python glucan.py``.  This should analyze your provided blood glucose data and output the results.

# Input
The input files are spreadsheets in the CSV (comma-separated value) file format.  They're very simple; you can look at them in a text editor like Notepad and see how they work.  You can create and edit them in spreadsheet tools like LibreOffice Sheets or Google Sheets - make sure to save in the CSV format.

You need to have four files in the example_input directory:
* sensitivities.csv
* basals.csv
* carb_ratios.csv
* events.csv

I'm not going to describe their contents in this version of the documentation; hopefully the provided examples are helpful.

