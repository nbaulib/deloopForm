from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed

from parser import *
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()])
log = logging.getLogger(__name__)

FORM_URL = "https://forms.gle/WZoLLTF86axQ99ux5"

# HELPERS

# small and big text area
def fill_text(wait, label, value):
    field = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            f'//div[@role="listitem"][.//*[contains(normalize-space(.), "{label}")]]//input | '
            f'//div[@role="listitem"][.//*[contains(normalize-space(.), "{label}")]]//textarea',
        ))
    )
    field.clear()
    field.send_keys(value)

# dropdown
def select_dropdown(wait, driver, label, option):
    # locates dropdown and clicks
    dropdown = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            f'//div[@role="listitem"][.//*[contains(normalize-space(.), "{label}")]]//div[@role="listbox"]',
        ))
    )
    dropdown.click()
    
    # locates desired option and clicks
    option_xpath = f'(//div[@role="option"]//span[normalize-space()="{option}"])[last()]'
    target_option = wait.until(
        EC.visibility_of_element_located((By.XPATH, option_xpath))
    )
    target_option.click()
    
    # wait until dropdown invisible (closed)
    wait.until(
        EC.invisibility_of_element_located(
            (By.XPATH, '//div[@role="listbox"][@aria-expanded="true"]')
        )
    )

# button
def click_button(wait, label):
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//span[text()="{label}"]/ancestor::div[@role="button"]')
        )
    )
    btn.click()

# SUMBITING

# submits 1 entry
def submit_entry(i, email, name, school, date, entry):
    # log.info(f"Entry {i} starting: {entry['workshop']}")
    start = time.time()
    
    #runs without browser ui
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(FORM_URL)

        # PAGE 1
        fill_text(wait, "Email", email)
        fill_text(wait, "Name", name)
        select_dropdown(wait, driver, "School Site", school)
        select_dropdown(wait, driver, "Workshop Name", entry["workshop"])
        fill_text(wait, "Date", date)
        select_dropdown(wait, driver, "week of the course", entry["week"])
        fill_text(wait, "What did you cover", entry["summary"])
        fill_text(wait, "Any issues", entry["issues"])
        click_button(wait, "Next")

        # PAGE 2
        fill_text(wait, "What materials are", entry["inventory"])
        click_button(wait, "Submit")

        # wait for confirmation page 
        wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Submit another response"))
        )
        
        elapsed = time.time() - start
        log.info(f"{entry['workshop']} done in {elapsed:.1f}s")
        return i, None  # success
    
    except Exception as e:
        log.error(f"Entry {entry['workshop']} FAILED: {e}", exc_info=True)
        return i, e     # error
    
    finally:
        driver.quit()

# handles batch
def submit_batch(raw, say):
    # slack message to vars
    email, name, school, date, entries = parse_text(raw)

    total = len(entries)
    
    say("Starting ...")

    # one thread per entry
    with ThreadPoolExecutor(max_workers=total) as pool:
        futures = {
        pool.submit(submit_entry, i, email, name, school, date, entry): (i, entry)
        for i, entry in enumerate(entries)
    }
    for future in as_completed(futures):
        i, entry = futures[future]
        idx, err = future.result()
        if err:
            say(f"{entry['workshop']} {i + 1}/{total} FAILED")
        else:
            say(f"{entry['workshop']} {i + 1}/{total} submitted.")

    say("End.")