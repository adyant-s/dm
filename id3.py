

import pandas as pd

import math

df = pd.read_csv('play_tennis.csv')

def recursion(df):
  no_of_records,no_of_attr = df.shape
  total_lst = df.groupby(['play']).count()['day']
  if 'Yes' not in total_lst or 'No' not in total_lst:
    if 'Yes' in total_lst:
      print("YES you can play")
    else:
      print("NO you can't play")
    print("STOP")
    return
  fn,fy = total_lst
  ft = fn+fy
  IE = -1 * ( (fy/ft)*math.log(fy/ft,2) + (fn/ft)*math.log(fn/ft,2) )
  attributes = df.columns.tolist()[1: len(df.columns)-1]
  IG_attr = []
  for attribute in attributes:
    values = df[attribute].unique()
    entr_attr = 0
    for value in values:
      lst = df[df[attribute] == value].groupby(['play']).count()['day']
      y = 0
      if 'Yes' in lst:
        y = lst['Yes']
      n = 0
      if 'No' in lst:
        n = lst['No'] 
      total = y + n
      ent = 0 
      if y == 0 or n == 0:
        ent = 0
      else:
        ent = -1 * ( (y/total) * math.log(y/total,2) + (n/total)*math.log(n/total,2) )
      entr_attr = entr_attr + (total/ft) * ent
    IG_attr.append(IE - entr_attr)
  root_attr = attributes[IG_attr.index(max(IG_attr))]
  print("root_attr : ",root_attr)
  for value in df[root_attr].unique():
    print("attr : ",value)
    new_df = df[df[root_attr] == value].drop(root_attr,inplace = False,axis = 1)
    recursion(new_df)
  return

recursion(df)

def hunts_recursion(df):
  no_of_records,no_of_attr = df.shape
  total_lst = df.groupby(['play']).count()['day']
  if 'Yes' not in total_lst or 'No' not in total_lst:
    if 'Yes' in total_lst:
      print("YES you can play")
    else:
      print("NO you can't play")
    print("STOP")
    return
  attributes = df.columns.tolist()[1: len(df.columns)-1]
  root_attr = attributes[0]
  for value in df[root_attr].unique():
    print("attr : ",value)
    new_df = df[df[root_attr] == value].drop(root_attr,inplace = False,axis = 1)
    hunts_recursion(new_df)
  return

hunts_recursion(df)

fn,fy = df.groupby(['play']).count()['day']

ft = fn+fy

IE = -1 * ( (fy/ft)*math.log(fy/ft,2) + (fn/ft)*math.log(fn/ft,2) )

print("Entropy of entire dataset is ",IE)

attributes = df.columns.tolist()[1: len(df.columns)-1]
attributes

IG_attr = []
for attribute in attributes:
  values = df[attribute].unique()
  entr_attr = 0
  for value in values:
    lst = df[df[attribute] == value].groupby(['play']).count()['day']
    y = 0
    if 'Yes' in lst:
      y = lst['Yes']
    n = 0
    if 'No' in lst:
      n = lst['No'] 
    total = y + n
    ent = 0 
    if y == 0 or n == 0:
      ent = 0
    else:
      ent = -1 * ( (y/total) * math.log(y/total,2) + (n/total)*math.log(n/total,2) )
    entr_attr = entr_attr + (total/ft) * ent
  IG_attr.append(IE - entr_attr)
root_attr = attributes[IG_attr.index(max(IG_attr))]
for value in df[root_attr].unique():
  new_df = df[df[root_attr] == value].drop(root_attr,inplace = False,axis = 1)

y = df[df['outlook'] == 'Overcast'].groupby(['play']).count()['day']



new_df = df[df['outlook'] == 'Sunny'].drop('outlook',inplace = False,axis = 1)

new_df