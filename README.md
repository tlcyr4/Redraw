# Redraw
## Table of Contents
- [Product Guide]
	- [Introduction](#introduction)
	- [User Guide]
		- [Searching for Rooms]
		- [GUI Navigation]
	- [Developer Guide]
		- [Getting Started](#getting-started)
			- [Environment Setup](#environment-setup)
			- [Run ReactJS Local](#run-reactjs-local)
			- [Run Django Local](#run-django-local)
			- [Production Build](#production-build)
		- [Back-End Systems]
			- [Database]
			- [Floorplans]
			- [Data Pre-Processing]
		- [Front-End Systems]
- [Project Report] 
	- [The Team](#the-team)
	- [Reflections]
		- [Milestones]
		- [Design Decisions]
			- [UI Design]
			- [Back-End Design]
			
## Product Guide
[Redraw](https://predraw.herokuapp.com) is a website built for Princeton 
undergraduate students and is equipped with an intuitive, fast, and 
powerful way of planning for Room Draw. The system allows students to 
find specific dorm rooms that would be the best fit for their campus 
life the following year. Using Redraw, students can connect to other 
students who are in their draw group to favorite potential rooms together.

A highly interactive GUI enhances the experience while providing detailed 
information about each of the rooms in every dorm building. The data 
available to the student body from the Housing Department’s website is 
conveniently formatted and conveyed to the users.

### Design Document
Our design document can be found [Here](https://tigerredraw.azurewebsites.net/).

## The Team
- Tigar Cyr, '20, Project Lead, Backend Developer
- Daniel Chae '20, Fullstack Developer
- Kesin Ryan Dehejia '20, Frontend Developer
- Chris Chu '19, Frontend Developer


## How To
### Environment Setup
Install [Python 3.x](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/) for Python 3.x. Install pipenv from Brew
```sh
brew install pipenv
```
Download the dependencies from Pipfile
```sh
pipenv install
```
For developing, make sure you have a copy of node_modules. Install npm
```sh
npm install
```

### Run ReactJS Local
Run on the terminal (opens up [localhost:3000](http://localhost:3000/))
```sh
npm start
```

### Run Django Local
Run on the terminal
```sh
./manage.py runserver
```
Open up [localhost:8000](http://localhost:8000/)

### Production Build
To get a production build after making changes to the front-end,
```sh
npm run build
```
This updates the 'build/' directory in the project 'root'.

## Other Notes
This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app). There is a ReactJS frontend running with a Django backend, deployed through Heroku
