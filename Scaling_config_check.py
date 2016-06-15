"""
Title:  Scaling Configuration Set Checker

Revision:  1.0
Author:  Nick Okerberg

Description:  This script will analyze a configuration file from a Juniper Networks router that
is in "set" format.  The script will determine the scaling profile of the router from a configuration
perspective.  For example, it will output the number of physical interfaces, number of vrfs, and etc,
that are configured on the router.  

Instructions:  Capture the "show configuration | display set" output in a file. Execute the
script using the syntax below from a command prompt and it will return the scaling profile back.
  Scaling_config_check.py <config-file-name>
This has been tested on Windows 10.  

Revision History:
Date          Ver   Author          Description
2016/06/14    1.0   Nick            Initial release, created with Python 2.7.11.

"""

import sys      # For command line arguments.

# Usage Check
if len(sys.argv) != 2:
  sys.exit('\nUsage: python %s <config-file>' % sys.argv[0])

# Variables and Initializations
configFile = sys.argv[1]   # Set variable for the command line argument for file name.   
listIFD = []        # Initialize list of IFDs.
listIFL = []        # Initialize list of IFLs.
listLSP = []        # Initialize list of LSPs.  
listVRF = []        # Initialize list of VRF instances.  
listVPLS = []       # Initialize list of VPLS instances.
listL2VPN = []      # Initialize list of L2VPN instances.

# Iterate through the config file, line by line.
for line in open(configFile, "r").read().splitlines():
  
  # If the IFD doesn't exist in its list, then add it.  
  if 'set interfaces ' in line:
    words = line.split(' ')
    if (words[2] not in listIFD and words[2].find("lo0") == -1 and words[2].find("fxp") == -1 and words[2].find("em") == -1):
      listIFD.append(words[2])

  # If the IFL doesn't exist in its list, then add it.
  if 'set interfaces ' in line and 'unit' in line:
    words = line.split(' ')
    ifl = words[2] + '.' + words[4]
    if ifl not in listIFL:
      listIFL.append(ifl)

  # If the LSP isn't in its list, then add it.
  if 'set protocols mpls label-switched-path ' in line:
    words = line.split(' ')
    if words[4] not in listLSP:
      listLSP.append(words[4])      

  # If the VRF isn't in its list, then add it.
  if 'set routing-instances ' in line and 'instance-type vrf' in line:
    words = line.split(' ')
    if words[2] not in listVRF:
      listVRF.append(words[2])

  # If the VPLS instance isn't in its list, then add it.
  if 'set routing-instances ' in line and 'instance-type vpls' in line:
    words = line.split(' ')
    if words[2] not in listVPLS:
      listVPLS.append(words[2])

  # If the L2VPN instance isn't in its list, then add it.
  if 'set routing-instances ' in line and 'instance-type l2vpn' in line:
    words = line.split(' ')
    if words[2] not in listL2VPN:
      listL2VPN.append(words[2])

# Print the results
print "IFDs: ".ljust(20) + str(len(listIFD)).ljust(20)
print "IFLs: ".ljust(20) + str(len(listIFL)).ljust(20)
print "LSPs: ".ljust(20) + str(len(listLSP)).ljust(20)
print "VRFs: ".ljust(20) + str(len(listVRF)).ljust(20)
print "VPLS: ".ljust(20) + str(len(listVPLS)).ljust(20)
print "L2VPN: ".ljust(20) + str(len(listL2VPN)).ljust(20)

