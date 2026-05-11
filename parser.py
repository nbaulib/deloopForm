from datetime import date


def transform_entry(entry):
    # replaces "today" with today's date
    if entry["date"].strip().lower() == "today":
        entry["date"] = date.today().strftime("%m%d%Y")

    # standardize entriess
    if entry["issues"].strip().lower() in ("no issues", "none", ""):
        entry["issues"] = "None"

    if entry["inventory"].strip().lower() in ("no materials", "none", ""):
        entry["inventory"] = "None"

    return entry


# pasrse from string
def parse_text(raw: str):
    # split into lines
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    # defaults in first 3 lines
    email, name, school = lines[:3]

    # formats email line
    # <mailto:nico@email.com|nico@email.com> -> nico@email.com
    if "mailto:" in email and "|" in email:
        start = email.index(":") + 1
        end = email.index("|")
        email = email[start:end].strip()

    # rest of form
    data = lines[3:]
    entries = []
    for i in range(0, len(data), 6):
        p = data[i : i + 6]
        if len(p) == 6:
            entries.append(
                transform_entry(
                    {
                        "workshop": p[0],
                        "date": p[1],
                        "week": p[2],
                        "summary": p[3],
                        "issues": p[4],
                        "inventory": p[5],
                    }
                )
            )
    return email, name, school, entries
