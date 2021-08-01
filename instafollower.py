from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from random import randint
import requests
import time
wd = "./WebDriver/chromedriver.exe"
PROCESS_RUNNING =False
COUNT = 0;
TAG_COUNT = 0;


def random_client_selector(client_count: int):
    random_dropdown_element_num = randint(1,client_count)
    return random_dropdown_element_num


def internet_connection_test(url,timeout):
    try:
        request = requests.get(url,timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False
    else:
        return True


def processRunStatus():
    return PROCESS_RUNNING


class InstaFollower:
    def __init__(self,driver_path: str):
        global PROCESS_RUNNING
        PROCESS_RUNNING = True
        self.running = PROCESS_RUNNING
        self.igpath = "https://www.instagram.com"
        try:

            self.driver = webdriver.Chrome(executable_path=driver_path)
            self.driver.implicitly_wait(10)
        except:
            self.is_driver_present = False
            print("no webdriver found")
        else:
            self.is_driver_present = True

    def login(self,id,pwd):
        driver = self.driver
        driver.get('https://www.instagram.com/')
        driver.maximize_window()
        username = driver.find_element(By.XPATH, '//input[@name="username"]')
        username.send_keys(id)
        password = driver.find_element(By.XPATH, '//input[@name="password"]')
        password.send_keys(pwd)
        login_link = driver.find_element(By.XPATH, "//*[contains(text(),'Log In')]")
        IS_STATUS_PANEL_OPEN = False
        login_link.click()
        try:
            alert_message = driver.find_element_by_xpath('//*[@id="slfErrorAlert"]')
        except:
            return True
        else:
            print(alert_message.text)
            return False

    def search_with_tag(self,hash_tag: str,msg): # provided with hash tag value
        self.driver.implicitly_wait(10) # sets the implicit wait so as to wait for 10sec in case of failure
        driver = self.driver    # sets the driver parameter
        time.sleep(10)  # waits for 10 sec
        # searches for the search input element
        try:
            search = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[1]/div/span[2]')
            search.click() # clicks the search input to activate the field
        except:
            driver.refresh()
            return
        time.sleep(1) # waits for 1 sec
        # searches for point to type in the tag value
        search_key = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        search_key.send_keys(hash_tag) # types the hash tag result
        # searches for all the elements in the search drop down
        search_dropdown_items = driver.find_elements_by_xpath('//*[@id="react-root"]/section/nav/div[2]/'
                                                              'div/div/div[2]/div[3]/div/div[2]/div/div/a')
        # returns the random client number
        random_client = random_client_selector(len(search_dropdown_items))
        check = self.reach_client(random_client,msg)
        if check == "limitation reached":
            return "new"

    def reach_client(self,t_num: int,msg):
        driver = self.driver
        time.sleep(3)
        try:
            tag_target_element = driver.find_element_by_xpath(
            f'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[{t_num}]/a')
            tag_target_element.click()
        except :
            return

        time.sleep(4)
        try:
            error = driver.find_element_by_xpath('/html/body/div/div[1]/div/div/h2')
        except :
            self.post_message(msg)
            time.sleep(2)
            driver.back()
            time.sleep(2)
            return
        else:
            driver.get("https://www.instagram.com/accounts/onetap/?next=%2F")
            return "limitation reached"

    def element_of_most_recent(self):
        driver = self.driver
        driver.implicitly_wait(10)
        most_recent_post = driver.find_element_by_xpath('//*[@id="react-root"]/section/main'
                                                        '/article/div[2]/div/div[1]/div[1]/a')
        most_recent_post.click()

    def hashtags(self):
        tags = ['#music','#newmusic','#rapmusic','#rapartist']
        return tags

    def post_message(self,msg):
        driver = self.driver

        recent_post = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/'
                                                   'article/div[2]/div/div[1]/div[1]/a/div[1]')
        recent_post.click()
        try:
            text_area = driver.find_element_by_tag_name('textarea')
            # This block of Code comments on the targeted post
            # text_area.click()
            # text_area_comment = driver.find_element_by_tag_name('textarea')
            # text_area_comment.send_keys(msg[0][0])
            # post_btn = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article'
            #                                         '/div[3]/section[3]/div/form/button[2]')
            # post_btn.click()
        except NoSuchElementException:
            pass
        time.sleep(10)
        driver.refresh()
        driver.back()

    def logout(self):
        driver= self.driver
        profile_div = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav'
                                                   '/div[2]/div/div/div[3]/div/div[5]/span')
        profile_div.click()
        time.sleep(2)
        lg_out = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]'
                                              '/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div/div')
        lg_out.click()

    def abort_web(self):
        global PROCESS_RUNNING
        PROCESS_RUNNING = False
        processRunStatus()
        print(PROCESS_RUNNING)
        self.driver.quit()

    def driver_quit(self):
        self.driver.quit()