"""
Adds the 'category' column to the careers table and categorizes all existing careers.
Run once: python fix_categories.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "nexgenu.db")

# Comprehensive categorization map
CAREER_CATEGORIES = {
    # ── CSE Core ─────────────────────────────────
    "Software Engineer":               "Core Careers",
    "Backend Developer":               "Core Careers",
    "Frontend Developer":              "Core Careers",
    "Full Stack Developer":            "Core Careers",
    "Mobile App Developer":            "Core Careers",
    "DevOps Engineer":                 "Core Careers",
    "Cloud Architect":                 "Core Careers",

    # ── IT Core ──────────────────────────────────
    "Systems Administrator":           "Core Careers",
    "Network Engineer":                "Core Careers",
    "Cybersecurity Analyst":           "Core Careers",
    "IT Support Specialist":           "Core Careers",
    "Database Administrator":          "Core Careers",
    "Cloud Security Engineer":         "Core Careers",

    # ── AI & DS Core ─────────────────────────────
    "Machine Learning Engineer":       "Core Careers",
    "Data Scientist":                  "Core Careers",
    "Data Engineer":                   "Core Careers",
    "NLP Engineer":                    "Core Careers",
    "Computer Vision Engineer":        "Core Careers",
    "Generative AI Engineer":          "Core Careers",

    # ── ECE Core ─────────────────────────────────
    "VLSI Design Engineer":            "Core Careers",
    "Telecommunications Engineer":     "Core Careers",
    "Network Architect":               "Core Careers",
    "Hardware Engineer":               "Core Careers",
    "Signal Processing Engineer":      "Core Careers",
    "RF Engineer":                     "Core Careers",

    # ── EEE Core ─────────────────────────────────
    "Power Systems Engineer":          "Core Careers",
    "Electrical Design Engineer":      "Core Careers",
    "Protection Engineer":             "Core Careers",
    "Substation Engineer":             "Core Careers",
    "Transmission Engineer":           "Core Careers",
    "Distribution Engineer":           "Core Careers",
    "Renewable Energy Engineer":       "Core Careers",
    "Solar Engineer":                  "Core Careers",
    "Wind Energy Engineer":            "Core Careers",
    "PLC Programmer":                  "Core Careers",
    "SCADA Engineer":                  "Core Careers",
    "Industrial Automation Engineer":  "Core Careers",
    "Control Systems Engineer":        "Core Careers",

    # ── EEE → IT & Digital ───────────────────────
    "Embedded Engineer":               "IT & Digital Careers",
    "Robotics Engineer":               "IT & Digital Careers",
    "IoT Engineer":                    "IT & Digital Careers",
    "AI Engineer":                     "IT & Digital Careers",
    "Data Analyst":                    "IT & Digital Careers",

    # ── Mechanical Core ──────────────────────────
    "Mechanical Design Engineer":      "Core Careers",
    "Automotive Engineer":             "Core Careers",
    "Manufacturing Engineer":          "Core Careers",
    "Thermal Engineer":                "Core Careers",
    "Mechatronics Engineer":           "Core Careers",
    "HVAC Engineer":                   "Core Careers",

    # ── Civil Core ───────────────────────────────
    "Structural Engineer":             "Core Careers",
    "Construction Manager":            "Core Careers",
    "Geotechnical Engineer":           "Core Careers",
    "Transportation Engineer":         "Core Careers",
    "Environmental Engineer":          "Core Careers",
    "Urban Planner":                   "Core Careers",

    # ── Any Branch → IT & Digital ────────────────
    "Business Analyst":                "IT & Digital Careers",
    "Product Manager":                 "IT & Digital Careers",
    "Scrum Master":                    "IT & Digital Careers",
    "Technical Writer":                "IT & Digital Careers",
    "QA Automation Engineer":          "IT & Digital Careers",
}

GOV_PSU_CAREERS = [
    # EEE/ECE PSU
    ("TNEB / TANGEDCO Engineer",        "eee", "Government & PSU Careers"),
    ("PGCIL Transmission Engineer",      "eee", "Government & PSU Careers"),
    ("BHEL Electrical Engineer",         "eee", "Government & PSU Careers"),
    ("NTPC Power Plant Engineer",        "eee", "Government & PSU Careers"),
    ("TNEB Junior Engineer",             "eee", "Government & PSU Careers"),
    # Civil PSU
    ("PWD Civil Engineer",               "civil", "Government & PSU Careers"),
    ("NHAI Highway Engineer",            "civil", "Government & PSU Careers"),
    ("BRO Border Roads Engineer",        "civil", "Government & PSU Careers"),
    # Mechanical PSU
    ("DRDO Research Engineer",           "mech", "Government & PSU Careers"),
    ("HAL Aerospace Engineer",           "mech", "Government & PSU Careers"),
    # IT/CS PSU
    ("ISRO Software Engineer",           "cse", "Government & PSU Careers"),
    ("ECIL Electronics Engineer",        "ece", "Government & PSU Careers"),
]


def fix_categories():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Add column if not exists
    try:
        cur.execute("ALTER TABLE careers ADD COLUMN category TEXT DEFAULT 'Core Careers'")
        print("✅ Added 'category' column to careers table.")
    except sqlite3.OperationalError:
        print("ℹ️  'category' column already exists.")

    # Update categories
    updated = 0
    for name, cat in CAREER_CATEGORIES.items():
        cur.execute("UPDATE careers SET category = ? WHERE name = ?", (cat, name))
        updated += cur.rowcount

    conn.commit()
    print(f"✅ Updated {updated} careers with correct categories.")

    # Print summary
    cur.execute("SELECT category, COUNT(*) FROM careers GROUP BY category")
    rows = cur.fetchall()
    print("\nCategory Summary:")
    for row in rows:
        print(f"  {row[0] or 'Uncategorized'}: {row[1]} careers")

    conn.close()
    print("\n✅ Done!")


if __name__ == "__main__":
    fix_categories()
