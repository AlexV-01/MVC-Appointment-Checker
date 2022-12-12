# imports
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# chrome driver setup
options = webdriver.ChromeOptions()
options.add_argument('headless')
e_options = webdriver.ChromeOptions()
# functions
def getDate(driver, location): # returns date
    bodyText = driver.find_element_by_tag_name('body').text
    fromLocation = bodyText[bodyText.find(location):]
    filtered = fromLocation[fromLocation[1:].find(location):fromLocation.find("AM")+2]
    if filtered.find("No Appointments Available") != -1 and filtered.find(":") > filtered.find("No Appointments Available"):
        return "No Appointments Available"
    elif filtered.find("No Appointments Available") != -1 and filtered.find(":") < filtered.find("No Appointments Available"):
        return filtered[filtered.find(":")+2:filtered.find(":")+12]
    date = filtered[filtered.find(":")+2:filtered.find(":")+12]
    return date

def earlierDate(d1, d2):
    if d1 == "No Appointments Available" or d2 == "No Appointments Available":
        return None
    if int(d1[6:]) < int(d2[6:]):
        return d1
    elif int(d1[6:]) > int(d2[6:]):
        return d2
    if int(d1[:2]) < int(d2[:2]):
        return d1
    elif int(d1[:2]) > int(d2[:2]):
        return d2
    if int(d1[3:5]) < int(d2[3:5]):
        return d1
    elif int(d1[3:5]) > int(d2[3:5]):
        return d2
    return None

def emailLogin(): # returns the driver for sendEmail function to use
    driver = webdriver.Chrome(options=e_options)
    driver.get('https://account.proton.me/login?language=en')
    sleep(2)
    username = driver.find_element_by_id('username')
    username.send_keys(BOT_EMAIL) # this is the email address of the bot. Using protonmail
    password = driver.find_element_by_id('password')
    password.send_keys(PASSWORD_HIDDEN)
    password.submit()
    sleep(15)
    return driver
    
def sendEmail(location, date, driver):
    try:
        actions = ActionChains(driver)
        actions.send_keys('n')
        actions.pause(1)
        actions.send_keys(INSERT_EMAIL) # this can be any email that you want to receive a notification
        actions.pause(0.5)
        for i in range(4):
            actions.send_keys(Keys.TAB)
            actions.pause(0.5)
        actions.send_keys("New Knowledge Test Spot!")
        actions.pause(0.5)
        actions.send_keys(Keys.TAB)
        actions.pause(0.2)
        actions.send_keys(f"Congratulations! A new spot has opened up at {location}! The date is {date}. Enjoy!")
        actions.pause(1)
        for i in range(15):
            actions.send_keys(Keys.TAB)
            actions.pause(0.1)
        actions.pause(5)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        sleep(2)
        print("Message sent.")
        driver.quit()
    except Exception as e:
        print(f"Unable to send email. Error: {e}")

def main():
    oak = "99/99/9999"
    nb = "99/99/9999"
    lodi = "99/99/9999"
    wayne = "99/99/9999"
    pat = "99/99/9999"
    driver = webdriver.Chrome(options=options)
    driver.get('https://telegov.njportal.com/njmvc/AppointmentWizard/19')
    while True:
        new = False
        if earlierDate(getDate(driver, "Oakland"), oak) == getDate(driver, "Oakland"):
            oak = getDate(driver, "Oakland")
            print(f"NEW EARLY OAKLAND DATE: {oak}")
            new = True
            d = emailLogin()
            sendEmail("Oakland", oak, d)
        if earlierDate(getDate(driver, "North Bergen"), nb) == getDate(driver, "North Bergen"):
            nb = getDate(driver, "North Bergen")
            print(f"NEW EARLY NORTH BERGEN DATE: {nb}")
            new = True
            d = emailLogin()
            sendEmail("North Bergen", nb, d)
        if earlierDate(getDate(driver, "Lodi"), lodi) == getDate(driver, "Lodi"):
            lodi = getDate(driver, "Lodi")
            print(f"NEW EARLY LODI DATE: {lodi}")
            new = True
            d = emailLogin()
            sendEmail("Lodi", lodi, d)
        if earlierDate(getDate(driver, "Wayne"), wayne) == getDate(driver, "Wayne"):
            wayne = getDate(driver, "Wayne")
            print(f"NEW EARLY WAYNE DATE: {wayne}")
            new = True
            d = emailLogin()
            sendEmail("Wayne", wayne, d)
        if earlierDate(getDate(driver, "Paterson"), pat) == getDate(driver, "Paterson"):
            pat = getDate(driver, "Paterson")
            print(f"NEW EARLY PATERSON DATE: {pat}")
            new = True
            d = emailLogin()
            sendEmail("Paterson", pat, d)
        if not new:
            print("There were no new early dates.")
        sleep(60)
        driver.refresh()

main()
