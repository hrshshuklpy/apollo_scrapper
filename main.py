import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup ChromeDriver
chrome_driver_path = '/Users/harshshukla/Downloads/chromedriver-mac-arm64/chromedriver'
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)


def login_to_apollo(email, password):
    """Login to Apollo using the provided credentials."""
    driver.get('https://app.apollo.io/#/login?redirectTo=https%3A%2F%2Fapp.apollo.io%2F%23%2F')

    # Wait for email input field to be visible
    email_input = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))

    # Locate and fill the email and password fields
    password_input = driver.find_element(By.NAME, 'password')

    # Input email and password
    email_input.send_keys(email)
    password_input.send_keys(password)

    # Locate and click the "Log In" button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="login-button"]')
    login_button.click()

    # Wait for the page to load after login
    wait.until(EC.url_changes('https://app.apollo.io/#/login?redirectTo=https%3A%2F%2Fapp.apollo.io%2F%23%2F'))


def open_new_tab_and_navigate(url):
    """Open a new tab and navigate to the given URL."""
    driver.execute_script("window.open('');")  # Open new tab
    driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
    driver.get(url)

    # Wait for elements to be loaded
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'zp_hWv1I')))


def click_reveal_buttons():
    """Find and click all the 'Access email' buttons to reveal emails and phone numbers."""
    # Find all buttons with the class that reveals emails and phone numbers
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.zp_qe0Li.zp_FG3Vz.zp_QMAFM.zp_h2EIO')

    # Iterate through the buttons and click the ones that have the text 'Access email'
    for index, button in enumerate(buttons):
        try:
            # Check if the button contains the specific text 'Access email'
            if 'Access email' in button.text:
                # Simulate human behavior with a random sleep between 1 to 2 seconds
                delay = random.uniform(1, 4)
                time.sleep(delay)

                # Scroll the button into view (in case it's out of the viewport)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

                # Add another small delay after scrolling to mimic human-like pauses
                time.sleep(random.uniform(0.5, 1))

                # Click the button to reveal the email
                button.click()

                print(f"Clicked 'Access email' button {index + 1}/{len(buttons)}")

        except Exception as e:
            print(f"Could not click button {index + 1}: {e}")

    # Wait a short moment to ensure all clicks have revealed the data
    time.sleep(10)


def extract_data_from_elements():
    """Extract required data from the first 25 elements on the page."""
    data = []
    parent_elements = driver.find_elements(By.CLASS_NAME, 'zp_hWv1I')

    for index, parent_element in enumerate(parent_elements[:25]):
        try:
            name = parent_element.find_element(By.CSS_SELECTOR, '.zp_p2Xqs.zp_v565m').text
        except:
            name = 'N/A'

        try:
            job_title = parent_element.find_element(By.CLASS_NAME, 'zp_xvo3G').text
        except:
            job_title = 'N/A'

        try:
            company = parent_element.find_element(By.CLASS_NAME, 'zp_PaniY').text
        except:
            company = 'N/A'

        try:
            email = parent_element.find_element(By.CLASS_NAME, 'zp_hdyyu').text
        except:
            email = 'N/A'

        try:
            phone_number = parent_element.find_element(By.CLASS_NAME, 'zp_CCHXh').text
        except:
            phone_number = 'N/A'

        try:
            social_link_element = parent_element.find_element(By.CSS_SELECTOR, '.zp_uzcP0 a')
            social_link = social_link_element.get_attribute('href')
        except:
            social_link = 'N/A'

        try:
            num_employees = parent_element.find_element(By.CLASS_NAME, 'zp_mE7no').text
        except:
            num_employees = 'N/A'

        try:
            industry = parent_element.find_element(By.CLASS_NAME, 'zp_CEZf9').text
        except:
            industry = 'N/A'

        # Add the extracted data to the list
        data.append({
            'Name': name,
            'Job Title': job_title,
            'Company': company,
            'Email': email,
            'Phone Number': phone_number,
            'Social Link': social_link,
            '# Employees': num_employees,
            'Industry': industry
        })

    return data


def save_data_to_csv(data, file_name='apollo_data.csv'):
    """Save the extracted data to a CSV file."""
    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Data saved to '{file_name}'.")


def paginate_and_scrape(start_page, end_page):
    """Navigate through the pages between start_page and end_page, scrape data, and go to the next page."""
    for page_num in range(start_page, end_page + 1):
        try:
            # Open the pagination dropdown
            dropdown = driver.find_element(By.CSS_SELECTOR, 'div.zp_Knvs5')
            dropdown.click()

            # Wait for pagination options to load
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.zp_T8nat')))

            # Find and click the correct page number
            page_element = driver.find_element(By.CSS_SELECTOR, f'div[data-value="{page_num}"]')
            page_element.click()

            # Wait for the page to load after clicking
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'zp_hWv1I')))
            print(f"Scraping page {page_num}")

            # Click all buttons to reveal the emails and phone numbers
            click_reveal_buttons()

            # Extract data from the page
            extracted_data = extract_data_from_elements()

            # Save the data to a CSV file (appending data)
            save_data_to_csv(extracted_data, f'apollo_data_page_{page_num}.csv')

        except Exception as e:
            print(f"Error on page {page_num}: {e}")


try:
    # Hardcoded credentials (replace these with your actual email and password)
    email = 'abc@gmail.com'
    password = 'abc123'

    # Log in to Apollo
    login_to_apollo(email, password)

    # Open new tab and navigate to the desired URL
    url = 'https://app.apollo.io/#/people?page=1&sortAscending=false&sortByField=%5Bnone%5D&qPersonPersonaIds[]=6720f40de7f2ac05cc0cf70d&organizationTradingStatus[]=private&organizationLatestFundingStageCd[]=0&organizationLatestFundingStageCd[]=13&organizationLatestFundingStageCd[]=10&organizationLatestFundingStageCd[]=1&organizationLatestFundingStageCd[]=2&existFields[]=organization_revenue_in_thousands_int'
    open_new_tab_and_navigate(url)

    # Provide the page range (for example, 1 to 5)
    start_page = 3
    end_page = 6

    # Scrape data from the given range of pages
    paginate_and_scrape(start_page, end_page)

finally:
    # Always close the driver, even if something goes wrong
    driver.quit()