from numpy.random import randint
from numpy.random import rand
from random import sample
import time
import numpy as np
import random
#test=np.ones([16,16])
#np.fill_diagonal(test, 0)


#solution=test.flatten()


#objective function
def fitness(sequence):
    covd = 0
    total_poss_comb = n_bits*n_bits-n_bits
    #compare test particle with soultion
    for i in range(len(sequence)):
        #if (solution[i]== 1):
         #   total_poss_comb = total_poss_comb + 1
        if (sequence[i]  == 1):
                covd = covd + 1

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


# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            a = randint(len(bitstring))
            # print(a)
            temp = bitstring[i]
            bitstring[i] = bitstring[a]
            bitstring[a] = temp
    return bitstring


#check validity of child particles
def check_valid(sequence,n_bits):
    sequence= np.array(sequence)
    #print((len(sequence)))
    arr_2d=np.reshape(sequence,(n_bits,n_bits))
    #print(arr_2d)
    #print(len(arr_2d))
    #symmetry=(arr_2d == arr_2d.T).all()
    diag_0=1
    for i in range(len(arr_2d)):
        for j in range(len(arr_2d)):
            if (i==j):
                if(arr_2d[i][j]!=0):
                    diag_0=0
                #else:
                    #diag_0=0
    return (diag_0)#symmetry and

# genetic algorithm
def genetic_algorithm(fitness, n_bits, n_iter, n_pop, r_cross, r_mut):
    # initial population of random bitstring
    pop = []
    for i in range(n_pop):
        a = np.random.random_integers(0, 1, size=(n_bits, n_bits))
        sequence = np.tril(a) + np.tril(a, -1).T
        np.fill_diagonal(sequence, 0)
        pop.append(list(sequence.flatten()))
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
        for c in pop:

            if check_valid(c,n_bits)== 0:
                scores[count] = 0       #scores.append(fitness(c,solution))
            count+=1

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
        best_m = np.reshape(best, (n_bits, n_bits))
        print(best_m)
        print("BEST= {},Score= {}".format(best,best_eval))
    return [best_m, best_eval]


start_time = time.time()
# rows and columns
rows = 3
columns = 3
# define the total iterations
n_iter = 200
# bits
n_bits = rows *columns
# define the population size
n_pop = 200
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 1.0 / float(n_bits)
# perform the genetic algorithm search
best, score = genetic_algorithm(fitness, n_bits, n_iter, n_pop, r_cross, r_mut)
print("BEST= {},Score= {}".format(best,score))
print("---- Execution Time = {} seconds ----".format(np.around((time.time() - start_time),decimals=2)))

######TRAFFIC GENERATION
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