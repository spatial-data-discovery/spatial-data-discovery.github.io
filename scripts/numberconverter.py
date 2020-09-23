import argparse

##this simple utility script uses the Python argparse library to convert a decimal integer into binary, octal, and hexadecimal.
##this utility script is based on the code hosted by Programiz at the following URL, author unknown
##https://www.programiz.com/python-programming/examples/conversion-binary-octal-hexadecimal

def integerConverter(int):
	print("The decimal value of", int, "is:")
	print(bin(int), "in binary.")
	print(oct(int), "in octal.")
	print(hex(int), "in hexadecimal.")
	return

parser = argparse.ArgumentParser(description='Convert a decimal integer to binary, octal, and hexadecimal.')
parser.add_argument('integer', type=int, help='the decimal integer to be converted')
args = parser.parse_args()

integerConverter(args.integer) 