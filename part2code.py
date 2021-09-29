#objective: find the probability of rolling 2 dices and getting the same number, using Monte Carlo.
import random
def rollDie(sides=6):
    return random.randint(1,sides)
def rollDice():
    result=[]
    for i in range(2):
        number=rollDie()
        result.append(number)
    return result
    
def trialSuccess():
    trial = rollDice()
    for i in range(1,7):
        if trial.count(i)==2:
            return True
    return False
    
def trialSuccesses(trials=100):
    count = 0
    for trial in range(trials):
        if trialSuccess():
            count+=1
    return count/trials