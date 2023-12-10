#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd

# Read dataset-1.csv
df1 = pd.read_csv('C:/Users/h/Downloads/dataset-1.csv')


# In[22]:


# Question 1: Car Matrix Generation
def generate_car_matrix(df):
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(len(car_matrix))]*2] = 0  # Set diagonal values to 0
    return car_matrix


# In[23]:


# Question 2: Car Type Count Calculation
def get_type_count(df):
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_count.items()))


# In[24]:


# Question 3: Bus Count Index Retrieval
def get_bus_indexes(df):
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(bus_indexes)


# In[25]:


# Question 4: Route Filtering
def filter_routes(df):
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()
    return sorted(filtered_routes)


# In[26]:


# Question 5: Matrix Value Modification
def multiply_matrix(car_matrix):
    modified_matrix = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)
    return modified_matrix


# In[27]:



# Question 6: Time Check
df2 = pd.read_csv('C:/Users/h/Downloads/dataset-2.csv')

def check_time_completeness(df):
    df['start_time'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_time'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['day_of_week'] = df['start_time'].dt.day_name()

    completeness_check = df.groupby(['id', 'id_2']).apply(lambda group: group['day_of_week'].nunique() == 7 and
                                                            group['start_time'].min().hour == 0 and
                                                            group['end_time'].max().hour == 23)

    return completeness_check


# In[32]:


# Display the results
print("Question 1 - Car Matrix:")
print(car_matrix)

print("\nQuestion 2 - Car Type Count:")
print(type_count)

print("\nQuestion 3 - Bus Count Index Retrieval:")
print(bus_indexes)

print("\nQuestion 4 - Filtered Routes:")
print(filtered_routes)

print("\nQuestion 5 - Modified Car Matrix:")
print(modified_matrix)

print("\nQuestion 6 - Time Completeness Check:")
print(time_completeness_check)


# In[ ]:




