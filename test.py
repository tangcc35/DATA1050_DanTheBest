import selenium
print(selenium.__version__)
from selenium import webdriver
from lxml import etree
import time

url_main = "http://cab.inta-csic.es/rems/wp-content/plugins/marsweather-widget/widget.php?lang=en#next-sol"
driver = webdriver.Chrome(executable_path=r"Driver/chromedriver")
driver.maximize_window()
driver.get(url_main)
time.sleep(10)
html_main = etree.HTML(driver.page_source)
result_main = etree.tostring(html_main, encoding = 'utf-8', pretty_print= True, method = 'html')
result_main = result_main.decode('utf-8')
print(result_main)