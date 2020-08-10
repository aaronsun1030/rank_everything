import csv
import json
import os
from json import JSONDecodeError
from time import time
from random import choice


class Item:
    def __init__(self, line, thought, comparator=None):
        self.item_id, self.name, self.description = line[:3]
        self.thoughts = thought
        self.tags = line[4:]
        self.comparator = comparator

    """
    GET FIELDS
    """
    def get_item_id(self):
        """ get unique 5 digit hex ID for this item """
        return self.item_id

    def get_name(self):
        """ get this item's name """
        return self.name

    def get_description(self):
        """ get this item's description """
        return self.description

    def get_tags(self):
        """ get this item's tags as an array """
        return self.tags

    def get_thoughts(self):
        """ get the user's thoughts about this item """
        return self.thoughts
        
    """
    UPDATE ITEM
    """
    
    def update_thoughts(self, thought):
        self.thoughts = thought
        self.comparator.update_item_thoughts(self.item_id, self.thoughts)
    

        
        
class Comparison:
    def __init__(self, line):
        self.better, self.worse, self.date = line
        
    def __contains__(self, item):
        return item.item_id == self.better or item.item_id == self.worse


class Comparator:
    """ Object which picks items to compare from selected lists and can write comparisons """
    
    def __init__(self):
        self.comp_file = os.getcwd() + '/comparisons/aaron_comparisons.csv'
        self.thoughts_file = os.getcwd() + '/comparisons/aaron_thoughts.json'
        self.thoughts, self.comp_list = {}, []
        self.load_comps(self.comp_file)
        self.load_thoughts(self.thoughts_file)

        self.items, self.list_names = [], []
        self.list_ids = {}

        self.item1, self.item2 = None, None
        
    """
    COMPARISON FUNCTIONS
    """

    def shuffle_pair(self):
        """ changes the pair of item objects associated with this object
            such that they are from selected lists and have never been compared """
        self.item1, self.item2 = choice(self.items), choice(self.items)
        if self.item2 == self.item1:
            self.shuffle_pair()
        done = False
        for comp in self.comp_list:
            if self.item1 in comp and self.item2 in comp:
                done = True
        if done:
            self.shuffle_pair()

    def get_pair(self):
        """ returns the pair of items associated with this object """
        return self.item1, self.item2

    def select_preferred(self, item_num):
        """ selects the preferred item_num (1 or 2) and adds the comparison to the list """
        if item_num == 1:
            self.add_comparison(self.item1, self.item2)
        else:
            self.add_comparison(self.item2, self.item1)

    """
    LIST MANAGEMENT
    """
        
    def get_lists(self):
        """ returns a list of the names of all categories """
        l = []
        for subdir, dirs, files in os.walk(os.getcwd() + "/lists/"):
            for file in files:
                filepath = subdir + os.sep + file
                if file.endswith('.csv') and file != "list_ids.csv":
                    l.append(file[:-4])
        return l

    def add_list(self, list_name):
        """ adds lists to potential choices """
        if list_name not in self.list_names:
            self.list_names.append(list_name)
            path = self.get_path(list_name)
            with open(path, mode='r') as file:
                # reading the CSV file 
                csvFile = csv.reader(file)
                for line in list(csvFile)[1:]:
                    if line and line[0]:
                        thought = self.thoughts.get(line[0])
                        if not thought:
                            thought = ""
                        else:
                            thought = thought["thoughts"]
                        self.items.append(Item(line, thought, comparator=self))
    
    def remove_list(self, list_name):
        """ removes the list from being selected """
        if list_name in self.list_names:
            list_id = self.get_list_id(list_name)
            self.list_names.remove(list_name)
            for i in range(len(self.items)-1, -1, -1):
                item = self.items[i]
                if item.item_id[:4] == list_id:
                    self.items.remove(item)
                    
    """
    INTERNAL FUNCTIONS
    """
    def add_comparison(self, better, worse):
        """ adds a new comparison """
        l = [better.item_id, worse.item_id, time()]
        with open(self.comp_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(l)
        self.comp_list.append(Comparison(l))

    def load_comps(self, filename):
        with open(filename, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            for line in list(csvFile)[1:]:
                if line:
                    self.comp_list.append(Comparison(line))

    def load_thoughts(self, filename):
        with open(filename, mode='r') as f:
            try:
                self.thoughts = json.load(f)
            except JSONDecodeError:
                pass

    def update_item_thoughts(self, item_id, thought):
        self.thoughts[item_id] = thought
        a_dict = {item_id: {"thoughts": thought,
                            "time": time()}}

        with open(self.thoughts_file) as f:
            data = json.load(f)

        data.update(a_dict)

        with open(self.thoughts_file, 'w') as f:
            json.dump(data, f)
                    
    def get_path(self, list_name):
        for subdir, dirs, files in os.walk(os.getcwd() + "/lists/"):
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
                for line in list(csvFile)[1:]:
                    if line:
                        self.list_ids[line[0]] = line[1]
        return self.list_ids[list_name]

