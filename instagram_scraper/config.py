import json

class Config:
    def __init__(self):
        with open('/config/config.json') as fp:
            self.config = json.load(fp)
    
    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
        with open('/config/config.json') as fp:
            json.dump(self.config, fp)

    def get_all():
        return self.config

    def set_all(data):
        self.config = data
        with open('/config/config.json') as fp:
            json.dump(self.config, fp)
