import json
from selenium import webdriver

class Browser():
    def __init__(self):
        self.browser = None
        self.params = None
        self.webpage = None
        self.root = None
        self.column_indices = None
        self.data_rows = {}
        with open("./input/params.json") as params:
            self.params = json.load(params)

    def run(self):
        if self.browser:
            self.set_page()
            if self.set_root():
                self.find_columns()
                self.prepare_rows()
                self.calculate()
                self.prepare_report()
            self.quit()

    def set_browser(self, browser_, name):
        self.browser = browser_
        self.params["browser"] = name

    def quit(self):
        self.browser.quit()
    
    def set_page(self):
        self.browser.get(self.params["webpage"])

    def set_root(self):
        try:
            self.root = self.browser.find_element_by_class_name(self.params["element-class"])
        except:
            print("not found")
            #return False
        return True

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
            #element.get_attribute("textContent") works better than element.text.
            self.data_rows[cells[0].get_attribute("textContent").strip()] = \
                                    [(cells[index].get_attribute("textContent").strip(),
                                     cells[index].get_attribute(self.params["cell_attribute"]).lower())
                                     for index in self.column_indices[1:]]
##        print(self.data_rows)

    def calculate(self):
        for currency in self.data_rows.keys():
            #MAKE THIS ACTUALLY LOGICAL. THIS IS HARD-CODED!!!
            for name in self.params["column_names"].keys():
                if self.params["column_names"][name] is None:
                    continue
                elif not self.params["column_names"][name]:
                    self.data_rows[currency].insert(1, "better" if float(self.data_rows[currency][0][0]) >= 0 else "worse")
                    self.data_rows[currency].insert(2, "pass" if self.data_rows[currency][0][1] == self.data_rows[currency][1] else "fail")
                else:
                    self.data_rows[currency].append("better" if float(self.data_rows[currency][-1][0][:-1]) >= 0 else "worse")
                    self.data_rows[currency].append("pass" if self.data_rows[currency][-2][1] == self.data_rows[currency][1] else "fail")
##        for entry in self.data_rows.items():
##            print(entry)

    def prepare_report(self):
        from datetime import datetime
        with open("./output/"+str(datetime.now()).replace(":","")+"_"+self.params["browser"]+".log", "w") as report:
            title = list(self.params["column_names"].keys())
            header = ""
            for item in title:
                header+=item+"\t"
                if title.index(item)>0:
                    header+="format\texpect\tstatus\t"
            report.write(header+"\n")
            flag_fail = False
            for item in self.data_rows.keys():
                row = ""
                row += item+"\t"
                for data in self.data_rows[item]:
                    if isinstance(data,tuple):
                        row+="\t"
                        for d in data:
                            row += d+"\t"
                    else:
                        if data.lower() == "fail":
                            flag_fail = True
                        row += data+"\t"
                report.write(row+"\n")
            report.write("Test "+("fail" if flag_fail else "pass"))
