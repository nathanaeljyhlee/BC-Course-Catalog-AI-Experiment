import json
import csv
import re
import os

# --- CONFIG ---
INPUT_JSON = "json_results/output.json"
OUTPUT_CSV = "parsed_results/courses_with_fixes.csv"
os.makedirs("parsed_results", exist_ok=True)

# --- LOAD OCR OUTPUT ---
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

courses = []

# --- REGEX PATTERNS ---
course_code_pattern = re.compile(r'^[A-Z]{4,6}\d{5,6}$')  # e.g. SCWK993253
school_heading_pattern = re.compile(r'^# (.+)$')
term_pattern = re.compile(r'^(Spring|Summer|Fall|Winter)\s+\d{4}$')

current_school = None

prefix_to_school = {
    "LAWS": "Law School",
    "MFIN": "Carroll School of Management",
    "ACCT": "Carroll School of Management",
    "MARK": "Carroll School of Management",
    "MGMT": "Carroll School of Management",
    "SCWK": "School of Social Work",
    "SOWK": "School of Social Work",
    "THEO": "School of Theology and Ministry",
    "EDUC": "Lynch School of Education",
    "ECON": "Morrissey College of Arts and Sciences",
    "BIOL": "Morrissey College of Arts and Sciences",
    "HIST": "Morrissey College of Arts and Sciences",
    "ENGL": "Morrissey College of Arts and Sciences",
    "PHIL": "Morrissey College of Arts and Sciences",
    "CHEM": "Morrissey College of Arts and Sciences",
    "PHYS": "Morrissey College of Arts and Sciences"
}

# --- PARSE ---
for page in data["pages"]:
    lines = page["markdown"].splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        school_match = school_heading_pattern.match(line)
        if school_match:
            possible_school = school_match.group(1).strip()
            if any(kw in possible_school for kw in ["School", "College", "Courses"]):
                current_school = possible_school

        if course_code_pattern.match(line):
            course_prefix = line[:4]
            inferred_school = prefix_to_school.get(course_prefix, "")

            if current_school and inferred_school and inferred_school != current_school:
                school = inferred_school
            else:
                school = current_school or inferred_school or ""

            course = {
                "school": school,
                "course_code": line,
                "course_title": "",
                "instructor": "",
                "term": "",
                "credits": "",
                "description": ""
            }

            # --- Course Title ---
            for offset in range(1, 4):
                if i + offset < len(lines):
                    possible_title = lines[i + offset].strip()
                    if possible_title and not possible_title.startswith(("Credits:", "Room", "Prerequisites:", "Corequisites:", "Comments:", "Status:")) and not course_code_pattern.match(possible_title):
                        course["course_title"] = possible_title
                        i += offset
                        break

            # --- Instructor ---
            i += 1
            if i < len(lines):
                line2 = lines[i].strip()
                if not any(k in line2 for k in ["Spring", "Summer", "Fall", "Winter"]):
                    course["instructor"] = line2
                    i += 1

            # --- Term ---
            if i < len(lines) and term_pattern.match(lines[i].strip()):
                course["term"] = lines[i].strip()
                i += 1
            else:
                for offset in range(0, 4):
                    if i + offset < len(lines):
                        term_candidate = lines[i + offset].strip()
                        if term_pattern.match(term_candidate):
                            course["term"] = term_candidate
                            i += offset + 1
                            break

            # --- Description ---
            description_lines = []
            while i < len(lines) and not lines[i].startswith("Credits:"):
                if not lines[i].startswith(("Prerequisites:", "Corequisites:", "Comments:", "Status:", "Cross-listed with:")):
                    description_lines.append(lines[i].strip())
                i += 1
            course["description"] = " ".join(description_lines)

            # --- Credits ---
            if i < len(lines) and lines[i].startswith("Credits:"):
                course["credits"] = lines[i].replace("Credits:", "").strip()
                i += 1

            courses.append(course)
        else:
            i += 1

# --- EXPORT TO CSV ---
with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "school", "course_code", "course_title", "instructor", "term", "credits", "description"
    ])
    writer.writeheader()
    writer.writerows(courses)

print(f"✅ Parsed {len(courses)} courses → {OUTPUT_CSV}")
