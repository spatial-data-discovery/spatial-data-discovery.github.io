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

<div style="display: block; margin-left: auto; margin-right: auto; padding: 0 15px; vertical-align: top;">
<pre style="overflow: auto; white-space: pre; margin: 0 0 29px 0; border: 1px solid #cccccc; border-radius: 2px; background: #091e42; font-family: monospace, monospace; font-size: 1em; line-height: 1.5; font-weight: 400;"><code style="display: block; padding: 24px 40px; color: #ebecf0; font-family: Courier, serif; font-size: 15px; line-height: 1.16667; letter-spacing: 0; word-spacing: 0; white-space: pre; text-indent: 0; box-sizing: border-box; overflow-x: auto; text-rendering: optimizeLegibility;"><span style="color: #a5adba;"># On the Terminal / Command Prompt</span>
cd [path to repository] <span style="color: #a5adba;"># replace "[path to repository]" with the directory path</span>
git clone https://github.com/spatial-data-discovery/spatial-data-discovery.github.io.git
cd spatial-data-discovery.github.io <span style="color: #a5adba;"># change into the repository directory</span>
git config user.name [username] <span style="color: #a5adba;"># replace "[username]" with your GitHub user name</span>
git config user.email [email] <span style="color: #a5adba;"># replace "[email]" with the email associated with GitHub</span></code></pre>
</div>

If this is your first time writing in Markdown, practice some basic features (e.g., headings, lists, links, images, and emphasis) in an online environment, such as [StackEdit.io](http://stackedit.io/).

When you are ready to write your "About" page:

* Find the "about_dtwoods.Rmd" file located in the course's repository parent directory, which you have cloned to your computer.
* Copy it and rename it using your GitHub user name (i.e., "about_YOURUSERNAME.Rmd"); *remember to use all lowercase letters*.
* Open your file using a text editor of your choice and delete everything below the YAML header (the set of "---" lines at the top of the file).
* Update your name and date in the YAML header.
* Add an image you would like to associate with your bio.
* Use a definition list, ordered/unordered list, and a text emphasis format somewhere in your file.

<div style="display: block; margin-left: auto; margin-right: auto; padding: 0 15px; vertical-align: top;">
<pre style="overflow: auto; white-space: pre; margin: 0 0 29px 0; border: 1px solid #cccccc; border-radius: 2px; background: #ebecf0; font-family: monospace, monospace; font-size: 1em; line-height: 1.5; font-weight: 400;"><code style="display: block; padding: 24px 40px; color: #091e42; font-family: Courier, serif; font-size: 15px; line-height: 1.16667; letter-spacing: 0; word-spacing: 0; white-space: pre; text-indent: 0; box-sizing: border-box; overflow-x: auto; text-rendering: optimizeLegibility;">---
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

INCLUDE A TEXT EMPHASIS FORMAT (*ITALICS*, **BOLD**, ~~STRIKETHROUGH~~)</code></pre>
</div>

Save and close your file, stage it, commit it and push it to the course's online repository.

<div style="display: block; margin-left: auto; margin-right: auto; padding: 0 15px; vertical-align: top;">
<pre style="overflow: auto; white-space: pre; margin: 0 0 29px 0; border: 1px solid #cccccc; border-radius: 2px; background: #091e42; font-family: monospace, monospace; font-size: 1em; line-height: 1.5; font-weight: 400;"><code style="display: block; padding: 24px 40px; color: #ebecf0; font-family: Courier, serif; font-size: 15px; line-height: 1.16667; letter-spacing: 0; word-spacing: 0; white-space: pre; text-indent: 0; box-sizing: border-box; overflow-x: auto; text-rendering: optimizeLegibility;"><span style="color: #a5adba;"># On the Terminal / Command Prompt</span>
git pull <span style="color: #a5adba;"># check for remote changes on the repository</span>
git add [your .Rmd file] <span style="color: #a5adba;"># replace "[your .Rmd file]" with your file name</span>
git commit -m "Created my about .Rmd file"
git push <span style="color: #a5adba;"># you may be prompted to enter your GitHub username and password</span></code></pre>
</div>
