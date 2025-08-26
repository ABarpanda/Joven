from urllib.parse import urlencode

base_url = "https://www.linkedin.com/jobs/search/"
params = {
    "distance": 100,
    "f_TPR": "r86400",  # last 24 hours
    "geoId": 102713980, # India
    "keywords": "python developer"
}

url = f"{base_url}?{urlencode(params)}"