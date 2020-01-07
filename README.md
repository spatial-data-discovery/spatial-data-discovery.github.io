# spatial-data-discovery.github.io
Organization website

## About the Coder Assignment
This assignment is a way of introducing you to the Markdown syntax and demonstrates how we will be communicating to the public through the web. Additionally, you will practice using git by submitting your file to the course's online repository.

**Requirements**

* Name your .Rmd file "about" + _ + your GitHub user name in all lowercase (e.g., about_dtwoods.Rmd) in the parent repository directory.
* Include an embedded image (*keep it appropriate*)
* Include at least one definition list (e.g., bio, hobbies, website, etc.)
* Include an ordered and/or unordered list.
* Include a type of text formatting (e.g., *italics*, **bold**, ~~strikethrough~~).
* Keep your markdown formatting clean, clear, and consistent.

**Instructions**

If you have not already, create a folder for our course repository, clone the repository on to your computer, and configure your git workspace using the commands below.

```
# On the Terminal / Command Prompt
cd [path to repository] # replace "[path to repository]" with the directory path
git clone https://github.com/spatial-data-discovery/spatial-data-discovery.github.io.git
cd spatial-data-discovery.github.io # change into the repository directory
git config user.name [username] # replace "[username]" with your GitHub user name
git config user.email [email] # replace "[email]" with the email associated with GitHub
```

If this is your first time writing in Markdown, practice some basic features (e.g., headings, lists, links, images, and emphasis) in an online environment, such as [StackEdit.io](http://stackedit.io/).

When you are ready to write your "About" page:

* Find the "about_dtwoods.Rmd" file located in the course's repository parent directory, which you have cloned to your computer.
* Copy it and rename it using your GitHub user name (i.e., "about_YOURUSERNAME.Rmd"); *remember to use all lowercase letters*.
* Open your file using a text editor of your choice and delete everything below the YAML header (the set of "---" lines at the top of the file).
* Update your name and date in the YAML header.
* Add an image you would like to associate with your bio.
* Use a definition list, ordered/unordered list, and a text emphasis format somewhere in your file.

```
---
title: "About the Coder"
author: "YOURNAME"
date: "TODAY'S DATE"
---

![ALT TEXT](URL TO IMAGE "TITLE")

Bio
:  YOUR BIO LINE

INCLUDE AN (ORDERED/UNORDERED) LIST

- UNORDERED ITEM 1
- UNORDERED ITEM 2

INCLUDE A TEXT EMPHASIS FORMAT (*ITALICS*, **BOLD**, ~~STRIKETHROUGH~~)
```

Save and close your file, stage it, commit it and push it to the course's online repository.

```
# On the Terminal / Command Prompt</span>
git pull # check for remote changes on the repository
git add [your .Rmd file] # replace "[your .Rmd file]" with your file name
git commit -m "Created my about .Rmd file"
git push # you may be prompted to enter your GitHub username and password
```
