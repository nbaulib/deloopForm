from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time

driver = webdriver.Chrome(options=webdriver.ChromeOptions())
wait = WebDriverWait(driver, 20)

form_url = "https://forms.gle/PPZAe66rHKbqyUpz5"
driver.get(form_url)

today = date.today()
    
def e_clickable(role, text, type):
    if type == "listbox":
        xpath = (
        f'//div[@role="listitem"]'
        f'[.//span[text()="{text}"]]'
        f'//div[@role="{type}"]'
    )
    else: 
        xpath = (
            f'//div[@role="listitem"]'
            f'[.//span[text()="{text}"]]'
            f'//input[@type="{type}"]'
        )
        
    if type == "date":
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    else:
        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

name_field = e_clickable("listitem", "Name", "text")
name_field.send_keys("Nico")

# Date
date_field = e_clickable("listitem", "Date", "date")
date_field.send_keys(today.strftime("%m-%d-%Y"))

# School dropdown
school_dropdown = e_clickable("listitem", "School", "listbox")
school_dropdown.click()

option = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    '//div[@role="option"]//span[text()="a"]'
)))
option.click()

time.sleep(1)

# Submit
submit_button = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    '//span[text()="Submit"]/ancestor::div[@role="button"]'
)))
submit_button.click()

# Wait for confirmation page
wait.until(EC.presence_of_element_located((
    By.XPATH, '//*[contains(text(),"response has been recorded")]'
)))

driver.close()

# https://codewithtj.blogspot.com/2024/01/python-script-to-fill-google-form.html
# https://www.geeksforgeeks.org/python/automatically-filling-multiple-responses-into-a-google-form-with-selenium-and-python/

# make structured logging for debug