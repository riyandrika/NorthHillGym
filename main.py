from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
from telegram_bot import bot, booking_date, booking_time, booking_hour, chat_id

PATH = r"C:\Program Files (x86)\msedgedriver.exe"
driver = webdriver.Edge(executable_path=PATH)

url = "https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg="
driver.get(url)
driver.maximize_window()
username = driver.find_element(by=By.NAME, value="UserName")
username.send_keys(os.environ["NTU_NETWORK_USERNAME"])
ok_user = driver.find_element(by=By.NAME, value="bOption").click()
password = driver.find_element(by=By.NAME, value="PIN")
password.send_keys(os.environ["NTU_NETWORK_PASSWORD"])
ok_pw = driver.find_element(by=By.NAME, value="bOption").click()

cancel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sd4")))
cancel.click()
existing_bookings = driver.find_elements(by=By.XPATH, value="//input[@type='checkbox']")
if len(existing_bookings) < 2:
    driver.find_element(by=By.ID, value="sd3").click()
    north_hill = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[8]/td/input')))
    north_hill.click()

    slots = [f"0{i}" for i in range(1, 10)]
    slots.extend(str(i) for i in range(10, 21))
    idx = 0
    while True:
        idx = idx % 20
        slot_xpath = f'//input[@value="1NG2NG{slots[idx]}{booking_date}{booking_time}"]'
        idx += 1

        try:
            slot_element = driver.find_element(by=By.XPATH, value=slot_xpath)
            driver.implicitly_wait(.5)
            slot_element.click()
            break

        except:
            sleep(1)

        confirm = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='bOption' and @value='Confirm']")))
        confirm.click()
        driver.implicitly_wait(5)
        driver.quit()
        bot.send_message(chat_id=chat_id, text=f"Booking for {booking_date} @ {booking_hour} SUCCESSFUL")

else:
    driver.quit()
    bot.send_message(chat_id=chat_id, text="Booking limit exceeded")
    # TODO fetch the current bookings