import os
from time import time
from random import choice

class item:
    def __init__(self, line):
        self.item_id, self.name, self.description, self.thoughts = *(line[:4])
        self.tags = line[4:]
        self.list_names = {}
        
    """
    UPDATE ITEM
    """
    
    def update_thoughts(self, thought):
        this.overwrite_csv(3, thought)
        
    def update_description(self, description):
        this.overwrite_csv(2, description)
    
    """
    INTERNAL FUNCTIONS
    """
    
    def overwrite_csv(self, index, update):
        filepath = get_path(self.get_list_name(self.item_id[:2]))
        old = []
        
        line = 0
        item_line = 0
        # Read all data from the csv file.
        with open(filepath, 'rb') as b:
            line += 1
            item = csv.reader(b)
            old.extend(item)
            if old[-1][0] == self.item_id:
                item_line = line

        # data to override in the format {line_num_to_override:data_to_write}. 
        line_to_override = {line: old[item_line][0:index] + [update] + old[item_line][index+1:]}

        # Write data to the csv file and replace the lines in the line_to_override dict.
        with open(filepath, 'wb') as b:
            writer = csv.writer(b)
            for line, row in enumerate(old):
                 data = line_to_override.get(line, row)
                 writer.writerow(data)
    
    def get_path(list_name):
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                if file == list_name + '.csv':
                    return filepath
    
    def get_list_name(self):
        if not self.list_names:
            with open('lists/list_ids.csv', mode='r') as file:
                # reading the CSV file 
                csvFile = csv.reader(file)
              
                # displaying the contents of the CSV file 
                for line in csvFile[1:]: 
                    self.list_names[line[1]] = line[0]
        return self.list_names[list_name]
        
        
class comparison:
    def __init__(self, line):
        self.better, self.worse, self.date = *(line)
        
    def __contains__(self, item):
        return item.item_id == self.better or item.item_id == self.worse

class comparator:
    
    def __init__(self):
        self.comp_file = '/comparisons/aaron_comparisons.csv'
        self.list_names, self.items = [], []
        self.comp_list = self.read_comps()
        self.list_ids = {}
        
    """
    COMPARISON FUNCTIONS
    """
    
    def get_pair(self):
        """ returns a pair of item objects from selected lists which have never been compared """
        item1, item2 = choice(self.items), choice(self.items)
        if item2 == item1:
            return self.get_pair()
        done = False
        for comp in comp_list:
            if item1 in comp and item2 in comp:
                done = True
        if done:
            return self.get_pair()
        else:
            return item1, item2
            
    def add_comparison(self, better, worse):
        """ adds a new comparison """
        l = [better.item_id, worse.item_id, time()]
        with open(self.comp_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(l)
        self.comp_list.append(l)
        
    """
    LIST MANAGEMENT
    """
        
    def get_lists(self):
        """ returns a list of the names of all cateories """
        l = []
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                if file.endswith('.csv'):
                    l.append(file[:-4]))
        return l
        
    def add_list(self, list_name):
        """ adds lists to potential choices """
        if list_name not in self.list_names:
            self.list_names.append(list_name)
            path = get_path(list_name)
            with open(path, mode='r') as file:
                # reading the CSV file 
                csvFile = csv.reader(file)
                for line in csvFile[1:]:
                    self.items.append(item(line))
    
    def remove_list(self, list_name):
        """ removes the list from being selected """
        if list_name in self.list_names:
            list_id = self.get_list_id(list_name)
            self.list_names.remove(list_name)
            for item in self.items:
                if item.item_id[:2] == list_id:
                    self.items.remove(item)
                    
    """
    INTERNAL FUNCTIONS
    """
    
    def load_comps(self):
        with open(comp_file, mode='r') as file:
            # reading the CSV file 
            csvFile = csv.reader(file)
            for line in csvFile[1:]:
                self.comp_list.append(comparison(line))
                    
    def get_path(list_name):
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filepath = subdir + os.sep + file
                if file == list_name + '.csv':
                    return filepath
                    
    def get_list_id(self, list_name):
        if not self.list_ids:
            with open('lists/list_ids.csv', mode='r') as file:
                # reading the CSV file 
                csvFile = csv.reader(file)
              
                # displaying the contents of the CSV file 
                for line in csvFile[1:]: 
                    self.list_ids[line[0]] = line[1]
        return self.list_ids[list_name]
            
            
            
        
        
        