import os
import pickle
from json import dumps
from random import randint
from dotenv import load_dotenv
from time import sleep
from datetime import datetime

# Module Imports
from utils import fetch_req, send_mail

load_dotenv()

himalaya_marketing = os.getenv("HIMALAYA_MARKETING")
himalaya_data = os.getenv("HIMALAYA_DATA")
google_app_password = os.getenv("GOOGLE_PASSWORD")

M_DAT_FILE = "m_previous_data.dat"
D_DAT_FILE = "d_previous_data.dat"

sender = os.getenv("SENDER")
receiver = os.getenv("RECEIVER")

job_keywords = ["growth", "data", "analyst", "marketing"]

def run():
    process_marketing_jobs()

    sleep(randint(1,2))

    process_data_jobs()


def process_marketing_jobs():
    previous_data = None
    if os.path.exists(M_DAT_FILE):
        with open(M_DAT_FILE, "rb") as f:
            previous_data = pickle.load(f)

    marketing_jobs_raw = fetch_req(himalaya_marketing)
    marketing_jobs = marketing_jobs_raw.get("jobs", [])
    sleep(randint(1,2))
    
    for m_job in marketing_jobs:
        title = m_job["title"]
        
        if any(sub in title.lower() for sub in job_keywords):
            print(f"Match found in Marketing: {title}")          

            mjob_dict = {
                "title": title,
                "excerpt": m_job["excerpt"],
                "company_name": m_job["companyName"],
                "employment_type": m_job["employmentType"],
                "salary_period": m_job["salaryPeriod"],
                "currency": m_job["currency"],
                "location_restriction": m_job["locationRestrictions"],
                "timezone": m_job["timezoneRestrictions"],
                "application_link": m_job["applicationLink"],
                "pub_date": datetime.fromtimestamp(m_job["pubDate"]).date(),
                "expiry_date": datetime.fromtimestamp(m_job["expiryDate"]).date()
            }

            message = f"""
Job Title: {mjob_dict['title']} from: {mjob_dict['company_name']}
Brief Job Excerpt: {mjob_dict['excerpt']}
Salary Period: {mjob_dict['salary_period']} & Currency is: {mjob_dict['currency']}
Dates: Published on: {mjob_dict['pub_date']} and Expiring on: {mjob_dict['expiry_date']}
Apply at: {mjob_dict['application_link']}
            """
            
            if previous_data is None:
                print("First run ever for marketing...")
                with open(M_DAT_FILE, "wb") as f:
                    pickle.dump(mjob_dict, f)
                send_mail(sender, receiver, message, google_app_password)
                break
                
            elif title != previous_data.get("title"):
                print("Marketing data changed! Sending email...")
                with open(M_DAT_FILE, "wb") as f:
                    pickle.dump(mjob_dict, f)
                send_mail(sender, receiver, message, google_app_password)
                break
            else:
                print("Marketing job is exactly the same as last tracked. No email sent.")


def process_data_jobs():
    previous_data = None
    if os.path.exists(D_DAT_FILE):
        with open(D_DAT_FILE, "rb") as f:
            previous_data = pickle.load(f)

    data_jobs_raw = fetch_req(himalaya_data)
    data_jobs = data_jobs_raw.get("jobs", [])
    sleep(randint(1,2))

    for d_job in data_jobs:
        title = d_job["title"]
        
        if any(sub in title.lower() for sub in job_keywords):
            print(f"Match found in Data Jobs: {title}")          
            
            djob_dict = {
                "title": title,
                "excerpt": d_job["excerpt"],
                "company_name": d_job["companyName"],
                "employment_type": d_job["employmentType"],
                "salary_period": d_job["salaryPeriod"],
                "currency": d_job["currency"],
                "location_restriction": d_job["locationRestrictions"],
                "timezone": d_job["timezoneRestrictions"],
                "application_link": d_job["applicationLink"],
                "pub_date": datetime.fromtimestamp(d_job["pubDate"]).date(),
                "expiry_date": datetime.fromtimestamp(d_job["expiryDate"]).date()
            }

            message = f"""
Job Title: {djob_dict['title']} from: {djob_dict['company_name']}
Brief Job Excerpt: {djob_dict['excerpt']}
Salary Period: {djob_dict['salary_period']} & Currency is: {djob_dict['currency']}
Dates: Published on: {djob_dict['pub_date']} and Expiring on: {djob_dict['expiry_date']}
Apply at: {djob_dict['application_link']}
            """
            
            if previous_data is None:
                print("First run ever for data jobs...")
                with open(D_DAT_FILE, "wb") as f:
                    pickle.dump(djob_dict, f)
                send_mail(sender, receiver, message, google_app_password)
                break
                
            elif title != previous_data.get("title"):
                print("Data job changed! Sending email...")
                with open(D_DAT_FILE, "wb") as f:
                    pickle.dump(djob_dict, f)
                send_mail(sender, receiver, message, google_app_password)
                break
            else:
                print("Data job is exactly the same as last tracked. No email sent.")


if __name__ == "__main__":
    run()
