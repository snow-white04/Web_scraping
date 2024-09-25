import sqlite3 
import requests 
from bs4 import BeautifulSoup 

def setup_db():
    con = sqlite3.connect('Jobs.db')
    cursor = con.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS jobs
                    (
                    id INTEGER,
                    job_title TEXT(500),
                    creator TEXT(500),
                    address TEXT(500),
                    date TEXT
                    )
                    """)
    con.commit()
    return con, cursor

def scrape_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    job_id = 1
    for job in soup.find_all('div', class_='card-content'):
        job_title = job.find('h2', class_='title').text.strip()
        creator = job.find('h3', class_='company').text.strip()
        address = job.find('p', class_='location').text.strip()
        date = job.find('time')['datetime']
        jobs.append((job_id, job_title, creator, address, date))  # Use a tuple here
        job_id += 1
    return jobs

def insert_jobs(cursor, jobs):
    cursor.executemany("""
                       INSERT INTO jobs (id, job_title, creator, address, date)
                       VALUES (?, ?, ?, ?, ?)
                       """, jobs)
    
def display_jobs(cursor):
    cursor.execute("""
                   SELECT id, job_title, creator, address, date FROM jobs
                   """)
    for job in cursor.fetchall():
        print(
            f"ID: {job[0]}, Work title: {job[1]}, Creator: {job[2]}, Address: {job[3]}, Date: {job[4]}"
        )

def main():
    con, cursor = setup_db()  # Call the function here
    jobs = scrape_jobs()
    insert_jobs(cursor, jobs)
    con.commit()
    display_jobs(cursor)
    con.close()

if __name__ == '__main__':  # Corrected the if statement
    main()
