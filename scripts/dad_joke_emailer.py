#!/usr/bin/env python
# coding: utf-8
# Last edit: 09/15/2021
# This script emails you a dad joke

## Required Packages
import random
import ssl
import smtplib
import os

jokes = [
    "What kind of noise does a witch's vehicle make? Brooooom Broooom",
    "What's brown and sticky? A stick",
    "Two guys walked into a bar. The third guy ducked",
    "Why are elevator jokes so good? They work on many levels",
    "My wife asked me to go get 6 cans of Sprite from the grocery store. I realized when I go home that I have picked 7 up.",
    "Why do bees have sticky hair? Because they use a honeycomb",
    "Why do some couples go to the gym? Because they want their relationship to work out",
    "How can you tell it's a dogwood tree? By the bark.",
    "My boss told me to have a good day, so I went home.",
    "Why did the man fall down he well? Because he couldn't see that well.",
    "When does a joke become a 'dad joke?' When it becomes apparent.",
    "Why is peter pan always flying? Because he Neverlands",
    "Which state has the most streets? Rhode Island",
    "I used to hate facial hair, but then it grew on me.",
    "Why did the coach go to the bank? To get his quarterback",
    "How do celebrities stay cool? They have many fans",
    "Sundays are always a little sad, but the day before is a sadder day",
    "5/4 people admit that they are bad at fractions",
    "You're American when you go into a bathroom and when you come out, but what are you while you are in the bathroom? European",
    "I've been thinking about taking up meditation. I figure it's better than sitting around and doing nothing",
    "Dogs can't operate MRI machines. But catscan",
    "Singing in the shower is fun until you get soap in your mouth. Then it becomes a soap opera.",
    "It takes guts to be an organ donor.",
    "I lost my job at the bank on my first day. A woman asked me to check her balance, so I pushed her over.",
    "How do you row a canoe filled with puppies? Bring out the doggy paddle.",
    "How does a penguin build his house? Igloos it together",
    "What kind of music do chiropractors like? Hip pop.",
    "What does a house wear? Address",
    "I was going to tell a time-traveling joke, but you guys didn't like it",
    "What does the accountant say while auditing a document? This is taxing.",
    "What do you call a toothless bear? A gummy bear",
    "Why couldn't the bicycle stand up by itself? It was two-tired",
    "What does a nosey pepper do? It gets jalapeno business.",
    "I know a lot of jokes about retired people, but none of them work",
    "What do you call two octopuses that look the same? Itenticle",
    "Sore throats are a pain in the neck"
]

a = random.sample(range(len(jokes)),1)

jokes_to_send = jokes[a[0]]

## Email setup to alert you of model completion and output info
# For this to work you may need to change your setting 'less secure app access' to ON
# I made a junk email for this specifically and suggest you do the same
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
email = input('Enter the email that will send and receive the email (you email yourself): ')
sender_email = email  # Enter your address
receiver_email = email  # Enter receiver address
password = input("Type your password and press enter: ")



## Sending message
message = """Subject: Hi there! Here is your joke! 

{dad_joke}

Have a great day! :)

This message is sent from Python.""".format(dad_joke = jokes_to_send)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)




