from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.remote.webdriver import WebDriver
import os

import chrome_handler
import helper_funcs
import sys

chrome_handler.start_chrome()

service = Service(os.getcwd() + "/chromedriver.exe")
print(os.getcwd() + "/chromedriver")
chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=chrome_options)
helper_fn = helper_funcs.HelperFn(driver)


def check_guildlines():
    guidlines_xpath = "//*[contains(text(), 'Tips for getting started')]"
    helper_fn.wait_for_element(guidlines_xpath)
    if helper_fn.is_element_present(guidlines_xpath):
        guidlines_close_xpath = "//*[contains(text(), 'Okay, let’s go')]"
        guidlines_close = helper_fn.find_element(guidlines_close_xpath)
        guidlines_close.click()
    else:
        print("No guidlines found")

def start_chat_gpt():
    driver.maximize_window()
    driver.get("https://chat.openai.com/chat")
    #if login page is present
    time.sleep(2)
    login_msg_xpath = "//*[contains(text(), 'Log in with your OpenAI account to continue')]"
    login_page = helper_fn.is_element_present(login_msg_xpath)
    if login_page:
        login_btn_xpath = "//*[@class='btn relative btn-primary']//*[contains(text(), 'Log in')]"
        helper_fn.wait_for_element(login_btn_xpath)
        login_button = helper_fn.find_element(login_btn_xpath)
        login_button.click()
        
        time.sleep(2)
        #google login
        google_btn_xpath = "//*[@data-provider='google']"
        helper_fn.wait_for_element(google_btn_xpath)
        google_btn = helper_fn.find_element(google_btn_xpath)
        google_btn.click()

        time.sleep(2)
        #select mail
        gmail_xpath = "//*[contains(text(), 'PRIYANSHU PATEL')]" ## change this to your google account name.
        helper_fn.wait_for_element(gmail_xpath)
        gmail = helper_fn.find_element(gmail_xpath)
        gmail.click()

    else:
        print("Already logged in")

    #check for guidlines
    check_guildlines()

def Receive_limit():
    limit_xpath="//*[@class='mb-2 py-2 px-3 border text-gray-600 rounded-md text-sm dark:text-gray-100 border-red-500 bg-red-500/10']"
    button_xpath="//*[@class='btn relative btn-primary m-auto']"
    response_xpath = "//*[@class='markdown prose w-full break-words dark:prose-invert light']"
    if helper_fn.is_element_present(limit_xpath):
        print('Receive Limit,please wait 30 minutes')
        time.sleep(1800)
        regenerate_btn=helper_fn.find_element(button_xpath)
        regenerate_btn.click()
        times=1
        time.sleep(5)
        while helper_fn.is_element_present(limit_xpath):
            time.sleep(60)
            print('Has waited {} seconds'.format(1800+60*times))
            times+=1
            regenerate_btn = helper_fn.find_element(button_xpath)
            regenerate_btn.click()
            time.sleep(5)
        regenrate_xpath = '//*[@class="absolute p-1 rounded-md md:bottom-3 md:p-2 md:right-3 dark:hover:bg-gray-900 dark:disabled:hover:bg-transparent right-2 gizmo:dark:disabled:bg-white gizmo:disabled:bg-black gizmo:disabled:opacity-10 disabled:text-gray-400 enabled:bg-brand-purple gizmo:enabled:bg-black text-white gizmo:p-0.5 gizmo:border gizmo:border-black gizmo:rounded-lg gizmo:dark:border-white gizmo:dark:bg-white bottom-1.5 transition-colors disabled:opacity-40"]'
        helper_fn.wait_for_element(regenrate_xpath, 10)
        driver.execute_script("window.scrollBy(0,1000)")
        if helper_fn.is_element_present(response_xpath):
            response = helper_fn.find_elements(response_xpath)[-1]
        time.sleep(5)
        print('Cancel Limit , Continue Talking')
        return True,response.text
    else:
        return False,''



def make_gpt_request(text):
    time.sleep(3)
    text_area_xpath = "//*[@id='prompt-textarea']"
    helper_fn.wait_for_element(text_area_xpath,5)
    if helper_fn.is_element_present(text_area_xpath):
        text_area = helper_fn.find_element(text_area_xpath)
        text_area.send_keys(text)

        #send button
        send_btn_xpath = "//*[@data-testid='send-button']"
        helper_fn.wait_for_element(send_btn_xpath,3)
        send_btn = helper_fn.find_element(send_btn_xpath)
        send_btn.click()

    time.sleep(20)
    #waiting for response
    response_xpath = "//*[@class='markdown prose w-full break-words dark:prose-invert light']"
    regenrate_xpath = '//*[@class="absolute p-1 rounded-md md:bottom-3 md:p-2 md:right-3 dark:hover:bg-gray-900 dark:disabled:hover:bg-transparent right-2 gizmo:dark:disabled:bg-white gizmo:disabled:bg-black gizmo:disabled:opacity-10 disabled:text-gray-400 enabled:bg-brand-purple gizmo:enabled:bg-black text-white gizmo:p-0.5 gizmo:border gizmo:border-black gizmo:rounded-lg gizmo:dark:border-white gizmo:dark:bg-white bottom-1.5 transition-colors disabled:opacity-40"]'
    helper_fn.wait_for_element(regenrate_xpath,5)
    driver.execute_script("window.scrollBy(0,1000)")
    if helper_fn.is_element_present(response_xpath):
        response = helper_fn.find_elements(response_xpath)[-1]
        # print(response.text)
        return response.text # will return all the texual information under that perticular xpath



def stop_chat_gpt():
    driver.close()
    chrome_handler.kill_chrome()
    
if __name__ == "__main__":
    start_chat_gpt()
    
    try:
        while True:
            req = input("Enter text: ")
            if req == "i quit!":
                break
            resp = make_gpt_request(req)
            print(resp)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")
    finally:
        stop_chat_gpt()
        exit(0)