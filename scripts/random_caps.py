import numpy.random as random

# Define constants
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"


def main(file_in: str, file_out: str = "./rand_caps.txt"):
    """
    Takes an input text file and randomly capitalizes the letters in it.
    Writes the output to another text file.

    :param file_in: Path to a text file containing letters to randomly capitalize
    :param file_out: Path to a text file to write the new letters in
                     Default: `./rand_caps.txt`
    """
    file_input = open(file_in, "r")
    char_list = []
    # Collect all the ASCII characters
    for line in file_input:
        for character in line:
            char_list.append(character)

    file_input.close()
    output_file = open(file_out, 'w')
    # Go through and randomly capitalize them
    for character in char_list:
        # Pick whether to change it
        change_char = random.randint(0, 2)
        # Change it from upper to lower or vice-versa
        if change_char == 1 and character in UPPER:
            output_file.write(character.lower())
        elif change_char == 1 and character in LOWER:
            output_file.write(character.upper())
        else:
            output_file.write(character)
    output_file.close()


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("file", help="The file to read in letters from")
    p.add_argument("-o", "--out", nargs="?", default="./rand_caps.txt", help="Path to a file to hold the output")
    args = p.parse_args()

    main(args.file, args.out)
