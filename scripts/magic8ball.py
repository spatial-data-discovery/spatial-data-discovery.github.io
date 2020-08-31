import sys
import random
import argparse

def magic8ball():
	ans = True

	while ans:

		# Asks the user a question

		question = input("What is your question for the Magic 8 Ball? ")

		# Produces another integer

		ans = random.randint(1,20)

		# Quits program if user presses enter

		if question == "":
			sys.exit()

		elif ans == 1:
			print("It is certain.")

		elif ans == 2:
			print("It is decidedly so.")

		elif ans == 3:
			print("Without a doubt.")

		elif ans == 4:
			print("Yes - definitely.")

		elif ans == 5:
			print("You may rely on it.")

		elif ans == 6:
			print("As I see it, yes.")

		elif ans == 7:
			print("Most likely.")

		elif ans == 8:
			print("Outlook good.")

		elif ans == 9:
			print("Yes.")

		elif ans == 10:
			print("Signs point to yes.")

		elif ans == 11:
			print("Reply hazy, try again.")

		elif ans == 12:
			print("Ask again later.")

		elif ans == 13:
			print("Better not tell you now.")

		elif ans == 14:
			print("Cannot predict now.")

		elif ans == 15:
			print("Concentrate and ask again.")

		elif ans == 16:
			print("Don't count on it.")

		elif ans == 17:
			print("My reply is no.")

		elif ans == 18:
			print("My sources say no.")

		elif ans == 19:
			print("Outlook not so good.")

		elif ans == 20:
			print("Very doubtful.")

# Gives message to user if the enter --help

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="Type the a question to ask the Magic 8 Ball or press enter to exit.")
	args = p.parse_args()

	magic8ball()
