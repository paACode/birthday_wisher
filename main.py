import random
import smtplib
import pandas
import datetime as dt
import os
import glob


##################### Hard Starting Project ######################

# 1. Update the birthdays.csv with your friends & family's details. 
# HINT: Make sure one of the entries matches today's date for testing purposes. 

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
    return my_email, my_password


if __name__ == '__main__':
    cwd = os.getcwd()
    all_birthdays = read_birthdays_from_csv()
    today_birthdays = get_all_birthdays_of_today(dt.datetime.now())
    sender_email, sender_password = get_credentials()
    for birthday in today_birthdays.itertuples():
        letter = get_random_letter()
        personal_letter = letter.replace("[NAME]", birthday.name)
        write_email(personal_letter)

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# HINT: https://www.w3schools.com/python/ref_string_replace.asp

# 4. Send the letter generated in step 3 to that person's email address.
# HINT: Gmail(smtp.gmail.com), Yahoo(smtp.mail.yahoo.com), Hotmail(smtp.live.com), Outlook(smtp-mail.outlook.com)
