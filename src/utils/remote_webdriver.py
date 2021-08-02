from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()

driver = webdriver.Remote(
    command_executor='http://10.32.1.21:4444/wd/hub',
    options=firefox_options
)
