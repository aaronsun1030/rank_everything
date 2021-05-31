import csv
import json
import os
from json import JSONDecodeError
from time import time, ctime
from random import choice


class Item:
    def __init__(self, line, thought, comparator=None):
        self.item_id, self.name, self.description = line[:3]
        self.thoughts = thought
        self.tags = line[3:]
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
        formatted_thoughts = ""
        for key, value in self.thoughts.items():
            formatted_thoughts += ctime(float(key)) + ": " + value + 2 * os.linesep
        return formatted_thoughts
        
    """
    UPDATE ITEM
    """
    
    def add_thought(self, thought):
        self.thoughts[time()] = thought
        self.comparator.update_item_thoughts(self.item_id, self.thoughts)

    def update_item(self, field_name, new_field):
        """
        enter field name as string which can either be "name", "description", "tags".
        new_field is the updated field: strings for name/description, and array for tags.
        """
        l = []
        if field_name == "name":
            l = [self.item_id, new_field, self.description] + self.tags
            self.name = new_field
        elif field_name == "description":
            l = [self.item_id, self.name, new_field] + self.tags
            self.description = new_field
        else:
            while len(new_field) <= 3:
                new_field.append('')
            l = [self.item_id, self.name, self.description] + new_field
            self.tags = new_field
        if l:
            self.comparator.update_item(self, l)

    
        
class Comparison:
    def __init__(self, line):
        self.better, self.worse, self.date = line
        
    def __contains__(self, item):
        return item == self.better or item == self.worse


class ListManager:

    def __init__(self, comp_dir='/comparisons/aaron_comparisons.csv', thoughts_dir='/comparisons/aaron_thoughts.json'):
        self.list_ids = {}
        self.comp_file = os.getcwd() + comp_dir
        self.thoughts_file = os.getcwd() + thoughts_dir
        self.thoughts, self.comp_list = {}, []
        self.load_comps(self.comp_file)
        self.load_thoughts(self.thoughts_file)
        self.items = {}
        

    """
    Fetch list/item details
    """
    def get_path(self, list_name):
        ''' get directory for list from list name '''
        for subdir, _, files in os.walk(os.getcwd() + "/lists/"):
            for file in files:
                filepath = subdir + os.sep + file
                if file == list_name + '.csv':
                    return filepath
                    
    def get_list_id(self, list_name):
        ''' get list ID from list name '''
        if not self.list_ids:
            with open('lists/list_ids.csv', mode='r') as file:
                # reading the CSV file 
                csvFile = csv.reader(file)
              
                # displaying the contents of the CSV file 
                for line in list(csvFile)[1:]:
                    if line:
                        self.list_ids[line[0]] = line[1]
        return self.list_ids[list_name]

    def get_list_name(self, id):
        ''' get list name from list ID '''
        if not self.list_ids:
            with open('lists/list_ids.csv', mode='r') as file:
                # reading the CSV file
                csvFile = csv.reader(file)

                # displaying the contents of the CSV file
                for line in list(csvFile)[1:]:
                    if line:
                        self.list_ids[line[0]] = line[1]
        for key, value in self.list_ids.items():
            if id == value:
                return key

    def get_item(self, item_id):
        ''' get item from item ID '''
        if item_id in self.items:
            return self.items[item_id]
        list_name = self.get_list_name(item_id[:4])
        with open(self.get_path(list_name), mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            for line in list(csvFile)[1:]:
                if line and line[0]:
                    thought = self.thoughts.get(line[0])
                    if not thought:
                        thought = {}
                    temp = Item(line, thought, comparator=self)
                    self.items[temp.item_id] = temp
        return self.items[item_id]

    def get_all_lists(self):
        ''' returns a list of the names of all categories '''
        l = []
        for _, _, files in os.walk(os.getcwd() + "/lists/satisfactory/"):
            for file in files:
                if file.endswith('.csv') and file != "list_ids.csv":
                    l.append(file[:-4])
        return l

    """
    Update item
    """
    def update_item(self, item, new_line):
        """ updates the item in the CSV """
        new_rows = []
        list_dir = self.get_path(self.get_list_name(item.get_item_id()[:4]))
        with open(list_dir, 'r') as f:
            reader = csv.reader(f)  # pass the file to our csv reader
            for row in reader:  # iterate over the rows in the file
                if row and row[0] == item.get_item_id():
                    row = new_line
                new_rows.append(row)  # add the modified rows

        with open(list_dir, 'w', newline='') as f:
            # Overwrite the old file with the modified rows
            writer = csv.writer(f)
            writer.writerows(new_rows)

    def update_item_thoughts(self, item_id, thought):
        ''' changes the thought of item_id to thought '''
        if item_id in self.thoughts:
            previous_thoughts = {item_id: self.thoughts[item_id]}
        else:
            previous_thoughts = {item_id: {}}
        previous_thoughts.update({item_id: thought})
        a_dict = previous_thoughts
        self.thoughts.update(a_dict)

        with open(self.thoughts_file) as f:
            data = json.load(f)

        data.update(a_dict)

        with open(self.thoughts_file, 'w') as f:
            json.dump(data, f)


    """
    Load in files
    """
    def change_comp_file(self, comp_dir):
        self.comp_file = comp_dir
        self.comp_list = []
        self.load_comps(comp_dir)

    def change_thoughts_file(self, thoughts_dir):
        self.thoughts_file = thoughts_dir
        self.thoughts = {}
        self.load_thoughts(thoughts_dir)

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


class Comparator(ListManager):
    """ Object which picks items to compare from selected lists and can write comparisons """
    
    def __init__(self, comp_dir='/comparisons/aaron_comparisons.csv', thoughts_dir='/comparisons/aaron_thoughts.json'):
        super().__init__(comp_dir=comp_dir, thoughts_dir=thoughts_dir)
        self.active_lists, self.active_items = [], []
        self.item1, self.item2 = None, None
        
    """
    COMPARISON FUNCTIONS
    """

    def shuffle_pair(self):
        """ changes the pair of item objects associated with this object
            such that they are from selected lists and have never been compared """
        self.item1, self.item2 = self.get_item(choice(self.active_items)), self.get_item(choice(self.active_items))
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

    def get_active_lists(self):
        """ returns a list of active lists from which items can be selected """
        return self.active_lists

    def set_lists(self, names):
        """ sets active lists to the lists in names """
        removals = sum([1 for name in self.active_lists if name not in names])
        if removals >= len(self.active_lists) / 2:
            self.active_lists, self.active_items = [], []
            self.item1, self.item2 = None, None
            for name in names:
                self.add_list(name)
        else:
            for name in self.active_lists:
                if name not in names:
                    self.remove_list(name)
            for name in names:
                self.add_list(name)

    """
    INTERNAL FUNCTIONS
    Not for Josh to see/understand
    """

    def add_list(self, list_name):
        """ adds lists to potential choices """
        if list_name not in self.active_lists:
            self.active_lists.append(list_name)
            path = self.get_path(list_name)
            with open(path, mode='r') as file:
                # reading the CSV file
                csvFile = csv.reader(file)
                for line in list(csvFile)[1:]:
                    if line and line[0]:
                        self.active_items.append(line[0])

    def remove_list(self, list_name):
        """ removes the list from being selected """
        if list_name in self.active_lists:
            list_id = self.get_list_id(list_name)
            self.active_lists.remove(list_name)
            for i in range(len(self.active_items) - 1, -1, -1):
                item = self.active_items[i]
                if item[:4] == list_id:
                    self.active_items.remove(item)

    def add_comparison(self, better, worse):
        """ adds a new comparison """
        l = [better.item_id, worse.item_id, time()]
        with open(self.comp_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(l)
        self.comp_list.append(Comparison(l))

    
                    
