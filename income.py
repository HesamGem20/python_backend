import unicodedata
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from flask import Flask, send_file
#lib
app = Flask(__name__)

# Task 1: User Generation

def generate_users(names):
    users = []
    
    for name in names:
        surname = name[0]
        given_name = name[1]
        
        # Generate email address
        email = f"{remove_accents(surname)}.{remove_accents(given_name)}@company.hu"
        
        # Generate password
        password = f"{surname}123Start"
        
        # Create user dictionary
        user = {
            'name': name,
            'email': email,
            'password': password
        }
        
        users.append(user)
    
    # Sort users alphabetically by name
    sorted_users = sorted(users, key=lambda u: u['name'][0])
    
    # Write user details to names.txt file
    with open('names.txt', 'w') as file:
        for user in sorted_users:
            line = ' '.join(user['name']) + ' ' + user['email'] + ' ' + user['password'] + '\n'
            file.write(line)
    
    return sorted_users


def remove_accents(string):
    normalized = unicodedata.normalize('NFKD', string)
    return normalized.encode('ASCII', 'ignore').decode("utf-8")


# Example usage
names = [['Kovács', 'Béla'], ['Kiss', 'Gyula'], ['Szabó', 'Ervin']]
users = generate_users(names)
print(users)


# Task 2: Counter Class

class Counter:
    def __init__(self, value, step=1):
        self.value = value
        self.step = step
    
    def increment(self):
        self.value += self.step
    
    def decrement(self):
        self.value -= self.step
    
    def set_value(self, value):
        self.value = value
    
    def set_step(self, step):
        self.step = step
    
    def get_value(self):
        return self.value


class ScoreCounter(Counter):
    def __init__(self, value, player_name, age):
        super().__init__(value)
        self.player_name = player_name
        self.age = age
        self.winner = False
    
    def increment(self):
        super().increment()
        if self.value >= 12:
            self.winner = True


# Example usage
myCounter = Counter(10)
myCounter.increment()
myCounter.increment()
print(myCounter.get_value())
myCounter.set_step(5)
myCounter.decrement()
print(myCounter.get_value())
myCounter.set_value(100)
myCounter.increment()
print(myCounter.get_value())

myScoreCounter = ScoreCounter(10, 'Zsolt', 34)
myScoreCounter.increment()
print(myScoreCounter.get_value())
myScoreCounter.increment()
print(myScoreCounter.get_value())
print(myScoreCounter.winner)


# Task 3: Module Use

@app.route('/')
def hello_world():
    # Read data from income.txt file
    data_source = []
    with open('income.txt', 'r') as file:
        lines = file.readlines()[1:]  # Omitting the header line
        for line in lines:
            line = line.strip()
            elements = line.split(',')
            row = [int(element.replace(' ', '')) for element in elements]
            data_source.append(row)

    # Create DataFrame from data
    df = pd.DataFrame(data_source)
    df.columns = pd.read_csv('income.txt', nrows=0).columns

    # Generate bar plot using seaborn
    sns_plot = sns.barplot(palette="ch:.25", data=df, ci=None)
    sns_plot.figure.savefig("output.png")
    plt.close()

    return send_file('output.png', mimetype='image/png')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


#Make sure to create an `income.txt` file in the same directory as the Python file and populate it with your income data.

