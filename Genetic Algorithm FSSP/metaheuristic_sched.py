import numpy as np
import random
import queue

#Reading Data
f=open('data0.txt','r')

line = f.readline()
line_split = line.split()

jobs=int(line_split[0])
machines=int(line_split[1])

#Create the data for processing time
pt = []
for i in range(jobs):
    line = f.readline().split()
    new=[]
    for j in range(machines):
        new.append(int(line[2*j+1]))
    pt.append(new)

print("List of processing times:",pt)

f.close()

#Randomly generate an initial population

def initialization(Npop):
    pop = []
    for i in range(Npop):
        p = list(np.random.permutation(jobs))
        while p in pop:
            p = list(np.random.permutation(jobs))
        pop.append(p)
    return pop

#Calculate makespan

def makespan(solution):
    qTime = queue.PriorityQueue()

    qMachines = []                                      #Creates a list where every jobs will be assign to each machine
    for i in range(machines):
        qMachines.append(queue.Queue())      #Add in every machine i (item of a list) a queue (list) of infinite values

    for i in range(jobs):
        qMachines[0].put(solution[i])                           #Put the job i in the first machine to begin processing

    busyMachines = []
    for i in range(machines):
        busyMachines.append(False)

    time = 0

    job = qMachines[0].get()                                   #Remove and return the first job from the queue qMachine
    qTime.put((time + pt[job][0], 0, job))                       #Put the time, the machine 0, and the get job in qTime
    busyMachines[0] = True                                                                       #The machine 0 is busy

    while True:                                                                                          #Infinite loop
        time, machine, job = qTime.get()                                #Get the time, machine and job put in the qTime
        if job == solution[jobs - 1] and machine == machines - 1:     #Break the cycle when the job and the machine are
            break                                                     #the last ones
        busyMachines[machine] = False
        if not qMachines[machine].empty():                                #If the queue of the machine is not empty do:
            j = qMachines[machine].get()                                           #Save in j the value get in qMachine
            qTime.put((time + pt[j][machine], machine, j))                 #Put in qTime the next time, machine and job
            busyMachines[machine] = True                                                      #The next machine is busy
        if machine < machines - 1:                                                  #If machine
            if busyMachines[machine + 1] == False:
                qTime.put((time + pt[job][machine + 1], machine + 1, job))
                busyMachines[machine + 1] = True
            else:
                qMachines[machine + 1].put(job)

    return time

population=initialization(7)
print("This is the population",population)

ms=makespan(population[0])
print(ms)

def selection(pop):
    popMakespan=[]
    for i in range(len(pop)):
        popMakespan.append([makespan(pop[i]),i])

    popMakespan.sort(reverse=True)
    print(popMakespan)

    distr=[]
    distrInd=[]

    for i in range(len(pop)):
        distrInd.append(popMakespan[i][1])
        print("These are the individuals",distrInd)
        prob=(2*(i+1))/(len(pop)*(len(pop)+1))
        distr.append(prob)
        print("With it probability to be chosen",distr)

    parents=[]
    for i in range(len(pop)):
        parents.append(list(np.random.choice(distrInd,2, p=distr)))

    return parents

sel_proc=selection(population)
print(sel_proc)


def crossover(parents):
    pos = list(np.random.permutation(np.arange(jobs)))
    print(pos)

cross=crossover(parents)
print(cross)
    



