#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random


# In[2]:


df_monday = pd.read_csv('data/monday.csv', sep=';', index_col=0)

df_tuesday = pd.read_csv('data/tuesday.csv', sep=';', index_col=0)

df_wednesday = pd.read_csv('data/wednesday.csv', sep=';', index_col=0)

df_thursday = pd.read_csv('data/thursday.csv', sep=';', index_col=0)

df_friday = pd.read_csv('data/friday.csv', sep=';', index_col=0)


# In[3]:


# put together every dataframe for each day into one df
frames = [df_monday, df_tuesday, df_wednesday, df_thursday, df_friday]
df = pd.concat(frames)
df.head()


# In[4]:


df.index = pd.to_datetime(df.index)


# In[5]:


# Calculate the total number of customers in each section
df.groupby('location').count()


# In[6]:


df.groupby('location').count().plot(kind='bar')


# In[7]:


df['day'] = df.index.day
df.head()


# In[8]:


df.index


# In[9]:


# Calculate the total number of customers in each section over time (here complete time)
df.groupby(['location', 'day']).count()
df.head(6)


# In[10]:


# Calculate the total number of customers in each section over time (here hourly)
df.groupby('location').resample('h').count()


# In[11]:


# Display the number of customers at checkout over time (here one day)
df[(df.location == 'checkout') & (df.day==2)].count()


# In[12]:


# Calculate the total number of customers in each section over time (here day)
df.groupby(['location', 'day']).count()
df.head(7)


# In[13]:


df.groupby(['location', 'day']).count().plot(kind='bar')


# In[14]:


df.reset_index(inplace=True)
df


# In[15]:


df[df.location == 'checkout'].groupby(['day', 'timestamp'])[['customer_no']].count()


# In[16]:


# create new column 'time_spend'
df['time_spend'] = df.groupby(['day', 'customer_no'])['timestamp'].transform(lambda x : x.max()-x.min())


# In[17]:


# find customers who were not checked-out
df[df['time_spend'] == 0]


# In[18]:


# Calculate the time each customer spent in the market
df['time_spend']


# In[20]:


df = df.set_index(['timestamp'])
df = df.groupby('customer_no').resample('T').ffill()


# In[21]:


df


# In[23]:


# create a new column 'next location'
df.drop(columns='customer_no', inplace=True)

df['next_location'] = df.groupby(['day', 'customer_no'])['location'].shift(-1)


# In[24]:


df.head(10)


# In[25]:


df.next_location.fillna('checkout', inplace=True)


# In[26]:


df.head(10)


# In[27]:


transition_probes = pd.crosstab(df['location'], df['next_location'], normalize=0)


# In[28]:


transition_probes


# In[29]:


# all rows have to sum up to one
assert all(transition_probes.sum(axis=1) > 0.999)


# In[33]:


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


# In[60]:


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
                


# In[63]:


lidl = Supermarket(name='LIDL')

while lidl.is_open():
    
    lidl.get_time()

    # increase the time of the supermarket by one minute
    lidl.add_new_customers()
    

    lidl.next_minute()
    

    # remove churned customers from the supermarket
    lidl.print_customers()
    
    lidl.remove_exitsting_customers()

    # generate new customers at their initial location
    #lidl.add_new_customers()
    

    # repeat from step 1
    #lidl.print_customers()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[53]:


cust1 = Customer("Jake", "spices", transition_probes, 50)
cust1.next_state()


# In[ ]:




