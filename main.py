import random
import smtplib
import pandas
import datetime as dt
import os
import glob
import openai
import calendar


##################### Hard Starting Project ######################
# Todo: Add OpenAI
# Todo: Make sure email will be send only once a year, maybe with timestamp
# Todo: Make it OOP
# Todo: Add data of family and friends to list
# Todo: Create Application and add to startup

# 2. Check if today matches a birthday in the birthdays.csv
# HINT 1: Only the month and day matter. 
# HINT 2: You could create a dictionary from birthdays.csv that looks like this:
# birthdays_dict = {
#     (month, day): data_row
# }
def read_birthdays_from_csv():
    birthdays_dict = pandas.read_csv("birthdays.csv")
    return birthdays_dict


def get_all_birthdays_of_today(today):
    day_mask = all_birthdays['day'] == today.day
    month_mask = all_birthdays['month'] == today.month
    print(today.month)
    return all_birthdays[day_mask & month_mask]


def get_random_letter():
    letter_dir = os.path.join(cwd, 'letters')
    letter_files = glob.glob1(letter_dir, '*.txt')
    random_letter_file = random.choice(letter_files)
    letter_path = os.path.join(letter_dir, random_letter_file)
    with open(letter_path, "r") as file:
        random_letter = file.read()
    return random_letter


def write_email(email_txt):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=sender_email, password=sender_password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs="paack93@yahoo.com",
            msg=f"Subject: Happy Birthday! \n\n {email_txt}")


def get_credentials():
    credentials_path = os.path.join(cwd, 'my_credentials.txt')
    with open(credentials_path, "r") as file:
        credentials = file.readlines()
    my_email = credentials[0]
    my_password = credentials[1]
    my_openai_key = credentials[2]
    return my_email, my_password, my_openai_key


def get_keywords_of_the_month(month):
    keywords = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"I need 10 words that are related to the month {month}. Output in csv format",
        max_tokens=200
    )
    return keywords.choices[0].text.strip()


def get_letter_template(including_keywords):
    letter_template = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Generate a birthday letter with [for_name] and [from_name]. Include the words {including_keywords}. Max. 3 sentences",
        max_tokens=200
    )
    return letter_template.choices[0].text.strip()


def create_letter_template_as_txt(month):
    keywords = get_keywords_of_the_month(month)
    template = get_letter_template(keywords)
    with open(f'letters/{month}.txt', 'w') as f:
        f.write(template)

def create_templates_for_all_months():
    for month in range(1,12):
        create_letter_template_as_txt(calendar.month_name[month])


if __name__ == '__main__':
    cwd = os.getcwd()
    all_birthdays = read_birthdays_from_csv()
    today_birthdays = get_all_birthdays_of_today(dt.datetime.now())
    sender_email, sender_password, openai_key = get_credentials()
    openai.api_key = openai_key.strip()
    create_templates_for_all_months()
    #create_letter_template_as_txt(calendar.month_name[dt.datetime.now().month])

# 4. Send the letter generated in step 3 to that person's email address.
# HINT: Gmail(smtp.gmail.com), Yahoo(smtp.mail.yahoo.com), Hotmail(smtp.live.com), Outlook(smtp-mail.outlook.com)
