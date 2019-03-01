# _*_ coding: utf-8 _*_

"""
模拟登陆淘宝，并抓取商品
"""

import time
from urllib.parse import quote
from pyquery import PyQuery
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains


# webdriver
option = webdriver.ChromeOptions()
# option.add_argument("--proxy-server=127.0.0.1:9000")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
# option.add_argument("--headless")
browser = webdriver.Chrome("./chromedriver72", options=option)


def login(name, password):
	"""
	登陆
	"""
	url = "https://login.taobao.com/member/login.jhtml"
	browser.get(url)
	try:
		browser.find_element_by_css_selector("div.login-switch #J_Quick2Static").click()
	except Exception as excep:
		print(excep)

	# 输入用户名密码
	browser.find_element_by_id("TPL_username_1").send_keys(name)
	browser.find_element_by_id("TPL_password_1").send_keys(password)
	time.sleep(1)

	try:
		# 拖动滑块
		slider = browser.find_element_by_css_selector("#nc_1_n1z")
		action = ActionChains(browser)
		action.drag_and_drop_by_offset(slider, 500, 0).perform()
		time.sleep(3)
	except Exception as excep:
		print(excep)

	time.sleep(2)
	browser.find_element_by_id("J_SubmitStatic").click()
	return


def index_page(page, key):
	print("正在爬去第", page, "页")
	try:
		browser.get("https://s.taobao.com/search?q="+quote(key))
		try:
			slider2 = browser.find_element_by_css_selector("#nc_1__scale_text span.nc-lang-cnt")
			action2 = ActionChains(browser)
			action2.drag_and_drop_by_offset(slider2, 500, 0).perform()
			time.sleep(5)
		except Exception as excep:
			print(excep)

		input1 = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager div.form > input")))
		submit = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager div.form > span.btn.J_Submit")))
		input1.clear()
		input1.send_keys(page)
		submit.click()

		wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager li.item.active > span"), str(page)))
		wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".m-itemlist .items .item")))

		# 获取商品
		doc = PyQuery(browser.page_source)
		items = doc("#mainsrp-itemlist .items .item").items()
		for item in items:
			product = {
				"image": item.find(".pic .img").attr("data-src"),
				"price": item.find(".price").text(),
				"deal": item.find(".deal-cnt").text(),
				"title": item.find(".title").text(),
				"shop": item.find(".shop").text(),
				"location": item.find(".location").text(),
			}
			print(product)
	except TimeoutException:
		index_page(page, key)
	except Exception as excep:
		print(excep)
	return


if __name__ == "__main__":
	wait = WebDriverWait(browser, 10)
	login("username", "password")
	# 抓取商品
	for x in range(2, 10):
		time.sleep(5)
		index_page(x, "python")
	browser.close()
