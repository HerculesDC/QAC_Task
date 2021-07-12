from configparser import ConfigParser
from selenium.webdriver import Chrome, Firefox
from msedge.selenium_tools import EdgeOptions, Edge
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
        elif browser.title() == "Chrome":
            app.set_browser(Chrome())
        elif browser.title == "Edge":
            op = EdgeOptions()
            op.use_chromium = True
            app.set_browser(Edge(options = op))
        return app
