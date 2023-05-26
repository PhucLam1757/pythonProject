import time
import cv2 as cv
import numpy as np
from selenium import webdriver
import chromedriver_autoinstaller as ca
from collections import Counter
from selenium.webdriver.common.action_chains import ActionChains

import undetected_chromedriver as uc

ca.install()
chrome_version = ca.get_chrome_version().split('.')[0]
options = uc.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

url = "https://www.douyin.com/user/MS4wLjABAAAAEVIWemha_VzH2n29CtetgHBSmjSANeqTCsAKQv0Ktio"
driver.get(url)


def solve_captcha():
    global x_offset
    i = 1
    while True:
        try:
            img = driver.find_element_by_xpath("//*[@id='captcha-verify-image']")
            if img.get_attribute('src'):
                time.sleep(1)
                img.screenshot('foo.png')
                break
        except Exception as e:
            print('wait img loader.....')
            try:
                driver.find_element_by_xpath("//div[contains(text(), 'Authorize')]")
                return {'success': 1}
            except Exception as e:
                raise e

    img = cv.imread('foo.png')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 15, 0.05, 1)
    corners = np.int0(corners)

    x_Array = []
    for i in corners:
        x, y = i.ravel()
        cv.circle(img, (x, y), 3, 255, -1)
        #lấy tọa độ các điểm bên phải tâm ảnh để kéo
        if x > 75:
            x_Array.append(x)

    x_Array.sort()

    print(x_Array)

    # slider = driver.find_element_by_class_name("captcha_verify_slide--slidebar")
    slider = driver.find_element_by_xpath("//*[@id='captcha_container']/div/div[3]/div[1]")

    source = driver.find_element_by_xpath("//*[@id='secsdk-captcha-drag-wrapper']/div[2]")
    source_location = source.location
    source_size = source.size

    array = [170, 345, 400, 400, 345]
    unic = Counter(x_Array)
    print(unic)
    for x in x_Array:
        if unic[x] > 1:
            x_offset = x - 8
            break

    y_offset = 0
    action = ActionChains(driver)
    try:
        steps_count = 5
        step = (x_offset) / steps_count
        # print(step)
        # print(y_offset)
        # print(x_offset)
        act_1 = action.click_and_hold(source)
        for x in range(0, steps_count):
            act_1.move_by_offset(step, y_offset)
        time.sleep(1 )
        act_1.release().perform()

        msg = driver.find_element_by_class_name('msg').find_element_by_tag_name('div').text
        while msg == '':
            msg = driver.find_element_by_class_name('msg').find_element_by_tag_name('div').text
        print(msg)

        if '验证通过' in msg or 'complete' in msg:
            return {'success': 1}
        else:
            return {'success': 0}

    except Exception as e:
        print(e)


try:
    time.sleep(2)

    driver.find_element_by_xpath("//*[@id='captcha-verify-image']")
    i = 1
    while True:
        print(f"lần thứ {i}")

        ans = solve_captcha()
        if ans['success']:
            break
        i +=1
        time.sleep(4)
except Exception as e:
    print(e)

time.sleep(20)
btn_close = driver.find_element_by_xpath("//*[@id='login-pannel']/div[2]")
if btn_close:
    btn_close.click()

time.sleep(5)
driver.quit()
