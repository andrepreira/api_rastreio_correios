from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverChromeFactory:
    def __init__(self, proxy: Optional[str] = None) -> None:
        self._proxy = proxy

    def get_driver(self) -> WebDriver:
        self.__construct()
        return self._driver
    
    def __construct(self) -> None:

        chrome_options = Options()
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            + "AppleWebKit/537.36 (KHTML, like Gecko)"
            + "Chrome/89.0.4389.114 Safari/537.36"
        )
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        if self._proxy:
            chrome_options.add_argument(f"--proxy-server={self._proxy}")

        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )