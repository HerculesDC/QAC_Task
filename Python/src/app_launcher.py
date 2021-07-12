from configparser import ConfigParser
from selenium.webdriver import Chrome, Edge, Firefox
from src.browser import Browser

class AppLauncher():
    @staticmethod
    def launch_app():
        config = ConfigParser()
        config.read("./input/options.ini")
        info = config["DEFAULT"]
        browser = info.get("BROWSER")
        app = Browser()
        if browser.title() == "Firefox":
            app.set_browser(Firefox())
        if browser.title() == "Chrome":
            app.set_browser(Chrome())
        return app
