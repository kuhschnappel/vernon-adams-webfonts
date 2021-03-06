#!/usr/bin/env python
#
# nonhinting.py
#
# Copyright (c) 2011 Khaled Hosny <khaledhosny@eglug.org>
#
# This program takes a TTF font with no hinting and sets
# its hinting tables with magic values that turn on 
# rendering features that provide optimal font display. 
#
# The magic is in two places: 
#
# 1. The GASP table. Vern Adams <vern@newtypography.co.uk>
#    suggests it should have value 15 for all sizes. 
#
# 2. The PREP table. Raph Levien <firstname.lastname@gmail.com>
#    suggests using his code to turn on 'drop out control'
#
# This script depends on fontTools Python library, available
# in most packaging systems and sf.net/projects/fonttools/ 
#
# Usage:
#
# $ ./vern-gasp.py FontIn.ttf FontOut.ttf


# Import our system library and fontTools ttLib
import sys
from fontTools import ttLib
from fontTools.ttLib.tables import ttProgram

# Open the font file supplied as the first argument on the command line
font = ttLib.TTFont(sys.argv[1])

# Set GASP table
gasp = ttLib.newTable("gasp")
gasp.gaspRange = {65535: 15}

# Set the PREP table
program = ttProgram.Program()
assembly = ['PUSHW[]', '511', 'SCANCTRL[]', 'PUSHB[]', '4', 'SCANTYPE[]']
program.fromAssembly(assembly)

prep = ttLib.newTable("prep")
prep.program = program

# Add the table to the font, replacing existing ones
font["gasp"] = gasp
font["prep"] = prep

# Save the font to the filename supplied as the second 
# argument on the command line

font.save(sys.argv[2])
