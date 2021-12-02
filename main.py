import csv
import sqlite3
from datetime import datetime

#-----------------------------------------------------------------------------------------
# GLOBALS
#-----------------------------------------------------------------------------------------
DB_CONNECTION = sqlite3.connect('sql.db')
CURSOR = DB_CONNECTION.cursor()


#-----------------------------------------------------------------------------------------
# Opens a CSV file and creates a list of jobs based off of data in file
#-----------------------------------------------------------------------------------------
def read_csv():
    with open('salary_data.csv', encoding='utf-8') as file:
        dictReader = csv.DictReader(file)
        all_job_data = []
        for record in dictReader:
            all_job_data.append((
                record["company"],
                record["title"],
                record["level"],
                record["totalyearlycompensation"],
                record["basesalary"],
                record["bonus"],
                record["location"],
                record["yearsofexperience"],
                record["yearsatcompany"],
                record["timestamp"]
            ))
    return all_job_data


#-----------------------------------------------------------------------------------------
# Creates a job table to hold the info pulled from CSV file
#-----------------------------------------------------------------------------------------
def create_table():
    CURSOR.execute(
        "CREATE TABLE IF NOT EXISTS job\
         (company text,\
         title text,\
         level text,\
         totalyearlycompensation integer,\
         basesalary integer,\
         bonus integer,\
         location text,\
         yearsofexperience integer,\
         yearsatcompany integer, \
         timestamp text);")


#-----------------------------------------------------------------------------------------
# Populates the job table based off of given job_data list
#-----------------------------------------------------------------------------------------
def populate_table(all_job_data):
    CURSOR.executemany(
        "INSERT INTO job\
         (company,\
         title,\
         level,\
         totalyearlycompensation,\
         basesalary,\
         bonus,\
         location,\
         yearsofexperience,\
         yearsatcompany,\
         timestamp)\
         VALUES (?,?,?,?,?,?,?,?,?,?);", all_job_data)


#-----------------------------------------------------------------------------------------
# Checks to make sure that interactions with the user are valid.
# Str data type is assumed unless specified that you are looking for an integer instead
#-----------------------------------------------------------------------------------------
def validate_input(user_choice, data_type=str):
    if data_type == int:
        try:
            user_choice = int(user_choice)
            valid = isinstance(user_choice, data_type)
        except ValueError:
            valid = False
    else:
        valid = isinstance(user_choice, data_type)

    return valid


#-----------------------------------------------------------------------------------------
# Prompts a user if they want all records that meet the criteria to show
# If they do not, then they can input a number for the top num of records for criteria
#-----------------------------------------------------------------------------------------
def select_num_records(records):
    while (True):
        print(f"Display all {len(records)} results? (A)")
        print("OR some of the results? (S)")
        user_input = input("> ")
        is_valid = validate_input(user_input)

        user_input = user_input.upper()
        if user_input == "A" or user_input == "ALL":
            return records
        elif user_input == "S" or user_input =="SOME":
            print("How many records do you want to see?")
            user_input = input("> ")
            is_valid = validate_input(user_input, int)
            if is_valid:
                num_records = int(user_input)
                return records[:num_records]
            else:
                print("\n------> ERROR: Invalid input. Try putting in a number\n")
        else:
            print("\n------> ERROR: Invalid input, try again\n")


#-----------------------------------------------------------------------------------------
# Displays a list of jobs in a formatted table 
#-----------------------------------------------------------------------------------------
def display_results(results):
    new_results = select_num_records(results)

    print("\nRESULTS: ")
    pattern_string = "|  {:<20}  |  {:<20}  |  {:<20}  |  {:>8}  |  {:>8}  |  {:>8}  |  {:<20}  |"
    print("============================================================================================================================================")
    print(pattern_string.format("Company", "Title", "Level", "TotalPay", "Salary", "Bonus", "Location"))
    print("|------------------------|------------------------|------------------------|------------|------------|------------|------------------------|")

    for record in new_results:
        print(pattern_string.format(record[0][:20], record[1][:20], record[2][:20], record[3], record[4], record[5], record[6][:20]))

    print("|------------------------|------------------------|------------------------|------------|------------|------------|------------------------|")
    print(pattern_string.format("Company", "Title", "Level", "TotalPay", "Salary", "Bonus", "Location"))
    print("============================================================================================================================================\n")


#-----------------------------------------------------------------------------------------
# Premade Query Functions
#-----------------------------------------------------------------------------------------
def select_all():
    CURSOR.execute('SELECT * FROM job')
    results = CURSOR.fetchall()
    display_results(results)

def order_by_top_paying(desc_or_asc):
    CURSOR.execute(f"SELECT * FROM job ORDER BY totalyearlycompensation {desc_or_asc};")
    results = CURSOR.fetchall()
    display_results(results)

def top_paid_at_company(comp_name):
    CURSOR.execute(f"SELECT * FROM job WHERE company='{comp_name}' ORDER BY totalyearlycompensation DESC;")
    results = CURSOR.fetchall()
    display_results(results)

def top_paid_in_area(area):
    CURSOR.execute(f"SELECT * FROM job WHERE location='{area}' ORDER BY totalyearlycompensation DESC;")
    results = CURSOR.fetchall()
    display_results(results)

def top_paid_by_job(job):
    CURSOR.execute(f"SELECT * FROM job WHERE title='{job}' ORDER BY totalyearlycompensation DESC;")
    results = CURSOR.fetchall()
    display_results(results)
    

#-----------------------------------------------------------------------------------------
# Display Query Menu and handle user input
#-----------------------------------------------------------------------------------------
def query_list():
    while(True):
        print("         Pick a Query")
        print("/============================\\")
        print("| 0) Back to main menu       |")
        print("|                            |")
        print("|          Overall:          |")
        print("|----------------------------|")
        print("| 1) Most paid overall       |")
        print("| 2) Least paid overall      |")
        print("|                            |")
        print("|       Most paid at:        |")
        print("|----------------------------|")
        print("| 3) Apple                   |")
        print("| 4) Microsoft               |")
        print("| 5) Google                  |")
        print("| 6) Facebook                |")
        print("| 7) Amazon                  |")
        print("| 8) Custom                  |")
        print("|                            |")
        print("|       Most paid in:        |")
        print("|----------------------------|")
        print("| 9) Idaho Falls, ID         |")
        print("| 10) Boise, ID              |")
        print("| 11) Salt Lake City, UT     |")
        print("| 12) Seattle, WA            |")
        print("| 13) San Francisco, CA      |")
        print("| 14) Arlington, VA          |")
        print("| 15) Custom                 |")
        print("|                            |")
        print("|     Most paid by job:      |")
        print("|----------------------------|")
        print("| 16) Software Engineer      |")
        print("| 17) Software Engineering   |")
        print("|     Manager                |")
        print("| 18) Product Manager        |")
        print("| 19) Data Scientist         |")
        print("| 20) Custom                 |")
        print("\\============================/\n")      

        user_input = input("> ")
        print()
        if(validate_input(user_input, int)):
            if user_input =='0':
                break
            elif user_input =='1':
                order_by_top_paying('DESC')
            elif user_input =='2':
                order_by_top_paying('ASC')
            elif user_input =='3':
                top_paid_at_company('Apple')
            elif user_input =='4':
                top_paid_at_company('Microsoft')
            elif user_input =='5':
                top_paid_at_company('Google')
            elif user_input =='6':
                top_paid_at_company('Facebook')
            elif user_input =='7':
                top_paid_at_company('Amazon')
            elif user_input =='8':
                company = input("Company to search for: ")
                top_paid_at_company(company)
            elif user_input =='9':
                top_paid_in_area('Idaho Falls, ID')
            elif user_input =='10':
                top_paid_in_area('Boise, ID')
            elif user_input =='11':
                top_paid_in_area('Salt Lake City, UT')
            elif user_input =='12':
                top_paid_in_area('Seattle, WA')
            elif user_input =='13':
                top_paid_in_area('San Francisco, CA')
            elif user_input =='14':
                top_paid_in_area('Arlington, VA')
            elif user_input =='15':
                location = input("Location to search for: ")
                top_paid_in_area(location)
            elif user_input == '16':
                top_paid_by_job("Software Engineer")
            elif user_input == '17':
                top_paid_by_job("Software Engineering Manager")
            elif user_input == '18':
                top_paid_by_job("Product Manager")
            elif user_input == '19':
                top_paid_by_job("Data Scientist")
            elif user_input == '20':
                job = input("Job Title to search for: ")
                top_paid_by_job(job)

        else:
            print("\n------> ERROR: Invalid input, pick from the numbers above\n")
        

#-----------------------------------------------------------------------------------------
# Create a new job
#-----------------------------------------------------------------------------------------
def create_job():
    print("Input information to create new record")
    company = input("Company: ")
    title = input("Title: ")
    level = input("Level: ")
    totalPay = input("Total Pay: ")
    salary = input("Base Salary: ")
    bonus = input("Bonus: ")
    location = input("Location: ")
    yearsofexperience = input("Years of Experience: ")
    yearsatcompany = input("Years at Company: ")
    CURSOR.execute(f"INSERT INTO job (company,title,level,totalyearlycompensation,basesalary,bonus,location,yearsofexperience,yearsatcompany,timestamp)\
                     VALUES ('{company}','{title}','{level}','{totalPay}','{salary}','{bonus}','{location}','{yearsofexperience}','{yearsatcompany}','{datetime.now()}');")
    print("Record created!")


#-----------------------------------------------------------------------------------------
# Helper to update and delete job queries
#-----------------------------------------------------------------------------------------
def get_conditions():
    company = input("Company: ")
    title = input("Job Title: ")
    level = input("Level in Company: ")
    totalPay = input("Total Yearly Pay: ")
    return {'company' : company, 'title' : title, 'level': level, 'totalPay' : totalPay}


#-----------------------------------------------------------------------------------------
# Update a job
#-----------------------------------------------------------------------------------------
def run_update(column, new_value, cond):
    CURSOR.execute(f"\
            UPDATE job \
            SET {column} = {new_value}\
            WHERE company = '{cond['company']}'\
            AND title = '{cond['title']}'\
            AND level = '{cond['level']}'\
            AND totalyearlycompensation = '{cond['totalPay']}';")

def update_job():
    print("Please fill out fields to find job to update")

    conditions = get_conditions()

    print("What would you like to change?")
    print("1) Level")
    print("2) Total Pay")
    print("3) Bonus")
    print("4) Location")
    user_input = input("> ")

    if user_input == '1':
        column = 'level'
    elif user_input == '2':
        column = 'totalyearlycompensation'
    elif user_input == '3':
        column = 'bonus'
    elif user_input == '4':
        column = 'location'
    else:
        print("\n------> ERROR: Invalid input, pick from the numbers above\n")
        return
    
    new_value = input("Enter the new value: ")
    run_update(column, new_value, conditions)
    print("Update successful!")


#-----------------------------------------------------------------------------------------
# Delete a job
#-----------------------------------------------------------------------------------------
def run_delete(cond):
    CURSOR.execute(f"\
        DELETE FROM job\
        WHERE company = '{cond['company']}'\
            AND title = '{cond['title']}'\
            AND level = '{cond['level']}'\
            AND totalyearlycompensation = '{cond['totalPay']}';")

def delete_job():
    print("Fill in fields to find the job to delete")
    cond = get_conditions()
    run_delete(cond)
    print("Record deleted!")


#-----------------------------------------------------------------------------------------
# Display Main menu and handle user input
#-----------------------------------------------------------------------------------------
def start_menu():
    print("\n/=========================================================================\\")
    print("| Welcome to my Job/Salary Database! Pick a Number from the options below |")
    print("\\=========================================================================/")
    while(True):
        print("\n           MENU")
        print("/========================\\")
        print("| 0) Exit                |")
        print("| 1) View data           |")
        print("| 2) Run a query         |")
        print("| 3) Create a new record |")
        print("| 4) Update a record     |")
        print("| 5) Delete a record     |")
        print("\\========================/\n")
        user_input = input("> ")
        print()

        if(validate_input(user_input, int)):
            if user_input =='1':
                select_all()
            elif user_input =='2':
                query_list()
            elif user_input =='3':
                create_job()
            elif user_input =='4':
                update_job()
            elif user_input =='5':
                delete_job()
            elif user_input == '0':
                break
        else:
            print("\n------> ERROR: Invalid input, pick from the numbers above\n")


#-----------------------------------------------------------------------------------------
# MAIN - Manages the program
#-----------------------------------------------------------------------------------------
def main():
    # Get things initialized
    all_job_data = read_csv()
    create_table()
    populate_table(all_job_data)

    # Start the Menu
    start_menu()
        
# Run the Program
main()