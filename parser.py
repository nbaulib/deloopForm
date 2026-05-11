from datetime import date as Date

def transform_header(email, date):
    # <mailto:nico@email.com|nico@email.com> -> nico@email.com
    if "mailto:" in email and "|" in email:
        start = email.index(":") + 1
        end = email.index("|")
        email = email[start:end].strip()

    # replace "today"
    if date.strip().lower() == "today":
        date = Date.today().strftime("%m%d%Y")

    return email, date


def transform_entry(entry):
    if entry["issues"].strip().lower() in ("no issues", "none", ""):
        entry["issues"] = "None"

    if entry["inventory"].strip().lower() in ("no materials", "none", ""):
        entry["inventory"] = "None"

    return entry


def parse_text(raw: str):
    # split into lines
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    # defaults in first 4 lines
    email, name, school, date = lines[:4]

    # clean headers
    email, date = transform_header(email, date)

    # rest of form
    data = lines[4:]
    entries = []
    for i in range(0, len(data), 5):
        p = data[i : i + 5]
        if len(p) == 5:
            entries.append(
                transform_entry(
                    {
                        "workshop": p[0],
                        "week": p[1],
                        "summary": p[2],
                        "issues": p[3],
                        "inventory": p[4],
                    }
                )
            )
    return email, name, school, date, entries
