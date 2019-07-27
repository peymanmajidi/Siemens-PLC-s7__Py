def print_logo():
    with open('logo.txt', 'r') as file:
        data = file.read()
        print(data)