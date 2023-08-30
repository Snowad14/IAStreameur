import yaml, json

class Config:
    config_path = "config.yaml"

    def __load_config(file_path):
        with open(file_path, 'r') as file:
            if file_path.endswith('.json'):
                return json.load(file)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(file)
            else:
                raise ValueError("Le fichier de configuration doit être au format JSON ou YAML.")
    
    @staticmethod
    def get_value(key):
        config = Config.__load_config(Config.config_path)
        return config.get(key)

class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.messages = []

    def enqueue(self, message):
        if len(self.messages) < self.capacity:
            self.messages.append(message)
    
    def dequeue(self):
        if len(self.messages) > 0:
            return self.messages.pop(0)

if __name__ == "__main__":
    print(Config.get_value("edgetts_voice"))