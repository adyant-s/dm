

import pandas as pd
import numpy as np
import itertools
df=pd.read_csv('/content/Data Mining Lab PS6-Dataset2.csv',)
import itertools

df



df
df.fillna(value='None', inplace=True)
df

transactions=[]
# Convert the grouped items into transactions
for index,row in df.iterrows():
  #print(row)
  if len(transactions)<row['Transaction']:
    transactions.append([row['Item']])
  else:
    transactions[row['Transaction']-1].append(row['Item'])

transactions

freq_item_set=dict()
indx=0
map_lex_item=dict()
for transaction in transactions:
    for index,item in enumerate(transaction):
      if(item not in map_lex_item):
        freq_item_set[chr(97+indx)]=1
        map_lex_item[item]=chr(97+indx)
        indx+=1
      else:
        freq_item_set[map_lex_item[item]]+=1
L1 = [key for key,value in freq_item_set.items() if value >= 0.4*len(transactions)]

L=[]
L.append([])
L.append(list(L1))

map_lex_item

freq_item_set

L

def infrequent_subset(c,L,k):
  subsets=list(itertools.combinations(list(c),k))
  for subset in subsets:
    s=''.join(subset)
    print('subset',s,L)
    if s not in L:
      return True
  return False

def apriori_gen(L,k):
  Ck=[]
  for i1 in L:
    for i2 in L:
      if(i1[0:k-1]==i2[0:k-1] and i1[-1]!=i2[-1]):
        # join i1..i2 with -1 and -1 added
     #   print('i1,i2,',i1,i2,k)
        c=i1[0:k]+(i2[-1])
        if(infrequent_subset(c,L,k)):

          print('invalid subset',c,'-----------------')
          pass
        else:
          print('valid subset',c,''.join(sorted(c)))
          if ''.join(sorted(c)) not in Ck:
            Ck.append(''.join(sorted(c)))
  return Ck

def filter_L2(ck):
  new_ck=[]
  for el in ck:
    print('el',el,'--------')
    c=0
    for transaction in transactions:
     # print(l,'l',transaction)
      t_changed=[]
      for i in transaction:
        t_changed.append(i[0])
      t_set=set(''.join(sorted(t_changed)))
    #  print('t_string',t_set,set(el))
      if(set(el).issubset(t_set)):
        c+=1
      else:
        c+=0
   # print('c',c,l)
    if(c>=0.4*len(transactions)):
      # it is valid
      print('valid count of pair',c,new_ck,el)
      new_ck.append(el)
    else:
      print('not frequent at all',c,ck,transactions)
 # print(new_ck,"newck")
  return new_ck

k=2
while(len(L[k-1])>0):
  Ck = apriori_gen(L[k-1],k-1)
  print('Ck',Ck,'-----------------')
  fC=filter_L2(Ck)
  print('ck-fc',len(Ck)-len(fC))
  L.append(fC)

  print(L)
  k+=1

k

inv_map = {v: k for k, v in map_lex_item.items()}

for row in L:
  if(len(row)>0):
    for item in row:
      print('item',inv_map[item])
