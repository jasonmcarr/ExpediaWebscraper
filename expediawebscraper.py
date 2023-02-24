# Library imports
import os
import pandas as pd
import time
import schedule
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import selenium.common.exceptions
from bs4 import BeautifulSoup




# Generating the first csv file (comment out if already generated)
#df_header = pd.DataFrame(columns=['Airline', 'Time', 'Price'])
#path = r'C:\Users\Jason\Desktop\Data Analytics Portfolio Projects\Python Web Scraping\Expedia Webscraper'
#df_header.to_csv(path + '/Expedia_BZN_PHX_Flight_Information.csv',index=False)



# Function for retrieving and formatting flight data
def scraper():

    print('Updating CSV...')

    # Driver options
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Opening webpage according to input variable
    url = ('https://www.expedia.com/Flights-Search?leg1=from%3ABozeman%20(BZN%20-%20Gallatin%20Field)%2Cto%3APhoenix%2C%20AZ%20(PHX-Sky%20Harbor%20Intl.)%2Cdeparture%3A3%2F21%2F2023TANYT&mode=search&options=carrier%3A*%2Ccabinclass%3A%2Cmaxhops%3A1%2Cnopenalty%3AN&pageId=0&passengers=adults%3A1%2Cchildren%3A0%2Cinfantinlap%3AN&trip=oneway')
    driver.get(url)

    # Interaction with and error handling for first pop up
    try:
        popup1_wait = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//body')))
    except selenium.common.exceptions.TimeoutException:
        pass
    except selenium.common.exceptions.NoSuchElementException:
        pass
    else:
        driver.find_element(By.XPATH, '//body').click()

    # Interaction with and error handling for second pop up
    try:
        popup2_wait = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 uitk-toolbar-button-v2 uitk-toolbar-button-v2-icon-only"]')))
    except selenium.common.exceptions.TimeoutException:
        pass
    except selenium.common.exceptions.NoSuchElementException:
        pass
    else:
        driver.find_element(
            By.XPATH, '//button[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 uitk-toolbar-button-v2 uitk-toolbar-button-v2-icon-only"]').click()

    # Locating Expedia information containers and extracting data
    try:
        flight_info_wait = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-test-id="intersection-observer"]')))
    except selenium.common.exceptions.TimeoutException:
        print('Timeout Error for Flight Info')
    except selenium.common.exceptions.NoSuchElementException:
        print('Unable to locate flight information')
    else:
        list_flight = []
        flight_info = driver.find_elements(
            By.XPATH, '//div[@data-test-id="intersection-observer"]')

        for WebElement in flight_info:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML, 'html.parser')

            # Building and formatting information list
            temp_info = elementSoup.find(
                'h4', {'class': 'uitk-heading uitk-heading-7'})
            list_flight.append(str(temp_info))

        # Closing browser
        driver.close()
        driver.quit()

        # Formatting data by removing htlm element
        formatting = [char.replace('<h4 class="uitk-heading uitk-heading-7">', '')
                      for char in list_flight]
        formatting2 = [char.replace('</h4>', '') for char in formatting]
        formatted_list_flight = formatting2[1:]
        # Format of list:['Delta (Airlines) flight departing at 6:49pm from $150']

    # Building pandas dataframe for flight information
    list_airline, list_time, list_price = ([] for i in range(3))

    for string in formatted_list_flight:
        s = string.split()
        for element in s:
            if element == 'Airlines':
                s.remove('Airlines')
        list_airline.append(s[0])
        list_time.append(s[4])
        list_price.append(s[6])

    df = pd.DataFrame(data={'Airline': list_airline,
                      'Time': list_time, 'Price': list_price})
    df.to_csv(r'C:\Users\Jason\Desktop\Data Analytics Portfolio Projects\Python Web Scraping\Expedia Webscraper\Expedia_BZN_PHX_Flight_Information.csv',
              mode='a', index=False, header=False)

    today = date.today()
    print('CSV updated on', today)


print('--Webscraper Initialized--')
scraper()
# Run the scraper function every day at 12:00
#schedule.every().day.at("12:00").do(scraper)

#while True:
#    schedule.run_pending()
#    time.sleep(1)

