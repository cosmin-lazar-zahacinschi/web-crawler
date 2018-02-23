import json  

def get_prop(key):
    return property_dict[key]

class PropertyDict:
    
    def __init__(self):
        with open("conf.json", 'r') as f:
            self.conf_ = json.load(f)

    def __getitem__(self, key):
        return self.conf_[key]
    
property_dict = PropertyDict()