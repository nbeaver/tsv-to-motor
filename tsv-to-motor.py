#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    print "Usage: python tsv-to-motor.py source.tsv"
    exit(1)

script_name = sys.argv[0]
first_argument = sys.argv[1]
all_arguments = ''.join(sys.argv[1:])

if first_argument == "":
    print "Usage: python tsv-to-motor.py source.tsv"
    exit(1)

def get_datafilename(compound, edge_element):
    import os.path
    for i in range(1,1000):
        file_extension = str(i).zfill(3) # Pad it with leading zeros, 001 to 999
        datafilename = edge_element+"_"+compound+"."+file_extension
        if os.path.isfile(datafilename):
            print datafilename, "already exists."
            pass
        else:
            return datafilename
    raise RunTimeError("Could not find a suitable datafilename for "+compound+" at edge "+edge_element)

def script_step(compound, edge_element, x, y, z, scan_name, num_scans):
    # We assume that x and y are passed as strings,
    # not actual floating point numbers
    assert(type(x) == str)
    assert(type(y) == str)
    assert(type(z) == str)
    assert(num_scans > 0)
    commands = ""

    commands += "set field xafs.datafile_name " + get_datafilename(compound, edge_element) + "\n"
    # DONE: make the .00x avoid clobbering existing files
    commands += "mabs smx "+x+"\n"
    commands += "mabs smy "+y+"\n"
    commands += "mabs smz "+z+"\n"
    for _ in range(int(num_scans)):
        # If the beam goes down, we need to reopen the shutters
        commands += "op a\n"
        commands += "op b\n"
        # The actual scan instruction
        commands += "scan "+scan_name+"\n"

    commands += "\n"
    return commands

script_filename = first_argument + "_motor_script.txt"

script_file = open(script_filename, 'wb')
# Write in binary mode so that \n does not become \r\n on Windows.

script_beginning = "set plot nowait\nset header off\n\n"

script_end ="set plot on\nset header on\n"

script_file.write(script_beginning)

import csv
with open(first_argument) as tsvfile:
    rows = csv.reader(tsvfile, delimiter='\t')
    for i, row in enumerate(rows):
        if i == 0:
            pass # Ignore column name header.
        else:
            compound, edge_element, x, y, z, scan_name, num_scans, comment = row
            print compound, "at", edge_element, "edge:",\
            num_scans, "scans of type", scan_name, "at position", x + "," + y + "," + z
            script_file.write(script_step(compound, edge_element, x, y, z, scan_name, num_scans))
    script_file.write(script_end)
    script_file.close()
