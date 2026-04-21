from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time

start = time.time()

driver = webdriver.Chrome(options=webdriver.ChromeOptions())
wait = WebDriverWait(driver, 20)

form_url = "https://forms.gle/PPZAe66rHKbqyUpz5"
driver.get(form_url)

today = date.today()

XPATH_TEMPLATES = {
    "listbox": (
        '//div[@role="listitem"]'
        '[.//span[text()="{label}"]]'
        '//div[@role="listbox"]'
    ),
    "text": (
        '//div[@role="listitem"]'
        '[.//span[text()="{label}"]]'
        '//input[not(@aria-hidden="true")]'
    ),
    "option": (
        '//div[@role="option"]//span[text()="{label}"]'
    ),
}
    
def get_xpath(label, input_type):
    template = XPATH_TEMPLATES.get(input_type)
    if not template:
        raise ValueError(f"Unsupported input type: {input_type}")
    return template.format(label=label)
        
def wait_clickable(xpath):
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def wait_visible(xpath):
    return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

name_field = wait_clickable(get_xpath("Name", "text"))
name_field.click()
name_field.send_keys("Nico")

# Date
date_field = wait_visible(get_xpath("Date", "text"))
date_field.send_keys(today.strftime("%m%d%Y"))

# School dropdown
school_dropdown = wait_clickable(get_xpath("School","listbox"))
school_dropdown.click()

option = wait_clickable('//div[@role="option"]//span[text()="a"]')
option.click()

time.sleep(1) # does not work if i comment this out

# Submit
submit_button = wait_clickable('//span[text()="Submit"]/ancestor::div[@role="button"]')
submit_button.click()

# Wait for confirmation page
wait_visible('//*[contains(text(),"response has been recorded")]')

driver.close()
end = time.time()

runtime = end - start
print(round(runtime,3), "seconds")

# https://codewithtj.blogspot.com/2024/01/python-script-to-fill-google-form.html
# https://www.geeksforgeeks.org/python/automatically-filling-multiple-responses-into-a-google-form-with-selenium-and-python/