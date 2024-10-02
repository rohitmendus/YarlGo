# YarlGo

## Description
To sum it up, it's a test management system with several additional features like question bank, 
test and user reports, chatting as well as a well developed course interface. It's primary aim is to address 
the concerns of maintaininng and developing an interface for students to be able to prepare for high level exams.
**Please Note:  This work was done as part of an internship**

## Features
This app has the following features:
 - A user role system which includes admin, faculty and student(Note: The admin mentioned here has completely different roles as opposed to the admin of the site.)
 - A well developed interface for managing users.
 - The abilty to add and manage different exams and its sub categories.
 - Adding and managing of subjects and topics alike which are assigned to the faculty for administration.
 - To group students to batches based on the exam category they wish to study for.
 - Question banks for subjects which are provided to the students based on the batch they were added to.
 - An interface to add and manage questions to the question bank. This interface is used by the faculty based on the subject they were assigned under.
 - The ability to arrange practice tests for the students. Performance based eports are generated based on the test.
 - Dashboards and overview pages for the admin and faculty to see reports based on users, batches, subjects and question banks
 - Interface to add or manage your profile information.
 - An interface for the students to go through the question bank.
 - An interface for students to attend the practice tests arranged.
 - A chatting interfcae for students to communicate to their assigned faculty
**P.S: Additional will be added and not all features are complete!**

## Componenets
This app has the following components(apps in Django):
 - Accounts App
 - Exams App
 - Subjects App
 - Batches App
 - Tests App
 - Chat App

## How to Install
 1. Clone the repo
 2. In your virtual env or python environment install the dependencies mentioned in the [requirments.txt](https://github.com/rohitmendus/YarlGo/blob/main/requirements.txt) file.
 3. In the settings.py file replace the database configuration and the secret key with yours.
 4. Run `python manage.py migrate` to migrate the tables.
 5. The final step is to load all the fixtures in the accounts and subjects app. Type in this in the terminal inside the project directory `python manage.py loaddata <fixturename>`. Do this for each fixture. For example `python manage.py loaddata admin_user.json`.
