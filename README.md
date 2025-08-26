Joven – LinkedIn Job Scraper

This repository contains the LinkedIn scraping module of the larger Joven project — an AI-powered assistant that helps job seekers by parsing resumes, finding relevant job openings, and streamlining applications.

The scraper automates job searches on LinkedIn Jobs, extracts listings in real-time, and saves detailed job descriptions for further processing by other Joven modules.

🚀 Features

Logs into LinkedIn using saved cookies (no need for repeated manual logins).

Scrapes jobs from LinkedIn Jobs Search with filters:

Keyword search (python developer by default)

Location (India, via geoId)

Posted date (last 24 hours)

Distance (default 100 km)

Captures:

Job list panel (titles, companies, locations, summaries)

Detailed job description of the selected listing

Saves job details to a file (jobDetail.txt) every 5 minutes.

🛠️ Requirements

Python 3.8+

Google Chrome (latest version)

ChromeDriver (matching your Chrome version)
Download from: https://chromedriver.chromium.org/downloads

Python Dependencies

Install all dependencies:

pip install selenium beautifulsoup4 python-dotenv

⚙️ Setup

Clone the repo

git clone https://github.com/ABarpanda/Joven.git
cd Joven


Add LinkedIn cookies

Log into LinkedIn in Chrome.

Export your session cookies (e.g., using EditThisCookie
).

Save them as linkedin_cookies.pkl in the project root.

Environment setup
Create a .env file (if needed later for credentials/config). For now, only cookies are required.

ChromeDriver setup

Place chromedriver.exe in the project root or add it to your PATH.

Update the script path if needed:

service = Service(executable_path="chromedriver.exe")

▶️ Usage

Run the scraper:

python get_cookies.py
python main.py


The script will:

Open LinkedIn and restore your login session using cookies.

Perform a job search for "python developer" in India.

Continuously scrape and:

Print job list panel (scaffold-layout__list).

Save detailed job description (scaffold-layout__detail) into jobDetail.txt.

📂 Output

Console → Prints job list (titles, companies, etc.)

File → jobDetail.txt contains the latest detailed job description

Example:

Software Engineer – Microsoft
Location: Bangalore
Posted: 1 day ago

Description:
We are looking for a Python developer...

🔧 Customization

You can modify the search filters in the script:

params = {
    "distance": 100,          # Search radius
    "f_TPR": "r86400",        # Posted in last 24h
    "geoId": 102713980,       # India
    "keywords": "python developer"  # Search keyword
}


Change keywords, geoId, or distance to match your needs.
👉 LinkedIn geoId list reference

⚠️ Notes

Use responsibly: LinkedIn actively detects and may block aggressive scraping.

Add delays/random sleep if scraping at scale.

Works best with headless mode (optional with Selenium).

If cookies expire, regenerate linkedin_cookies.pkl.

📌 Roadmap

 Store scraped jobs in CSV/JSON format

 Add multi-keyword / multi-location scraping

 Integrate with resume parser module

 Add support for proxy rotation & rate limiting

📄 License

This project is part of the Joven ecosystem.
Distributed under the MIT License.