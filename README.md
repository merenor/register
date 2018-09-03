# register

A small project to index names in a book

## Getting Started

The application is started by running make_register.py. It uses a sqlite3-database
with two tables for names and pages. The final register can be exported as docx or json.

## Installing

Packages needed:
- python-docx (export function)
- winsound (optional for beeping)

## Commands

- create xy.db - creates a new database xy.db
- load xy.db - loads an existing database
- quit - exits the program

# Page Operations

- here - shows all names on this pages
- page 2 - moves to page 2
- showpagesfor Beethoven, Ludwig van - shows all registered pages for Beethoven, Ludwig van
- delfrompage Beethoven, Ludwig van - deletes page entry

# Shortcuts

It is possible to create shortcuts for ids. For example, ".beet" for "id #123". Use the dictionary in shortcuts.py.

# Name Operations

- add Beethoven, Ludwig van - adds "Beethoven, Ludwig van on the current page" (creates name if new)
- # 123 - adds name with the id 123
- .beet - adds name of a shortcut (see above)
- delname Beethoven, Ludwig van - deletes the name
- find hoven - finds all names that include "hoven"
- rename 123 - renames entry with id 123
- importnames vorlauf.txt - imports names from vorlauf.txt (caution, special format)

# Export Operations

- exporttoword file.docx - exports to word file (pages are accumulated, e.g. 2-4, 5, 7-10)
- exporttodict file.json - exports a json dictionary

# Other functions

- diffr.py - used to get differences beetween to register files (vorlauf and the current version)
- countpages.py - function to accumulate pages
