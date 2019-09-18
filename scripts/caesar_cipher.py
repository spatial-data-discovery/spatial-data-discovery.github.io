# caesar_ciper.py
#
# VERSION 0.2
#
# LAST_EDIT: 2019-09-17
#
# This script uses a Caesar cipher to encrypt a text message
#

##############################################################################
# REQUIRED MODULES
##############################################################################
import re
import sys

##############################################################################
# FUNCTIONS
##############################################################################
def show_help():
    """
    Name:     show_help
    Inputs:   None
    Outputs:  None
    Features: Prints the help text when user uses the '-h' command flag
    """
    help_txt = ("FILE: caesar_cipher.py\n"
                "DESC: This script uses a Caesar cipher to encrypt a text message written by the user.\n"
                "USGE: app_name [options]\n"
                "  -h, --help   shows the help text\n")
    print(help_txt)



##############################################################################
# CLASSES
##############################################################################
class Caesar:

    """
    Name: Caesar
    Features: Class for encrypting and decrypting a message
    History: Version 0.2
                - added show_help function
                - updated main to include error messages
            Version 0.1
                - original written in Fall 2018
    """


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Class Initialization
# ////////////////////////////////////////////////////////////////////////

    def __init__(self, shift):

        """
        Name:     Caesar.__init__
        Inputs:   str, shift variable
        Features: Initializes the Cipher class
        """
        # Intitialize class variables:

        self._encoder = [None] * 26
        self._decoder = [None] * 26

        for k in range(26):
            self._encoder[k] = chr((k + shift) % 26 + ord('A'))
            #ord- numeric position of that character in ASCII
            self._decoder[k] = chr((k - shift + 26) % 26 + ord('A'))
            #adding the 26 makes sure the value never goes negative


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Class Function Definitions
# ////////////////////////////////////////////////////////////////////////

    def encrypt(self, message):
        """
        Name:     Caesar.encrypt
        Inputs:   Message to encrypt
        Outputs:  Encoded message
        """
        return self._transform(message, self._encoder)

    def decrypt(self, secret):
        """
        Name:     Caesar.decrypt
        Inputs:   Message to decrypt
        Outputs:  Decrypted message
        """
        return self._transform(secret, self._decoder)

    def _transform(self, original, code):
        """
        Name:     Caesar._transform
        Inputs:   The message to be transformed and either encrypt or decrypt
        Outputs:  The transformed message
        """
        msg = list(original)                 # breaks it up by character
        for k in range(len(msg)):
            if msg[k].isupper():
                j = ord(msg[k]) - ord('A')   # gives the ASCII location
                msg[k] = code[j]             # the new coded letter
        return ''.join(msg)                  # appends all the letters


##############################################################################
# MAIN
##############################################################################
if __name__ == '__main__':

# Custructor call
    message = input("Enter The Message: ")
    cipher = Caesar(3)

# Check command line arguments
    if not re.match("^[A-Z a-z]*$", message):
        if (message == '-h') or (message == '--help'):
            show_help()

        else:
            show_help()
            print("Cipher only supports letters A-Z")

    elif len(message) == 0:
        show_help()
        print('Message not long enough to encrypt.')

    else:
        message = message.upper()
        coded = cipher.encrypt(message)
        print('Secret:  ' + coded)
        answer = cipher.decrypt(coded)
        print('Message: ' + answer)
