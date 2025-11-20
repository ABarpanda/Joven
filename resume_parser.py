import re
import json
import torch
import PyPDF2

TECH_KEYWORDS = [
    "python", "java", "c++", "c", "c#", "javascript", "typescript", "go", "golang", "rust",
    "matlab", "r", "ruby", "swift", "kotlin", "php", "scala", "sql", "bash", "shell",
    "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "xgboost", "lightgbm",
    "pandas", "numpy", "scipy", "opencv", "transformers", "huggingface", "spacy",
    "react", "next.js", "nextjs", "node.js", "node", "express", "django", "flask", "fastapi",
    "docker", "kubernetes", "aws", "azure", "gcp", "firebase", "postgresql", "mysql", "mongodb",
    "redis", "graphql", "rest", "restful", "html", "css", "sass", "tailwind", "bootstrap",
    "git", "github", "gitlab", "jira", "confluence", "vs code", "vscode", "intellij", "eclipse",
    "jenkins", "circleci", "travis", "ansible", "terraform", "prometheus",
    "spark", "hadoop", "airflow", "kafka",
    "pytest", "unittest", "junit", "selenium",
    "arduino", "raspberry pi", "esp32", "tinkercad", "verilog", "vhdl",
    "nlp", "computer vision", "cv", "deep learning", "machine learning", "reinforcement learning",
    "signal processing", "embedded", "microcontroller", "iot"
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "team player", "problem solving", "problem-solving",
    "time management", "adaptability", "creativity", "critical thinking", "collaboration",
    "mentoring", "coaching", "presentation", "public speaking", "organization", "analytical"
]

SKILL_KEYWORDS = {
    "python", "java", "c", "c++", "javascript", "typescript", "react",
    "node.js", "node", "express", "sql", "mysql", "postgresql", "mongodb",
    "html", "css", "docker", "kubernetes", "git", "linux", "aws", "gcp",
    "machine learning", "deep learning", "nlp", "computer vision",
    "pytorch", "tensorflow", "scikit-learn", "opencv", "pandas", "numpy"
}

SEED_SKILLS = sorted(set([k.lower() for k in TECH_KEYWORDS + SOFT_SKILLS]))
EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'(\+?\d{1,3}[\s\-\.])?(?:\(?\d{2,4}\)?[\s\-\./]?)?\d{6,12}')
YEAR_RE = re.compile(r'(?:(?:19|20)\d{2})')
YEARS_EXPERIENCE_RE = re.compile(r'(\d+(?:\.\d+)?)(?:\+)?\s*(?:years|yrs|year)', re.I)
DEGREE_RE = re.compile(r'\b(bachelor|master|b\.?tech|btech|b\.?e|b\.?sc|m\.?tech|mtech|m\.?sc|phd|doctor|diploma)\b', re.I)
PROJECT_SECTION_HEADERS = re.compile(r'^(projects?|personal projects|selected projects)\b', re.I | re.M)
EDU_SECTION_HEADERS = re.compile(r'^(education|academic background)\b', re.I | re.M)
CERT_SECTION_HEADERS = re.compile(r'^(certifications|certificates|licenses)\b', re.I | re.M)
ACHIEV_SECTION_HEADERS = re.compile(r'^(achievements|awards|honors)\b', re.I | re.M)
SKILLS_SECTION_HEADERS = re.compile(r'^(skills|technical skills|technical expertise|skills & tools)\b', re.I | re.M)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from a PDF file."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        return f"ERROR_PDF: {str(e)}"
    return text

def find_name_by_heuristic(text: str) -> str:
    """Heuristic: first non-empty line if it contains multiple capitalized words (likely name)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    first = lines[0]
    if EMAIL_RE.search(first) or PHONE_RE.search(first):
        for ln in lines[:5]:
            if not EMAIL_RE.search(ln) and not PHONE_RE.search(ln) and len(ln.split())<=5:
                first = ln
                break
    tokens = first.split()
    cap_count = sum(1 for t in tokens if t[:1].isupper())
    if cap_count >= 1 and len(tokens) <= 5:
        return first
    m = re.search(r'^\s*name[:\-]\s*(.+)$', text, re.I | re.M)
    if m:
        return m.group(1).strip()
    return first

def extract_emails(text: str) -> list[str]:
    found = EMAIL_RE.findall(text)
    return list(dict.fromkeys(found))

def extract_phones(text: str) -> list[str]:
    found = PHONE_RE.findall(text)
    raw = re.findall(r'(\+?\d[\d\-\s\(\)\.]{7,}\d)', text)
    cleaned = []
    for p in raw:
        p_clean = re.sub(r'[^\d\+]', '', p)
        if 7 <= len(re.sub(r'\D', '', p_clean)) <= 15:
            cleaned.append(p_clean)
    return list(dict.fromkeys(cleaned))

def extract_section_by_header(text: str, header_re: re.Pattern) -> str:
    """
    Return the text following the first header matched by header_re up to the next blank-line+header-like line or until 8000 chars.
    """
    m = header_re.search(text)
    if not m:
        return ""
    start = m.end()
    tail = text[start:]
    stop = len(tail)
    for hdr in [PROJECT_SECTION_HEADERS, EDU_SECTION_HEADERS, CERT_SECTION_HEADERS, ACHIEV_SECTION_HEADERS, SKILLS_SECTION_HEADERS]:
        if hdr == header_re:
            continue
    nxt = re.search(r'\n\s*\n(?=[A-Za-z]{3,})', tail)
    if nxt:
        stop = nxt.start()
    snippet = tail[:stop]
    return snippet.strip()

def find_projects(text: str) -> list[dict[str,str]]:
    projects = []
    proj_section = extract_section_by_header(text, PROJECT_SECTION_HEADERS)
    candidates = proj_section if proj_section else text
    lines = [ln.rstrip() for ln in candidates.splitlines() if ln.strip()]
    i = 0
    while i < len(lines):
        ln = lines[i]

        m = re.match(r'^(?:-|\*|\d+\.)\s*(.+?)(?:[:\-–—]\s*(.+))?$', ln)
        if m:
            title_candidate = m.group(1).strip()
            desc_candidate = m.group(2).strip() if m.group(2) else ""
    
            j = i+1
            extra = []
            while j < len(lines) and not re.match(r'^(?:-|\*|\d+\.)\s+', lines[j]):
        
                if re.match(r'^[A-Z][\w\s]{0,40}[:\-–—]$', lines[j]):
                    break
                extra.append(lines[j])
                j += 1
            desc = (desc_candidate + " " + " ".join(extra)).strip()
            projects.append({"title": title_candidate, "description": desc})
            i = j
            continue

        m2 = re.match(r'^([A-Z][\w &\-\:\(\)]+?)\s*[:\-–—]\s*(.+)$', ln)
        if m2 and len(m2.group(1).split()) <= 8:
            projects.append({"title": m2.group(1).strip(), "description": m2.group(2).strip()})
            i += 1
            continue

        if len(ln.split()) <= 6 and ln[0].isupper():
    
            if i+1 < len(lines) and len(lines[i+1].split())>3:
                desc_lines = []
                j = i+1
                while j < len(lines) and not (lines[j][0].isupper() and len(lines[j].split()) <= 6):
                    desc_lines.append(lines[j])
                    j += 1
                projects.append({"title": ln, "description": " ".join(desc_lines).strip()})
                i = j
                continue
        i += 1
    seen = set()
    unique = []
    for p in projects:
        t = p['title'].strip().lower()
        if t not in seen and p['title'].strip():
            unique.append({"title": p['title'].strip(), "description": p['description'].strip()})
            seen.add(t)
    return unique

def extract_education(text: str) -> list[dict[str, str]]:
    DEGREE_KEYWORDS = [
        r"b\.?tech", r"bachelor", r"m\.?tech", r"master",
        r"engineering", r"class xii", r"class 12", r"class x",
        r"higher secondary", r"secondary", r"cbse", r"pcm"
    ]

    STOP_HEADERS = [
        "projects", "experience", "achievements",
        "certifications", "skills", "technical skills",
        "extracurricular", "volunteer", "work experience"
    ]


    edu_section = extract_section_by_header(text, EDU_SECTION_HEADERS)

    if not edu_section:

        lines = text.splitlines()
    else:
        lines = edu_section.splitlines()

    lines = [ln.strip() for ln in lines if ln.strip()]

    cleaned = []
    for ln in lines:
        if any(h.lower() in ln.lower() for h in STOP_HEADERS):
            break
        cleaned.append(ln)

    filtered = []
    for ln in cleaned:
        if (
            re.search("|".join(DEGREE_KEYWORDS), ln, flags=re.I) or
            re.search(r"\b(university|college|institute|school|nit)\b", ln, flags=re.I)
        ):
            filtered.append(ln)

    merged = []
    buffer = ""
    for ln in filtered:
        if re.search("|".join(DEGREE_KEYWORDS), ln, flags=re.I):
    
            if buffer:
                merged.append(buffer.strip())
            buffer = ln
        else:
    
            buffer += " " + ln
    if buffer:
        merged.append(buffer.strip())

    results = []
    for entry in merged:
        year_match = re.findall(r"(19|20)\d{2}", entry)
        year = year_match[-1] if year_match else ""


        m = re.match(
            r"(?P<degree>.*?)(?: at |, |- )(?:the )?(?P<inst>[^,–\-]+)",
            entry,
            flags=re.I
        )

        if m:
            degree = m.group("degree").strip()
            inst = m.group("inst").strip()

    
            degree = re.sub(r"\(.*?\)", "", degree).strip()
            inst = re.sub(r"\(.*?\)", "", inst).strip()
        else:
    
            degree = entry
            inst = ""

        results.append({
            "degree": degree,
            "institution": inst,
            "year": year
        })

    unique = []
    seen = set()
    for e in results:
        key = (e["degree"].lower(), e["institution"].lower(), e["year"])
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique

def extract_certifications(text: str) -> list[str]:
    cert_section = extract_section_by_header(text, CERT_SECTION_HEADERS)
    lines = []
    if cert_section:
        lines = [ln.strip() for ln in cert_section.splitlines() if ln.strip()]
    else:

        lines = [ln.strip() for ln in text.splitlines() if re.search(r'\b(certificat|certified|course:)\b', ln, re.I)]
    cleaned = []
    for ln in lines:

        cleaned.append(re.sub(r'\s*\(?\b(?:19|20)\d{2}\)?$', '', ln).strip())
    return list(dict.fromkeys([c for c in cleaned if c]))

def extract_achievements(text: str) -> list[str]:
    ach_section = extract_section_by_header(text, ACHIEV_SECTION_HEADERS)
    lines = []
    if ach_section:
        lines = [ln.strip() for ln in ach_section.splitlines() if ln.strip()]
    else:

        lines = [ln.strip() for ln in text.splitlines() if re.search(r'\b(award|won|prize|rank|achiev|selected|runner-up)\b', ln, re.I)]
    filtered = []
    for ln in lines:
        if len(ln.split()) < 3:
            continue
        filtered.append(ln)
    return list(dict.fromkeys(filtered))

def infer_years_of_experience(text: str) -> str:
    yrs = YEARS_EXPERIENCE_RE.findall(text)
    nums = []
    for y in yrs:
        try:
            nums.append(float(y))
        except:
            pass
    if nums:

        mx = max(nums)

        if float(mx).is_integer():
            return str(int(mx))
        else:
            return str(mx)
    date_ranges = re.findall(r'((?:19|20)\d{2})\s*(?:-|to|–|—)\s*((?:19|20)\d{2})', text)
    intervals = []
    for s,e in date_ranges:
        try:
            intervals.append(abs(int(e) - int(s)))
        except:
            pass
    if intervals:
        mx = max(intervals)
        return str(mx)
    return ""

def extract_skills(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    extracted = set()
    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            extracted.add(skill)
    return sorted(extracted)

def find_skill_mentions(text: str, seed_list: list[str]) -> list[str]:
    found = set()
    low = text.lower()
    for token in seed_list:

        if re.search(r'\b' + re.escape(token) + r'\b', low):
            found.add(token)
    return list(found)

def extract_additional_tech_from_text(text: str) -> list[str]:
    tokens = set(re.findall(r'\b[A-Za-z0-9\+\#\.\_]{2,30}\b', text))
    extras = []
    for t in tokens:
        tl = t.lower()
        if tl in SEED_SKILLS:
            continue
        if any(ch.isupper() for ch in t[1:]) or re.search(r'\d', t) or re.search(r'js$|py$|lib$|cv$|kit$', t.lower()):
            extras.append(t)
    return extras

def normalize_skill(s: str) -> str:
    s = s.strip()
    s = re.sub(r'[\(\)\[\]\{\}]', '', s)
    s = re.sub(r'\b(version|v)\s*\d+(\.\d+)*', '', s, flags=re.I)
    s = re.sub(r'[^A-Za-z0-9\+\#\.\s\-/]+', ' ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip()

def dedupe_skills_with_pytorch(skill_list: list[str]) -> list[str]:
    """
    Demonstration PyTorch usage: create simple hashed-int tensor for each normalized skill,
    use torch.unique to deduplicate and then map back. This is a fuzzy-ish numeric dedupe,
    but we still rely primarily on normalized string dedupe too.
    """
    normed = [normalize_skill(s).lower() for s in skill_list if s and s.strip()]
    expanded = []
    for s in normed:
        for delim in ['/', '&', ' and ', ',']:
            if delim in s:
                pieces = [p.strip() for p in re.split(r'[\/&,]| and ', s) if p.strip()]
                if len(pieces) > 1:
                    expanded.extend(pieces)
                    break
        else:
            expanded.append(s)
    final = []
    for s in expanded:
        if len(s) >= 1:
            final.append(s)
    def stable_hash(x):
        return sum(ord(c) for c in x) % 2_000_000_000
    ints = [stable_hash(s) for s in final]
    tensor = torch.tensor(ints, dtype=torch.int64)
    uniq_vals, inverse = torch.unique(tensor, return_inverse=True)
    unique_skills = []
    seen = set()
    for idx, val in enumerate(uniq_vals.tolist()):

        for i, s in enumerate(final):
            if stable_hash(s) == val:
                candidate = final[i]
                if candidate not in seen:
                    unique_skills.append(candidate)
                    seen.add(candidate)
                break
    return unique_skills

def extract_contact_details(text: str) -> tuple[str,str,str]:
    name = find_name_by_heuristic(text)
    emails = extract_emails(text)
    phones = extract_phones(text)
    email = emails[0] if emails else ""
    phone = phones[0] if phones else ""
    return name, email, phone

def parse_resume(text: str) -> dict:
    result = {
        "Full Name": "",
        "Email": "",
        "Phone": "",
        "Skills": [],
        "Total Years of Experience": "",
        "Education": [],
        "Achievements": [],
        "Certifications": [],
        "Projects": []
    }

    name, email, phone = extract_contact_details(text)
    result["Full Name"] = name
    result["Email"] = email
    result["Phone"] = phone

    projects = find_projects(text)
    result["Projects"] = [{"title": p["title"], "description": p["description"]} for p in projects]

    result["Education"] = extract_education(text)

    result["Certifications"] = extract_certifications(text)

    result["Achievements"] = extract_achievements(text)

    result["Total Years of Experience"] = infer_years_of_experience(text)

    skills = []

    skills_section_items = extract_skills(text)
    skills.extend(skills_section_items)

    deduped = dedupe_skills_with_pytorch(skills)
    cleaned = []
    for s in deduped:
        s2 = s.strip()
        s2 = re.sub(r'^\W+|\W+$', '', s2)
        if len(s2) < 2:
            continue

        if re.match(r'^(experience|years|year|graduation)$', s2, re.I):
            continue
        cleaned.append(s2)

    seen = set()
    final_skills = []
    for s in cleaned:
        key = s.lower()
        if key not in seen:
            final_skills.append(s)
            seen.add(key)

    canonical_rewrites = {
        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "scikit learn": "scikit-learn",
        "scikit-learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "python": "Python",
        "java": "Java",
        "c++": "C++",
        "c#": "C#",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "react": "React",
        "node.js": "Node.js",
        "node": "Node.js",
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "aws": "AWS",
        "gcp": "GCP",
        "azure": "Azure",
        "sql": "SQL",
        "html": "HTML",
        "css": "CSS",
        "git": "Git",
    }
    pretty_skills = []
    for s in final_skills:
        sl = s.lower()
        pretty = canonical_rewrites.get(sl, s)
        pretty_skills.append(pretty)

    result["Skills"] = pretty_skills

    if not result["Projects"]:

        projects_raw = re.findall(r'project[:\-]\s*(.+)', text, re.I)
        for pr in projects_raw:
            result["Projects"].append({"title": pr.split('-')[0].strip(), "description": pr.strip()})

    result["Education"] = result["Education"] if result["Education"] else []
    result["Achievements"] = result["Achievements"] if result["Achievements"] else []
    result["Certifications"] = result["Certifications"] if result["Certifications"] else []
    result["Projects"] = result["Projects"] if result["Projects"] else []

    return result

def main(cv_path = "cv.pdf"):
    resume_text = extract_text_from_pdf(cv_path)
    parsed = parse_resume(resume_text)
    print(json.dumps(parsed, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main("cv.pdf")