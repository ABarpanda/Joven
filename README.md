# Joven – LinkedIn Job Scraper

This repository contains the **LinkedIn scraping module** of the larger **Joven project** — an AI-powered assistant that helps job seekers by parsing resumes, finding relevant job openings, and streamlining applications.

The scraper automates job searches on **LinkedIn Jobs**, extracts listings in real-time, and saves detailed job descriptions for further processing by other Joven modules.

---

## 🚀 Features

- Logs into LinkedIn using saved cookies (no repeated manual logins).
- Scrapes jobs from **LinkedIn Jobs Search** with filters:
  - Keyword search (`python developer` by default)
  - Location (**India**, via `geoId`)
  - Posted date (**last 24 hours**)
  - Distance (**100 km** default)
- Captures:
  - **Job list panel** (titles, companies, locations, summaries)
  - **Detailed job description** of the selected listing
- Saves job details to a file (`jobDetail.txt`) every 5 minutes.

---

## 🛠️ Requirements

- **Python 3.8+**
- **Google Chrome** (latest version)
- **ChromeDriver** (matching your Chrome version)  
  👉 [Download ChromeDriver](https://chromedriver.chromium.org/downloads)

### Python Dependencies
Install dependencies with:
```bash
pip install selenium python-dotenv
```
Sure 👍 — here’s your polished **Setup/Usage section** in proper **Markdown code block** so you can copy it directly into your `README.md`:


## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/ABarpanda/Joven.git
cd Joven
```

### 2. Add LinkedIn cookies

* Log into LinkedIn in Chrome.
* Export your session cookies (e.g., using [Latest chrome driver](https://googlechromelabs.github.io/chrome-for-testing/)).
* Save them as **`linkedin_cookies.pkl`** in the project root.

### 3. Environment setup

* Create a `.env` file if needed later (for credentials/config).
  *Currently, only cookies are required.*
* `pip install -r requirements.txt` to install all the dependencies.

### 4. ChromeDriver setup

* Place `chromedriver.exe` in the project root or add it to your PATH.
* Update the script path in `main.py` if needed:

```python
service = Service(executable_path="chromedriver.exe")
```

---

## ▶️ Usage

Run the scraper in two steps:

```bash
python get_cookies.py
python main.py
```

The script will:

1. Open LinkedIn and restore your login session using cookies.
2. Perform a job search for **"python developer" in India**.
---

## 📂 Output

* **Console** → Prints job list (titles, companies, etc.)
* **File** → `jobDetail.txt` contains the latest detailed job description

**Example:**

```
Software Engineer – Microsoft
Location: Bangalore
Posted: 1 day ago

Description:
We are looking for a Python developer...
```

---

## 🔧 Customization

You can modify the search filters in `main.py`:

```python
params = {
    "distance": 100,            # Search radius
    "f_TPR": "r86400",          # Posted in last 24h
    "geoId": 102713980,         # India
    "keywords": "python developer"  # Search keyword
}
```

* Change `keywords`, `geoId`, or `distance` to match your needs.
  👉 [LinkedIn geoId list reference](https://www.linkedin.com/help/linkedin/answer/a507663)

---

## ⚠️ Notes

* **Use responsibly**: LinkedIn actively detects and may block aggressive scraping.
* Add **delays/random sleep** if scraping at scale.
* Works best with **headless mode** (optional with Selenium).
* If cookies expire, regenerate **`linkedin_cookies.pkl`**.

---

## 📌 Roadmap

* [ ] Store scraped jobs in **CSV/JSON** format
* [ ] Add **multi-keyword / multi-location** scraping
* [ ] Integrate with **resume parser** module


---

## 📄 License

This project is part of the **Joven ecosystem**.
Distributed under the **MIT License**.
