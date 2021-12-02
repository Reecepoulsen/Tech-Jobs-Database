# Overview
This repository contains software that allows you to query a dataset containing 62,640 jobs across large companies in the tech industry. The dataset in use can be found at [Kaggle](https://www.kaggle.com/jackogozaly/data-science-and-stem-salaries). The dataset is read into a SQLite database table so SQL can be used to query it.

You can start the software by running `python main.py` on the command line. You will then see a menu containing instructions on how to proceed.

I wrote this software because I wanted to gain some experience using `sqlite3` with python. I stumbled upon this dataset and it seemed like something that would be useful to query. It was definitely a good exercise.

[Software Demo Video](https://youtu.be/HvoeGN9V6ZI)

# Relational Database

For this project I am using `sqlite3` as my database.

The data is read into a job table that contains these columns: 
* company (text)
* title (text)
* level (text)
* total yearly compensation (integer)
* base salary (integer)
* bonus (integer)
* location (text)
* years of experience (integer)
* years at company (integer)
* timestamp (text)



# Development Environment

Tools used in developing this software:
* Editor: VSCode
* Rainbow CSV Extension
* SQLite Extension
* Data Source: Kaggle.com

Languages:
* Python
* SQL

Libraries:
* SQLite3
* CSV
* Datetime 

# Useful Websites

* [Kaggle](https://www.kaggle.com/)
* [SQLite Tutorials](https://www.sqlitetutorial.net/)
* [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)

# Future Work

* Make chainable queries. Ex: At company + In location 
* Make an easy way for a user to write their own queries without having to know SQL
* Make user input checking more robust