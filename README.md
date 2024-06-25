# Programmer salaries in Moscow

[Russian](RU_README.md)

The project is designed to analyze the average salaries of programmers in Moscow for popular programming languages.

## Description

This Python script uses open data from the HeadHunter and SuperJob job search platforms. It makes requests to the APIs of these sites to collect data about vacancies for the specified programming languages.

The script analyzes the proposed salaries and calculates the average salary for each programming language. The results are then displayed as a table in the console.

## How to install

To use this script you need to have Python3 installed on your computer.

To install the required dependencies, run the following command:

`pip install -r requirements.txt`

## Settings

1. Create an account on [SuperJob](https://api.superjob.ru/) register the application and a SeceretKey will be generated for you, which will be located in the ["Your application"](https://api.superjob.ru/info) section /) your account.

2. Create a .env file in the same directory as the script and add the following line:

`SUPER_JOB_API_KEY=<your_secret_key>`

## Usage

To use the script, open a terminal or command prompt and navigate to the directory where the script is located.

Run the script by running the following command:

`python main.py`

In the console you will see the result of the analysis of vacancies on the sites [HeadHunter](https://hh.ru/) and [SuperJob](https://superjob.ru/) in the form of two plates with information on the average salary of programmers in the city of Moscow by popular programming languages.

### Project goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).