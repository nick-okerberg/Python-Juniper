"""
Title:  Juniper Library

Revision:  1.0
Author:  Nick Okerberg

Description:  This library file defines several functions that can be used as part of other
programs.  See the heading above each function definition for the details of what that
particular function does.  

Instructions:  The functions can be copied into another program, or imported.  
This has been tested on Windows 10.  

Revision History:
Date          Ver   Author          Description
2016/06/08    1.0   Nick            Initial release, created with Python 2.7.11.
"""



# Begin Function Definitions.



"""
This function takes in a string, which is a line of text from an output that includes
the router cli prompt.  It parses the line to find the router name.  An example line
that the function expects is:
    userName@routerName> show chassis hardware
The router name is then returned back as a string.  If the router name couldn't be
parsed out of the line, it returns the error code "???".  
"""
def getHostName(s):
    errorCode = "???"   # Initialize the error code.
    
    # Compliance check.
    if isinstance(s, basestring) == False:
        return errorCode
    if (s.find("@") == -1 and s.find(">") == -1):
        return errorCode
    if (s.find("@") > s.find(">")):
        return errorCode

    s = s.lstrip()  # Strip the whitespace on the left side of the line.

    CharAt = s.find("@")    # Find the "@" symbol index number.
    subStr = s[CharAt+1:]   # Create a substring from the index of "@" to the end of line.
    result = subStr[:subStr.find(">")]  # The result is the text between "@" and ">". 
    return result



"""
This function takes in a string, which is a line of text from an output that includes
the router cli prompt.  It parses the line to find the user name.  An example line
that the function expects is:
    userName@routerName> show chassis hardware
The user name is then returned back as a string.  If the user name couldn't be
parsed out of the line, it returns the error code "???".  
"""
def getUserName(s):
    errorCode = "???"   # Initialize the error code.

    # Compliance check.
    if isinstance(s, basestring) == False:
        return errorCode
    if (s.find("@") == -1 and s.find(">") == -1):
        return errorCode
    if (s.find("@") > s.find(">")):
        return errorCode

    s = s.lstrip()  # Strip the whitespace on the left side of the line.

    CharAt = s.find("@")    # Find the "@" symbol index number.
    result = s[:CharAt]     # The result is the text from the beginning to the "@" index.
    return result    



"""
This function takes in an IFD and 'show chassis hardware' output as strings,
then determines the optic type of the IFD.  It returns back the optic type
as a string.
"""
def getOpticForIFD(ifd, s):
    # If ifd is not in ifd format, then return a null string.
    if (ifd.count('-') != 1 or ifd.count('/') !=2):
        return ""
    # If ifd is not a string, then return a null string.
    if isinstance(ifd, basestring) == False:
        return ""
    # If s is not in "show chassis hardware" format, then return a null string.
    if (s.find("Hardware inventory") == -1):
        return ""
    # If s is not a string, return null string.
    if isinstance(s, basestring) == False:
        return ""

    result = ""       # Initialize the result string to be returned.
    
    # Determine the FPC slot number of the ifd, put this in 'fpc' variable.
    f_charAt = ifd.find("-")
    f_str = ifd[f_charAt+1:]
    fpc = f_str[:f_str.find("/")]

    # Determine the PIC slot number of the ifd, put this in the 'pic' variable.
    p_charAt = ifd.find("/")
    p_str = ifd[p_charAt+1:]
    pic = p_str[:p_str.find("/")]

    # Determine the port number of the ifd, put this in the 'port' variable.
    x_charAt = ifd.rfind("/")
    x_str = ifd[x_charAt+1:]
    port = x_str

    m_f = 0         # Match code for FPC.
    m_p = 0         # Match code for PIC.
    m_x = 0         # Match code for Port.

    s = s.split('\n')   # Split string s into a list of lines.

    # Iterate through the list of lines to find the fpc, pic, and xcvr.
    for line in s:
        line = line.lstrip()    # Remove whitespace from beginning of lines.
        
        if (line.startswith("FPC ") and m_f == 1):
            break
        if (line.startswith("FPC ") and m_f == 0):
            words = line.split(' ')
            if (words[1] == fpc):     # Found the FPC match, set fpc match code to 1.
                m_f = 1
                continue

        if (line.startswith("PIC ") and m_f == 1 and m_p == 1):
            break          
        if (line.startswith("PIC ") and m_f == 1 and m_p == 0):
            words = line.split(' ')
            if (words[1] == pic):     # Found the PIC match, set the pic match code to 1.
                m_p = 1
                if line.find("RJ45") != -1:     # Add an exception for copper.
                    result = "RJ45_Copper"
                    break
                continue

        if (line.startswith("Xcvr ") and m_f == 1 and m_p == 1 and m_x == 1):
            break          
        if (line.startswith("Xcvr ") and m_f == 1 and m_p == 1 and m_x == 0):
            words = line.split(' ')
            if (words[1] == port):    # Found the Xcvr match.
                m_x = 1
                result = line[line.rfind(" ")+1:]
                break

    return result





