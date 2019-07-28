def print_logo():
    with open('./Modules/logo.txt', 'r') as file:
        data = file.read()
        print(data)