import json
from selenium import webdriver


class Browser():
    def __init__(self):
        self.browser = None
        self.params = None
        self.webpage = None
        self.root = None
        self.column_indices = None
        with open("./input/params.json") as params:
            self.params = json.load(params)

    def run(self):
        if self.browser:
            self.set_page()
            self.set_root()
            #self.find_columns()
            self.quit()

    def set_browser(self, browser_):
        self.browser = browser_

    def quit(self):
        self.browser.quit()
    
    def set_page(self):
        self.browser.get(self.params["webpage"])

    def set_root(self):
        self.root = self.browser.find_element_by_class_name(self.params["element-class"])
        print(self.root)

    def find_columns(self):
        column_holder = self.root.find_element_by_class_name(self.params["column-class"])
        self.column_indices = [-1 for name in self.params["column_names"].keys()]
        for n_index in range(len(self.column_indices)):
            for col in column_holder:
                if self.params["column_names"][n_index] == col.text.title():
                    self.column_indices[n_index] = column_holder.index(col)
                    break
        if -1 in self.column_indices:
            index = self.column_indices.index(-1)
            print(f"Column {self.params['column_names'][index]} not found!")
