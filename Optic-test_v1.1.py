"""
Title:  Interface Optics Health Check

Revision:  1.1
Author:  Nick Okerberg, Javed Syed

Description:  This script will analyze a log file that contains the "show interfaces diagnostics
optics" output from a Juniper Networks router.  The script will get a list of all of the physical
interfaces found in that output, and determine if there are any optical warnings or alarms.  It
will then return with the total number of physical interfaces that contain optics and list any
physical interface that has an alarm or warning associated with it, including how many warnings
or alarms are associated with it.  

Instructions:  Capture the "show interfaces diagnostics optics" output in a log file. Execute the
script using the syntax below from a command prompt and it will return the data back.
  Optic-test_v1.1.py <log-file-name>
This has been tested on Windows 7.  

Revision History:
Date          Ver   Author          Description
2016/05/25    1.0   Nick, Javed     Initial release, created with Python 2.7.9.
2016/05/27    1.1   Nick            Updated to include taking the log file name as an argument.

"""

import sys      # For command line arguments.

# Usage Check
if len(sys.argv) != 2:
  sys.exit('\nUsage: python %s <log-file>' % sys.argv[0])

# Variables and Initializations
userLogFile = sys.argv[1]   # Set variable for the command line argument for file name.   
p = 0               # Initialize parse code for interface optics output.
listIFD = []        # Initialize list of IFD's.
dIFDalarm = dict()  # Dictionary of IFD to alarm count mapping.
dIFDwarn = dict()   # Dictionary of IFD to warning count mapping.

# Iterate through the log file, line by line.
for line in open(userLogFile, "r").read().splitlines():
  # Once we reach the desired output that we want to start parsing, set the parse code to 1 and continue.
  if (p == 0 and 'show interfaces diagnostics optics' in line and 'xml' not in line):
      p = 1
      continue
  # Once we reach the end of the desired output to be parsed, exit.
  if (p == 1 and '@' in line and '>' in line):
      p = 0
      break
  # Parse code variable is 1, this is where the desired output is and will be parsed.
  if p == 1:
      # For these lines, append the ifd to the list, initialize the alarm and warning counters,
      # and initialize the dictionaries.  
      if 'Physical interface:' in line:
          alarmCount = 0
          warnCount = 0
          words = line.split(' ')
          ifd = words[2].rstrip()   # The word at index 2 is the ifd.
          if ifd not in listIFD:
            listIFD.append(ifd)
            dIFDalarm[ifd] = alarmCount
            dIFDwarn[ifd] = warnCount
      # For these lines, if an alarm is On, then increment the alarm counter and update the dictionary.
      if (line.find("alarm") > 0):
          if (line.find("On") > 0):
            alarmCount = alarmCount + 1
            dIFDalarm[ifd] = alarmCount
      # For these lines, if a warning is On, then increment the warning counter and update the dictionary.
      if (line.find("warning") > 0):
          if (line.find("On") > 0):
            warnCount = warnCount + 1
            dIFDwarn[ifd] = warnCount
            
# The total number of ifd's found in the output, which is the length of the list.  
ifdCount = len(listIFD)

# First, print the total number of physical interfaces that contain optics that were found from the output:
print "The total number of physical interfaces with optics: "
print ifdCount
print ""

# Next, print all of the interfaces that were flagged to have any warnings or alarms.
# This includes the alarm count and warning count.
print "Interface".ljust(20) + "alarms".ljust(20) + "warnings".ljust(20)
for item in listIFD:
  if (dIFDalarm[item] > 0 or dIFDwarn[item] > 0):
    print item.ljust(20) + str(dIFDalarm[item]).ljust(20) + str(dIFDwarn[item]).ljust(20)


