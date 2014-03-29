#!/usr/bin/env python

import sys

script_name = sys.argv[0]
first_argument = sys.argv[1]
all_arguments = ''.join(sys.argv[1:])

if first_argument == "":
    print "Usage: python tsv-to-motor.py source.tsv"
    exit

def script_step(compound, edge_element, x, y, scan_name, num_scans):
    # We assume that x and y are passed as strings,
    # not actual floating point numbers
    assert(type(x) == str)
    assert(type(y) == str)
    assert(num_scans > 0)
    commands = ""
    commands += "set field xafs.datafile_name "+edge_element+"_"+compound+".001\n"
    # TODO: make the .00x avoid clobbering existing files
    commands += "mabs smx "+x+"\n"
    commands += "mabs smy "+y+"\n"
    for _ in range(int(num_scans)):
        # If the beam goes down, we need to reopen the shutters
        commands += "op a\n"
        commands += "op b\n"
        # The actual scan instruction
        commands += "scan "+scan_name+"\n"

    commands += "\n"
    return commands

script_filename = first_argument + "_motor_script.txt"
script_file = open(script_filename, 'w')

script_beginning = "set plot nowait\nset header off\n\n"

script_end ="set plot on\nset header on"

script_file.write(script_beginning)

import csv
with open(first_argument) as tsvfile:
    rows = csv.reader(tsvfile, delimiter='\t')
    for i, row in enumerate(rows):
        if i == 0:
            pass
        else:
            compound, edge_element, x, y, scan_name, num_scans, comment = row
            print compound, "at", edge_element, "edge:",\
            num_scans, "scans of type", scan_name, "at position", x + "," + y
            script_file.write(script_step(compound, edge_element, x, y, scan_name, num_scans))
    script_file.write(script_end)
    script_file.close()
