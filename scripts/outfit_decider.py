import sys
import argparse
import random


colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'white', 'gray']

def pick_outfit():
    top = random.choice(colors)
    bottom = random.choice(colors)
    if temp >= 75:
        print("Wear a", top, "t-shirt with", bottom, "shorts")
    if temp < 75 and temp > 60:
        print("Wear a", top, "hoodie with", bottom, "shorts")
    if temp <= 60 and temp > 40:
        print("Wear a", top, "hoodie with", bottom, "pants")
    if temp <= 40:
        print("Wear a", top, "jacket with", bottom, "pants")
        
def new_outfit():
    new = input("Do you want a different outfit? (yes/no)")
    if new == "yes":
        pick_outfit()
        new_outfit()
    if new == "no":
        print("Have a great day!")
    
    
    
if __name__ == "__main__":
    
    script_desc = "This script decides an outfit for the user depending on the weather"
    p = argparse.ArgumentParser(description = script_desc)
    args = p.parse_args()
    
    temp = int(input("Lets decide your outfit! First we need to know the weather today. What is the temperature?"))
    
    pick_outfit()
    
    new_outfit()
    
        
    