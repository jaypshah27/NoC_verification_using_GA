from numpy.random import randint
from numpy.random import rand
from random import sample
import time
import numpy as np
import random

#PARAMETERS
# rows and columns
rows = 2
columns = 2
max_pack= 12
# define the total iterations
n_iter = 5
# bits
n_bits = rows *columns
# define the population size
n_pop = 100
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 0.9#1.0 / float(n_bits)
const=max(rows,columns)+1

#objective function
def fitness(sequence):

    covd = 0
    total_poss_comb = n_bits * n_bits - n_bits
    for i in range(len(sequence)):

        if (sequence[i]  > 0):
            covd = covd+1

    fitness_value = (covd/ total_poss_comb) * 100
    #print(fitness_value)
    return fitness_value


# tournament selection
def selection(pop, scores):
    #print(scores)
    selected = []
    for i in range(2):
        l = scores.index(max(scores))
        selected.append(pop[l])
        scores[l] = -1
    return selected


# crossover two parents to create two children
def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    p1 = list(p1)
    p2 = list(p2)
    # check for recombination
    if rand() < r_cross:
        k = randint(0, len(p1))
        #print("Crossover point :", k)

        # interchanging the genes
        # for i in range(k, len(p1)):
        #    p1[i], p2[i] = p2[i], p1[i]
        # p1 = ''.join(p1)
        # p2 = ''.join(p2)
        c1 = np.append(p1[:k], p2[k:])
        c2 = np.append(p2[:k], p1[k:])
        #print(c1)
        #print(c2, "\n\n")
        ch1=c1
        #return [p1, p2]
    else:
        ch1 = p1
    return [ch1]

def mutation(bitstring, r_mut):
    #print("INSIDE")
    #print(bitstring)

# check for a mutation
    for i in range(n_bits):
        if rand() < r_mut:
            a = random.randint(0, len(bitstring) - 1)
            #print(a)
            #print(bitstring)
            #print(sum(bitstring))
            if bitstring[a]>const:
                bitstring[a] = 0
            else :
                bitstring[a] = bitstring[a]+1
                if sum(bitstring)> max_pack:
                    bitstring[a] = bitstring[a] - 1

        #print(bitstring)
    return bitstring

def randofsum_unbalanced(s, n):
    # Where s = sum (e.g. 40 in your case) and n is the output array length (e.g. 4 in your case)
    r = np.random.rand(n)
    #print(r)
    a = np.array(np.round((r/np.sum(r))*s,0),dtype=int)
    #print(a)
    while np.sum(a) > s:
        r1=np.random.choice(n)
        if(a[r1]!=0):
            a[r1] -= 1
    while np.sum(a) < s:
        r2 = np.random.choice(n)
        #if (a[r2] != const-1 or const):
        a[np.random.choice(n)] += 1
    return a

# genetic algorithm
def genetic_algorithm(fitness, n_bits, n_iter, n_pop, r_cross, r_mut,max_pack):
    # initial population of random bitstring
    pop = []
    cores=n_bits*n_bits-n_bits
    for i in range(n_pop):
        n = random.randint(0, max_pack)
        #print(n)
        x = randofsum_unbalanced(n, cores)
        pop.append(x)

    print("Initial Population: ")
    print(pop)
    # keep track of best solution

    best, best_eval = pop[0], fitness(pop[0])
    #print(best_eval)
    # print(objective(pop[0]))
    # enumerate generations
    for gen in range(n_iter):
        print("GEN= {}".format(gen))
        # evaluate all candidates in the population
        #print(pop)

        scores = [fitness(c) for c in pop]
        count=0
        """
        for c in pop:

            if check_valid(c,n_bits)== 0:
                scores[count] = 0       #scores.append(fitness(c,solution))
            count+=1
        """
        #print(pop)
        #print(scores)

        #for i in range(len(scores)):
         #   if (scores[i]==100):
          #      break
        # check for new best solution
        for i in range(n_pop):
            if (scores[i] >best_eval):
                best, best_eval = pop[i], scores[i]
                #print(best, best_eval)
                print("iteration {}, new best f({}) = {}".format(i, pop[i], scores[i]))
            # select parents
        selected = selection(pop, scores)
        #print(selected)
        # print(selected)
        # create the next generation
        children = []
        for i in range(0, n_pop):
            # get selected parents in pairs
            x = randint(len(selected))
            y = randint(len(selected))
            while x == y:
                x = randint(len(selected))
                y = randint(len(selected))

            p1 = selected[0]
            p2 = selected[1]
            #print("SELECTED")
            #print(p1,p2)
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):

                # mutation
                mutation(c, r_mut)
                # store for next generation
                children.append(c)

            # replace population
        pop = children
        #print(pop)
        best_m = np.reshape(best, (n_bits, n_bits-1))
        print(best)
        print("BEST= {},Score= {}".format(best,best_eval))
    return [best_m, best_eval]


start_time = time.time()


# perform the genetic algorithm search
best, score = genetic_algorithm(fitness, n_bits, n_iter, n_pop, r_cross, r_mut,max_pack)
print("BEST= {},Score= {}".format(best,score))
print("---- Execution Time = {} seconds ----".format(np.around((time.time() - start_time),decimals=2)))

######TRAFFIC GENERATION
"""
total_cores=rows *columns
payloads=3
lst = list(range(0, total_cores))
for i in range(0,total_cores):
    name="core"+str(i)
    f=open(name+".txt","w")
    random.shuffle(lst)
    for j in lst:
        if (best[i][j]==1):
            lbs=i//columns
            source_l = bin(lbs).replace('0b', '')
            x = source_l[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            source_l = x[::-1]
            ubs = i % columns
            source_u = bin(ubs).replace('0b', '')
            x = source_u[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            source_u = x[::-1]
            source=str(source_l)+str(source_u)
            ######################
            lbd = j // columns
            dest_l = bin(lbd).replace('0b', '')
            x = dest_l[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            dest_l = x[::-1]
            ubd = j % columns
            dest_u = bin(ubd).replace('0b', '')
            x = dest_u[::-1]  # this reverses an array
            while len(x) < 4:
                x += '0'
            dest_u = x[::-1]
            dest = str(dest_l) + str(dest_u)


            rand_ls=np.random.random_integers(0, 1, size=(13))
            rand_ls=str(rand_ls).replace(" ", "")
            rand_ls = str(rand_ls).replace("[", "")
            rand_ls = str(rand_ls).replace("]", "")
            h_f= "001"+str(rand_ls)+str(source)+str(dest)
            f.write(h_f)
            f.write("\n")
            for k in range(payloads):
                pay_ls = np.random.random_integers(0, 1, size=(29))
                pay_ls = str(pay_ls).replace(" ", "")
                pay_ls = str(pay_ls).replace("[", "")
                pay_ls = str(pay_ls).replace("]", "")
                p_f="000"+str(pay_ls)
                f.write(p_f)
                f.write("\n")
            t_f="01000000000000000000000000000000"
            f.write(t_f)
            f.write("\n")
            f.write("01111111111111111111111111111111")
            f.write("\n")

    f.close()
"""