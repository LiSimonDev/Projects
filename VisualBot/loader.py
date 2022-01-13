from configparser import ConfigParser

def save_config(data, num): #data must be a dictionary
    config_object = ConfigParser()
    for slot in data:
        config_object[slot] = data[slot]
    with open('config\config'+str(num)+'.ini', 'w') as conf:
        config_object.write(conf)

def load_config():
    configs = {}
    for i in range(9):
        config_object = ConfigParser()
        config_object.read("config\config"+str(i+1)+".ini")
        configs[str(i+1)] = config_object._sections
    return configs

if __name__ == "__main__":
    print(load_config()['1'])
