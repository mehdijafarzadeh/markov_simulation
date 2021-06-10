import pandas as pd
import numpy as np
import random
import os
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import glob

df = pd.DataFrame()

for file in glob.glob('./data/'+'*.csv'):
    data = pd.read_csv(file, sep=';', parse_dates=['timestamp'], index_col=['timestamp'])
    df = df.append(data)


# Calculate the total number of customers in each section
df.groupby('location').count()


df.groupby('location').count().plot(kind='bar')

df['day'] = df.index.day
df.head()

# Calculate the total number of customers in each section over time (here complete time)
df.groupby(['location', 'day']).count()
df.head(6)

# Calculate the total number of customers in each section over time (here hourly)
df.groupby('location').resample('h').count()


# Display the number of customers at checkout over time (here one day)
df[(df.location == 'checkout') & (df.day==2)].count()


# Calculate the total number of customers in each section over time (here day)
df.groupby(['location', 'day']).count()
df.head(7)




df.groupby(['location', 'day']).count().plot(kind='bar')



df.reset_index(inplace=True)
df

df[df.location == 'checkout'].groupby(['day', 'timestamp'])[['customer_no']].count()

# create new column 'time_spend'
df['time_spend'] = df.groupby(['day', 'customer_no'])['timestamp'].transform(lambda x : x.max()-x.min())

# find customers who were not checked-out
df[df['time_spend'] == 0]

# Calculate the time each customer spent in the market
df['time_spend']

df = df.set_index(['timestamp'])
df = df.groupby('customer_no').resample('T').ffill()

# create a new column 'next location'
df.drop(columns='customer_no', inplace=True)

df['next_location'] = df.groupby(['day', 'customer_no'])['location'].shift(-1)

df.next_location.fillna('checkout', inplace=True)

transition_probes = pd.crosstab(df['location'], df['next_location'], normalize=0)


# all rows have to sum up to one
assert all(transition_probes.sum(axis=1) > 0.999)

class Customer:
       
    def __init__(self, name, state, transition_probes, budget=100):
        
        self.name = name
        self.state = state
        self.transition_probes = transition_probes
        self.budget = budget
        
    def __repr__(self):
        
        return f'<Customer {self.name} in {self.state}>'
    
    def next_state(self):
        
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        self.state = random.choices(transition_probes.columns, transition_probes.loc[self.state])[0]
        return self.state
        
        
    def is_active(self):
        
        return self.state != 'checkout'
            #return True


class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self, name):        
        # a list of Customer objects                  
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.name = name
        # opens at 0
        # closes at 15


    def __repr__(self):
        return f'{self.name} supermarket at {self.get_time()} with {len(self.customers)} customers.'


    def get_time(self):
        """current time in HH:MM format,
        """
        hours = self.minutes // 60  # integer division
        minutes = self.minutes % 60 # remainder/ modulo
        return f'{hours:02d}:{minutes:02d}:00'


    def is_open(self):  
        # supermarket closes after 15hours    
        return self.minutes < 900


    def print_customers(self):
        """print all customers with the current time and id in CSV format.     
        """
        
        for customer in self.customers:
            
            print(f'{self.get_time()}, {customer.name}, {customer.state}')


    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.minutes += 1
        # for every customer determine their next state
        for customer in self.customers:
            customer.next_state()
   

    def add_new_customers(self):
        """randomly creates new customers.
        """
        self.last_id += 1
        new_customer = Customer(self.last_id, random.choices(['fruit', 'dairy', 'drinks', 'spices'])[0], transition_probes)
        self.customers.append(new_customer)
        


    def remove_exitsting_customers(self):
        """removes every customer that is not active any more.
        """
        self.customers = [customer for customer in self.customers if customer.is_active()]
        
        #for customer in self.customers if 
                


lidl = Supermarket(name='LIDL')

while lidl.is_open():
    
    lidl.get_time()

    # increase the time of the supermarket by one minute
    lidl.add_new_customers()

    lidl.next_minute()
    
    # remove churned customers from the supermarket
    lidl.print_customers()
    
    lidl.remove_exitsting_customers()





