# CRIATCO CLIENT PORTAL

#### Video Demo URL:

#### Description

##### Introduction

This web application was developed as my final project for the CS50 Introduction to Computer Science online class from Harvard in partnership with Edx.

The goal for this project was to develop any type of program, webpage or web application to showcase the abilities we learned during the course.

My project consists of a Cliente Portal for my photography business that allows my clients to consult their data such as photo shoot summaries, pricing and editiing status. All the data is stores in a Notion database and is being pulled to the app through Notion's API.

This web application is built using Python and Flask for the backend.

My motivation to build this application was to familiarize myself with Notion's API and Flask's features. It was also a great opportunity for me to develop UI using HTML and CSS.

##### Observations

This is a very personal project and the integration with Notion is very specific to my own databases and account. There is currently no support to integrate this application with other Notion accounts.

As a test case, this application lacks the proper cyber security measures to protect users data and should not be deployed as is to real-world use.

##### Usage

This application has a very simple interface and forward usage. The client needs only to insert their identification number (Brazilian CPF, in this case) and, if the number is on the database, the page will show all the data related to it.

The user can only read the data and click the provided links in buttons. There is no support to updating or inserting data to a client's file from within the application.

The data shown on the page can only be modified by the owner of the connected Notion account.

##### Documentation

The application is divided into three sections:

`app.py`
The main Flask application that runs the server.

`notion_api.py`
This file stores all the specific functions used to retrieve and format data from Notion.

`templates/` and `static/`
These two folders store the `html`, `css` and image files required to render the pages.

##### Dependencies

- Flask 2.3.1
- Python 3.9

##### Contact me

[Linkedin](https://www.linkedin.com/in/vini-fig/)
Email: vinicius@criatco.com
