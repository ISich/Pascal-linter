# Pascal Linter

##### made by: @VartoSss and @ISich

---

### Description:

This program is the implementation of a simple Linter for Pascal programming language that shows simple style errors just as invalid tabs in lines or identifiers named not in the correct case.

---

### Usage:

An app has GUI so to use it run main.py and you'll see the main app window. There you can find style analysis rules and their parameter fields. Also the true/false checkbox could tell the program ether to analyze or not the files with such rule.

On the bottom of the window there are buttons "Choose_files", "Choose_folders", "Clean_paths". The Linter can analyze multiple files in one request so this buttons help you to choose which files to work with. First two buttons are adding files in analyzing list (that btw can be vied in the very bottom of the window). The third button cleans the list.

The "Result" button will show you the window with style errors of each file.

---

### Project structure:

main.py is the entry point.

Menu is a UI class that creates the app window and handles all the buttons etc.

Linter - All the analyzing functions are located here.

tests.py - file for unittests.

---
