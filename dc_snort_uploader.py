#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import argparse

parser = argparse.ArgumentParser(description="Upload Snort to Defense center Sourcefire Snort")
parser.add_argument("-f", "--file", help="Snort file to upload", required=True)
parser.add_argument("-s", "--sourcefire", help="Sourcefire ip or hostname", required=True)
parser.add_argument("-u", "--user", help="Sourcefire user account", required=True)
parser.add_argument("-p", "--password", help="Sourcefire user password", required=True)
parser.add_argument("-i", "--uuid", help="Intrusion Policy UUID that will contains new signatures", required=True)

args = parser.parse_args()

SNORT_FILE_PATH = args.file
SNORT_FILE_NAME = SNORT_FILE_PATH.split("/")[-1]
SOURCEFIRE = args.sourcefire

oldname=""

driver = webdriver.Firefox()

def Authentication(user,password):
    '''
        Authenticate on the server web access
    '''
    driver.get("https://" + SOURCEFIRE)
    time.sleep(2)
    elem = driver.find_element_by_id("username")
    elem.send_keys(user)
    time.sleep(2)
    elem2 = driver.find_element_by_id("password")
    elem2.send_keys(password)
    time.sleep(2)
    elem3 = driver.find_element_by_name("logon")
    elem3.submit()
    time.sleep(2)

try:
    Authentication(args.user, args.password)

    #Go to Import page
    time.sleep(20)
    driver.get("https://" + SOURCEFIRE + "/DetectionPolicy/rules/rulesimport.cgi")
    time.sleep(2)
    elem4 = driver.find_element_by_xpath("/html/body/div[6]/div[3]/form[1]/div/table/tbody/tr[3]/td/input[1]")
    elem4.click()
    time.sleep(2)

    #upload the file
    elem5 = driver.find_element_by_xpath("/html/body/div[6]/div[3]/form[1]/div/table/tbody/tr[3]/td/input[2]")
    elem5.send_keys(SNORT_FILE_PATH)
    time.sleep(2)
    elem6 = driver.find_element_by_xpath("/html/body/div[6]/div[3]/form[1]/div/table/tbody/tr[5]/td[2]/input")
    elem6.click()
    time.sleep(40)

except Exception:
    print 'Failed to load last SNORT rules in ' + SNORT_FILE_NAME + ' (navigation problem)'
    driver.close()
    exit()

try:
    notifmsg = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[2]/div")
    if 'Error' in notifmsg.get_attribute('innerHTML'):
        raise Exception("Error","Bad Snort file.")

except NoSuchElementException: #Normal behaviour (no error message displayed)
    driver.close()
    time.sleep(10)

except Exception:
    print 'Failed to load last SNORT rules in ' + SNORT_FILE_NAME + '. Some rules are bad.'
    driver.close()
    exit()

#Second part : Activate the policy

driver = webdriver.Firefox()

try:
    Authentication(args.user, args.password)
    driver.get('https://' + SOURCEFIRE + '/DetectionPolicy/ids.cgi?uuid=' + args.uuid + '#rules')
    time.sleep(50)
    elem7 = driver.find_element_by_class_name("filterTextBox")
    elem7.send_keys('Message:"[MISP]"')
    elem7.send_keys(Keys.RETURN)
    time.sleep(10)
    elem8 = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div[4]/div/div[1]/div/div/div[3]/div/div/div[7]/div/div/div/div[1]/table/tbody/tr[2]/td[1]/span/input")
    elem8.click()
    time.sleep(10)
    elem9 = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div[4]/div/div[1]/div/div/div[3]/div/div/div[5]/div/div[2]/div/table/tbody/tr/td[1]")
    elem9.click()
    time.sleep(10)
    elem10 = driver.find_element_by_xpath("/html/body/div[9]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td")
    elem10.click()
    time.sleep(15)
    driver.close()
    time.sleep(10)
except Exception:
    print 'Failed to activate MISP SNORT rules in the policy'
    driver.close()
    exit()

#Third part : Commit policy changes

driver = webdriver.Firefox()

try:
    Authentication(args.user, args.password)
    time.sleep(2)
    driver.get('https://'+ SOURCEFIRE +'/DetectionPolicy/ids.cgi?uuid=' + args.uuid + '#policy')
    time.sleep(10)
    elem12 = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div[4]/div/div[1]/div/div/div[3]/div/div[6]/button[1]")
    elem12.click()
    time.sleep(10)
    elem13 = driver.find_element_by_xpath("/html/body/div[10]/div/table/tbody/tr[2]/td[2]/div/div/div[2]/table/tbody/tr[1]/td/div/textarea")
    elem13.send_keys('New MISP rules : ' + SNORT_FILE_NAME)
    time.sleep(10)
    elem14 = driver.find_element_by_xpath("/html/body/div[10]/div/table/tbody/tr[2]/td[2]/div/div/div[2]/table/tbody/tr[3]/td/div/button[1]")
    elem14.click()
    time.sleep(60)
    driver.close()
except Exception:
    print 'Failed to commit policy'
    driver.close()
    exit()

print 'Auto Upload successfull of Snort rules : ' + SNORT_FILE_NAME

exit()
