# imports
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import smtplib, ssl

# chrome driver setup
options = webdriver.ChromeOptions()
options.add_argument('headless')
e_options = webdriver.ChromeOptions()

# dictionaries
month_order = {
    "January": 0,
    "February": 1,
    "March": 2,
    "April": 3,
    "May": 4,
    "June": 5,
    "July": 6,
    "August": 7,
    "September": 8,
    "October": 9,
    "November": 10,
    "December": 11,
    "ABCXYZ": 12
}

month_length = {
    "January": 7,
    "February": 7,
    "March": 5,
    "April": 5,
    "May": 3,
    "June": 4,
    "July": 4,
    "August": 6,
    "September": 9,
    "October": 7,
    "November": 8,
    "December": 8
}

# functions
def getDate(driver): # returns date list in format of [str(month), int(day), int(year)]
    frame_text = driver.page_source
    for key in month_order:
        if key in frame_text:
            month_index = frame_text.find(key)
            if frame_text.find(" EDT") != -1:
                year = frame_text[frame_text.find(" EDT")-4:frame_text.find(" EDT")]
            else:
                year = frame_text[frame_text.find(" EST")-4:frame_text.find(" EST")]
            date = [frame_text[month_index:month_index+month_length[key]], int(frame_text[month_index+month_length[key]+1:month_index+month_length[key]+3]), int(year)]
            return date

def earlierDate(d1, d2):
    if d1[2] < d2[2]:
        return d1
    elif d1[2] > d2[2]:
        return d2
    if month_order[d1[0]] < month_order[d2[0]]:
        return d1
    elif month_order[d1[0]] > month_order[d2[0]]:
        return d2
    if d1[1] < d2[1]:
        return d1
    elif d1[1] > d2[1]:
        return d2
    else:
        return None

def emailLogin(): # returns the driver for sendEmail function to use
    driver = webdriver.Chrome(options=e_options)
    driver.get('https://account.proton.me/login?language=en')
    sleep(10)
    username = driver.find_element_by_id('username')
    username.send_keys("automatedtest@protonmail.com")
    sleep(1)
    password = driver.find_element_by_id('password')
    password.send_keys(INSERT_PASSWORD) # password hidden
    sleep(1)
    password.submit()
    sleep(20)
    return driver
    
def sendEmail(location, date, driver, subject, message):
    try:
        actions = ActionChains(driver)
        actions.send_keys('n')
        actions.pause(3)
        actions.send_keys(INSERT_EMAIL) # this can be any email that you want to receive a notification
        actions.pause(1)
        for i in range(4):
            actions.send_keys(Keys.TAB)
            actions.pause(2)
        actions.send_keys(subject)
        actions.pause(1)
        actions.send_keys(Keys.TAB)
        actions.pause(0.2)
        actions.send_keys(message)
        actions.pause(1)
        for i in range(15):
            actions.send_keys(Keys.TAB)
            actions.pause(1)
        actions.pause(3)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        sleep(2)
        print("Message sent.")
        driver.quit()
    except Exception as e:
        print(f"Unable to send email. Error: {e}")

def getAppointmentPage(driver):
    # Step 1
    driver.get('https://www27.state.nj.us/tc/driverlogin.do?url=njmvcdtclient')
    licence_id = driver.find_element_by_name("licenseNumber")
    licence_id.send_keys(INSERT_LICENSE_NUMBER) # license number
    validation = driver.find_element_by_name("permitNumber")
    validation.send_keys(INSERT_PERMIT_NUMBER) # permit number
    submit = driver.find_element_by_class_name("button")
    submit.click()
    # Step 2
    sleep(2)
    email = driver.find_element_by_name("EmailAddress")
    email.send_keys(INSERT_EMAIL) # email
    phone = driver.find_element_by_name("PhoneNumber")
    phone.send_keys(INSERT_PHONE_NUMBER) # phone number
    submit = driver.find_element_by_class_name("button")
    submit.click()
    # Step 3
    sleep(1)
    actions = ActionChains(driver)
    for i in range(2):
        actions.send_keys(Keys.TAB)
        actions.pause(0.2)
    actions.pause(0.5)
    actions.send_keys("07869")
    actions.pause(0.5)
    for i in range(3):
        actions.send_keys(Keys.TAB)
        actions.pause(0.2)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    # Step 4
    driver.find_elements_by_tag_name("font") # This exists only for the next line to work
    driver.get("https://www27.state.nj.us/tc/NJ_SelectOptions.do?method=nextLocation&domObject=appointment&domProperty=select_location&LocationId=18&LocationName=Randolph+VIS&reschedule=false&cmd=donext&process=driver_testing_client&process2=driver_testing_client&entry=&level=&urlstring=njmvcdtclient&step=Select+Location&locationSearchType=1&location_zip=07869&location_countyId=1&location_city=&location_location=")
    sleep(1)
    first_button = driver.find_elements_by_class_name("f12b")[11]
    first_button.click()
    let_it_load = ActionChains(driver)
    let_it_load.pause(1.5)
    let_it_load.perform()
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    
def main():
    current = ["ABCXYZ", 99, 9999]
    driver = webdriver.Chrome(options=options)
    getAppointmentPage(driver)
    location = "Randolph"
    while True:
        if earlierDate(getDate(driver), current) == getDate(driver):
            current = getDate(driver)
            print(f"GOOD NEWS! NEW EARLY {location.upper()} DATE: Week of {current[0]} {current[1]}, {current[2]}")
            subject = f"{location} {month_order[current[0]]+1}/{current[1]}/{current[2]-2000}"
            if current[0] == "August" or current[0] == "September":
                d = emailLogin()
                sendEmail(location, current, d, subject, "")
        elif earlierDate(getDate(driver), current) == current:
            print("DATE TAKEN")
            current = getDate(driver)
        else:
            print("There was no date change outside of the current week.")
            sleep(55)
        driver.refresh()
        sleep(5)
        driver.find_elements_by_tag_name("font") # This exists only for the next line to work
        driver.get("https://www27.state.nj.us/tc/NJ_SelectOptions.do?method=nextLocation&domObject=appointment&domProperty=select_location&LocationId=18&LocationName=Randolph+VIS&reschedule=false&cmd=donext&process=driver_testing_client&process2=driver_testing_client&entry=&level=&urlstring=njmvcdtclient&step=Select+Location&locationSearchType=1&location_zip=07869&location_countyId=1&location_city=&location_location=")
        sleep(1)
        first_button = driver.find_elements_by_class_name("f12b")[11]
        first_button.click()
        let_it_load = ActionChains(driver)
        let_it_load.pause(1.5)
        let_it_load.perform()
        driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))

main()
