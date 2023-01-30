
import numpy as np
import pandas as pd
from itertools import combinations

#convert the data into list of lists structure
def convertData(dataFrame):
  transactions = []

  for index, row in dataFrame.iterrows():
    itemList = []

    for column in dataFrame.columns.tolist():
      item = dataFrame[column][index]
      #to remove all the null values
      if pd.isna(item) == False:
        itemList.append(item)
    
    transactions.append(itemList)
  
  return transactions

#get the initial unique itemset
def getInitialItemSet(transactions):
  itemSet = []
  tempDict = {}

  for itemList in transactions:
    for item in itemList:
      tempDict[item] = 1
  
  for item in tempDict:
    itemSet.append([item])
    
    
  
  #sort it lexicographically
  itemSet.sort()

  return itemSet

#function to get itemSet above minSup
def getAboveMinSupport(itemSet, transactions, support):
  newItemSet = []
  minSup = support * len(transactions)

  def check(itemList, transaction):
    for item in itemList:
      if item not in transaction:
        return False
    
    return True

  for itemList in itemSet:
    freq = 0

    for transaction in transactions:
      if check(itemList, transaction):
        freq += 1

    if freq >= minSup:
      newItemSet.append(itemList)

  return newItemSet

#function to lexicographically join Li ItemSet
def joining(itemSet):
  newItemSet = []

  def check(list1, list2):
    if list1 == list2:
      return False
    
    for i in range(0,len(list1) - 1):
      if list1[i] != list2[i]:
        return False
    
    return True
  
  def combine(list1, list2):
    newList = []
    tempDict = {}

    for item in list1:
      tempDict[item] = 1

    for item in list2:
      tempDict[item] = 1
    
    for item in tempDict:
      newList.append(item)
    
    return newList

  for i in range(0, len(itemSet)):
    for j in range(i+1, len(itemSet)):
      newList = []
      itemList1 = itemSet[i]
      itemList2 = itemSet[j]

      if check(itemList1, itemList2):
        newList = combine(itemList1, itemList2)
      
      if len(newList) > 0:
        newItemSet.append(newList)
    
  return newItemSet

#prune itemset which are not satisfying the apriori property
def pruning(candidateSet, previousSet, length):
  newCandidateSet = []

  for itemList in candidateSet:
    flag = True
    subsets = combinations(itemList,length)

    for subset in subsets:
      check = list(subset)
      check.sort()
      if check not in previousSet:
        flag = False
    
    if flag:
      newCandidateSet.append(itemList)

  return newCandidateSet

#apriori function implementation
def apriori(transactions, support):
  frequentItemSets = []

  C1ItemSet = getInitialItemSet(transactions)
  L1ItemSet = getAboveMinSupport(C1ItemSet, transactions, support)

  count = 1
  currentLset = L1ItemSet
  while len(currentLset) > 0:
    frequentItemSets.append(currentLset)

    candidateSet = joining(currentLset)
    candidateSet = pruning(candidateSet, currentLset, count)
    currentLset = getAboveMinSupport(candidateSet, transactions, support)

    count += 1
  
  return frequentItemSets

#function to find all the strict association rules
def associationRules(frequentItemSets, transactions, confidence):
  associationRules = []

  def powerset(itemList):
    powerset = []

    for i in range(1,len(itemList)):
      subset = combinations(itemList,i)
      for s in subset:
        powerset.append(list(s))

    return powerset
  
  def difference(list1, itemList):
    list2 = []

    for item in itemList:
      if item not in list1:
        list2.append(item)
    
    return list2

  def support(itemList, transactions):
    support = 0

    for row in transactions:
      flag = True

      for item in itemList:
        if item not in row:
          flag = False
      
      if flag:
        support += 1
    
    return support
  

  for i in range(1,len(frequentItemSets)):
    freqItemSet = frequentItemSets[i]
    
    for itemList in freqItemSet:
      subsets = powerset(itemList)

      for list1 in subsets:
        list2 = difference(list1, itemList)
        conf = support(itemList, transactions)/ support(list1, transactions)
        if conf >= confidence:
          associationRules.append([list1, list2, conf])

  return associationRules

def main():
    dataFrame = pd.read_csv("data.csv", header = None)
    transactions = convertData(dataFrame)
    frequentItemSets = apriori(transactions, 0.3)
    rules = associationRules(frequentItemSets, transactions, 0.6)
    print(frequentItemSets,"\n\n\n\n")
    print(rules)

main()
