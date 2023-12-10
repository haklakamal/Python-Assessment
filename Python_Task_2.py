#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
from itertools import combinations
from datetime import time


# In[22]:


# Read dataset-3.csv
df3 = pd.read_csv('C:/Users/h/Downloads/dataset-3.csv')


# In[23]:


# Question 1: Distance Matrix Calculation
def calculate_distance_matrix(df):
    routes = df.groupby(['id_start', 'id_end']).agg({'distance': 'sum'}).reset_index()
    distance_matrix = routes.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)
    np.fill_diagonal(distance_matrix.values, 0)
    return distance_matrix


# In[24]:


# Question 2: Unroll Distance Matrix
def unroll_distance_matrix(distance_matrix):
    unrolled_distances = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for pair in combinations(distance_matrix.index, 2):
        id_start, id_end = pair
        distance = distance_matrix.loc[id_start, id_end]
        unrolled_distances = unrolled_distances.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                                       ignore_index=True)
    return unrolled_distances


# In[25]:


# Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(unrolled_distances, reference_value):
    avg_distance = unrolled_distances[unrolled_distances['id_start'] == reference_value]['distance'].mean()
    threshold = 0.1 * avg_distance
    ids_within_threshold = unrolled_distances[(unrolled_distances['distance'] >= avg_distance - threshold) &
                                              (unrolled_distances['distance'] <= avg_distance + threshold)]['id_start'].unique()
    return sorted(ids_within_threshold)


# In[26]:


# Question 4: Calculate Toll Rate
def calculate_toll_rate(unrolled_distances):
    toll_rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle in toll_rates:
        unrolled_distances[vehicle] = unrolled_distances['distance'] * toll_rates[vehicle]
    return unrolled_distances


# In[27]:


# Question 5: Calculate Time-Based Toll Rates
def calculate_time_based_toll_rates(unrolled_distances):
    discount_factors = {
        'weekday_morning': 0.8,
        'weekday_daytime': 1.2,
        'weekday_evening': 0.8,
        'weekend': 0.7
    }
    
    unrolled_distances['start_day'] = unrolled_distances['start_time'] = unrolled_distances['end_day'] = unrolled_distances['end_time'] = None
    
    for pair in unrolled_distances.itertuples(index=False):
        unrolled_distances.at[pair.Index, 'start_day'] = 'Monday'
        unrolled_distances.at[pair.Index, 'end_day'] = 'Sunday'
        unrolled_distances.at[pair.Index, 'start_time'] = time(0, 0, 0)
        unrolled_distances.at[pair.Index, 'end_time'] = time(23, 59, 59)

    unrolled_distances['start_time'] = pd.to_datetime(unrolled_distances['start_time'])
    unrolled_distances['end_time'] = pd.to_datetime(unrolled_distances['end_time'])
    
    weekday_morning_mask = (unrolled_distances['start_time'].dt.weekday < 5) & (unrolled_distances['start_time'].dt.hour < 10)
    weekday_daytime_mask = (unrolled_distances['start_time'].dt.weekday < 5) & (unrolled_distances['start_time'].dt.hour < 18)
    weekday_evening_mask = (unrolled_distances['start_time'].dt.weekday < 5) & (unrolled_distances['start_time'].dt.hour >= 18)
    weekend_mask = (unrolled_distances['start_time'].dt.weekday >= 5)
    
    unrolled_distances.loc[weekday_morning_mask, 'distance'] *= discount_factors['weekday_morning']
    unrolled_distances.loc[weekday_daytime_mask, 'distance'] *= discount_factors['weekday_daytime']
    unrolled_distances.loc[weekday_evening_mask, 'distance'] *= discount_factors['weekday_evening']
    unrolled_distances.loc[weekend_mask, 'distance'] *= discount_factors['weekend']
    
    return unrolled_distances


# In[28]:


# Test the functions
distance_matrix = calculate_distance_matrix(df3)
unrolled_distances = unroll_distance_matrix(distance_matrix)
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_distances, reference_value=1)
toll_rate_result = calculate_toll_rate(unrolled_distances)
time_based_toll_rates_result = calculate_time_based_toll_rates(unrolled_distances)


# In[ ]:


# Display the results
print("Question 1 - Distance Matrix:")
print(distance_matrix)

print("\nQuestion 2 - Unrolled Distance Matrix:")
print(unrolled_distances)

print("\nQuestion 3 - IDs within Percentage Threshold:")
print(ids_within_threshold)

print("\nQuestion 4 - Toll Rate Calculation:")
print(toll_rate_result)

print("\nQuestion 5 - Time-Based Toll Rates:")
print(time_based_toll_rates_result)


# In[ ]:




