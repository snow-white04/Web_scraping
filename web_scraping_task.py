import sqlite3
import requests
from bs4 import BeautifulSoup

def setup_db():
    con = sqlite3.connect('Jobs.db')
    cursor = con.cursor()
    cursor.execute("""
                    create table if not exists jobs
                    (
                    id integer,
                    job_title text(500),
                    creator text(500),
                    address text(500),
                    date text
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
        jobs.append((job_id, job_title, creator, address, date))
        job_id += 1
    return jobs

def insert_jobs(cursor, jobs):
    cursor.executemany("""
                       insert into jobs (id, job_title, creator, address, date)
                       values (?, ?, ?, ?, ?)
                       """, jobs)

def insert_specific_job(cursor):
    specific_job = (1, 'data_analyst', 'Cobb-Douglas', 'Marietta, GA', '2024-09-25')
    cursor.execute("""
                   insert into jobs (id, job_title, creator, address, date)
                   values (?, ?, ?, ?, ?)
                   """, specific_job)

def display_jobs(cursor):
    cursor.execute("""
                   select id, job_title, creator, address, date from jobs
                   """)
    for job in cursor.fetchall():
        print(
            f"ID: {job[0]}, Job title: {job[1]}, Creator: {job[2]}, Address: {job[3]}, Date: {job[4]}"
        )

def main():
    con, cursor = setup_db()
    jobs = scrape_jobs()
    insert_jobs(cursor, jobs)
    insert_specific_job(cursor)  
    con.commit()
    display_jobs(cursor)
    con.close()

if __name__ == '__main__':
    main()
