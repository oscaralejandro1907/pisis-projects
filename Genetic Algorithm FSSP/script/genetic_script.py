import numpy as np
import random
import queue
import time
import pandas as pd
import os


df = pd.read_csv("BestSolutionsAndBounds.csv",skiprows=0,skip_blank_lines=True,usecols=[0,1])
df=df.sort_values(by=['Instance'])

data=pd.DataFrame()

for x in os.listdir("."):
    if x.__contains__("txt"):

        # Reading Data
        f=open(x,'r')

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

        f.close()

        # Randomly generate an initial population

        def initialization(Npop):
            pop = []
            for i in range(Npop):
                p = list(np.random.permutation(jobs))
                while p in pop:
                    p = list(np.random.permutation(jobs))
                pop.append(p)
            return pop

        # Calculate makespan

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

            job = qMachines[0].get()   #Remove and return the first job from the queue qMachine
            qTime.put((time + pt[job][0], 0, job))  #Put the time, the machine 0, and the get job in qTime
            busyMachines[0] = True    #The machine 0 is busy

            while True:    #Infinite loop
                time, machine, job = qTime.get()    #Get the time, machine and job put in the qTime
                if job == solution[jobs - 1] and machine == machines - 1: #Break the cycle when the job and the machine are
                    break                                                 #the last ones
                busyMachines[machine] = False
                if not qMachines[machine].empty():         #If the queue of the machine is not empty do:
                    j = qMachines[machine].get()           #Save in j the value get in qMachine
                    qTime.put((time + pt[j][machine], machine, j))    #Put in qTime the next time, machine and job
                    busyMachines[machine] = True       #The next machine is busy
                if machine < machines - 1:             #If machine
                    if busyMachines[machine + 1] == False:
                        qTime.put((time + pt[job][machine + 1], machine + 1, job))
                        busyMachines[machine + 1] = True
                    else:
                        qMachines[machine + 1].put(job)

            return time

        # Selection operator

        def selection(pop):
            popMakespan=[]
            for i in range(len(pop)):
                popMakespan.append([makespan(pop[i]),i])

            popMakespan.sort(reverse=True)

            distr=[]
            distrInd=[]

            for i in range(len(pop)):
                distrInd.append(popMakespan[i][1])
                prob=(2*(i+1))/(len(pop)*(len(pop)+1))
                distr.append(prob)

            parents=[]
            while len(parents) != len(pop):
                pair = list(np.random.choice(distrInd, 2, p=distr))
                if pair[0] != pair[1] and pair not in parents:
                    parents.append(pair)

            return parents

        # Crossover operator

        def crossover(parents):
            points = list(np.random.permutation(np.arange(jobs-1)+1)[:2])

            if points[0] > points[1]:
                points[0], points[1] = points[1], points[0]

            child = list(parents[0])

            for i in range(points[0],points[1]):
                child[i]=-1

            p = -1
            for i in range(points[0],points[1]):
                while True:
                    p += 1
                    if parents[1][p] not in child:
                        child[i] = parents[1][p]
                        break

            return child

        # Mutation operator

        def mutation(child):
            points = list(np.random.permutation(np.arange(jobs))[:2])

            if points[0] > points[1]:
                points[0], points[1] = points[1], points[0]

            movedJob = child[points[1]]

            for i in range(points[1], points[0], -1):
                child[i] = child[i-1]

            child[points[0]] = movedJob

            return child

        # Elitist update strategy

        def elitistStrategy(oldPop, newPop):
            bestSolInd=0
            bestSol = makespan(oldPop[0])

            for i in range(1, len(oldPop)):
                tempMakespan = makespan(oldPop[i])
                if tempMakespan < bestSol:
                    bestSol = tempMakespan
                    bestSolInd=i

            randomInd=random.randint(0,len(newPop)-1)

            newPop[randomInd] = oldPop[bestSolInd]

            return newPop

        # Return the best solution
        def bestSolution(pop):
            bestMakespan = makespan(pop[0])
            bestIndividual = 0
            for i in range(1,len(pop)):
                tMakespan = makespan(pop[i])
                if tMakespan < bestMakespan:
                    bestMakespan = tMakespan
                    bestIndividual = i

            return bestIndividual, bestMakespan

        # MAIN SOLVER

        # Population size
        Npop = 100
        # Probability of crossover
        Pc = 1.0
        # Probability of mutation
        Pm = 1.0
        # Stopping condition
        stopGeneration = 25

        # Start timer
        start = time.time()

        # Create initial population
        population = initialization(Npop)

        # Run the algorithm until the stopping condition
        for i in range(stopGeneration):
            b_clock = time.time()
            e_clock = time.time()
            while e_clock - b_clock <= 1:
                # Select the parents
                parents = selection(population)

                childs=[]

                # Apply crossover
                for p in parents:
                    childs.append(crossover([population[p[0]], population[p[1]]]))

                # Apply mutation
                for c in childs:
                    c = mutation(c)

                # Update population
                population = elitistStrategy(population, childs)

                #End Timer
                e_clock = time.time()

            break

        #Stop Timer
        end = time.time()
        # Result
        bestSequence, bestMakespan = bestSolution(population)

        #Execution time
        exe_time=end-start

        row = pd.DataFrame({'Instance':[x],
                            'ObjValue': bestMakespan,
                            'ExecutionTime': exe_time})

        data=data.append(row)

data['Instance']=data['Instance'].str.replace('.txt','')
data=data.sort_values(by=['Instance'])

df = df.reset_index(drop=True)
data = data.reset_index(drop=True)

table=df.merge(data, on='Instance', how='left')

r = pd.DataFrame(table)

result=r.assign(GAP = ((r.ObjValue - r.UB)/r.UB)*100)

print(result)
result.to_csv('dataframe.csv',index=False)