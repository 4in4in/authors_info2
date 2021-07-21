
from selenium import webdriver

profile = webdriver.FirefoxProfile()
profile.set_preference("dom.disable_beforeunload", True)
profile.set_preference("browser.tabs.warnOnClose", False)

gecko_path = './src/utils/webdriver/geckodriver'
log_path = './src/utils/webdriver/geckodriver.log'

driver = webdriver.Firefox(
    executable_path=gecko_path,
    firefox_profile=profile,
    log_path=log_path
    )