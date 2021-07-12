import json
from selenium import webdriver


class Browser():
    def __init__(self):
        self.browser = None
        self.params = None
        self.webpage = None
        self.root = None
        self.column_indices = None
        self.data_rows = []
        with open("./input/params.json") as params:
            self.params = json.load(params)

    def run(self):
        if self.browser:
            self.set_page()
            self.set_root()
            self.find_columns()
            self.prepare_rows()
            self.quit()

    def set_browser(self, browser_):
        self.browser = browser_

    def quit(self):
        self.browser.quit()
    
    def set_page(self):
        self.browser.get(self.params["webpage"])

    def set_root(self):
        self.root = self.browser.find_element_by_class_name(self.params["element-class"])

    def find_columns(self):
        column_holder = self.root.find_elements_by_class_name(self.params["column-class"])
        keys = list(self.params["column_names"].keys())
        self.column_indices = [-1 for name in keys]
        for n_index in range(len(self.column_indices)):
            for col in column_holder:
                if keys[n_index] == col.text.title():
                    self.column_indices[n_index] = column_holder.index(col)
                    break
##        #Check: Returns the result of the indices of the columns that were
##        #       found, as per the "column_names" property keys in the
##        #       params.json file
##        key_list = list(self.params["column_names"].keys())
##        for key in range(len(key_list)):
##            print(key_list[key], end = " ")
##            if self.column_indices[key] == -1:
##                print(" not")
##            print("found at index",self.column_indices[key], end="\n")
                
    def prepare_rows(self):
        rows = self.root.find_elements_by_class_name(self.params["row-class"])
        for row in rows:
            cells = row.find_elements_by_class_name(self.params["cell-class"])
            self.data_rows.append([cells[0].text,
                                   cells[2].text,
                                   #float(cells[2].text),
                                   cells[2].get_attribute(self.params["cell_attribute"]).lower(),
                                   cells[2].text,
                                   #float(cells[3].text[:-1]),
                                   cells[3].get_attribute(self.params["cell_attribute"]).lower()])
        print(self.data_rows)
                                                          
