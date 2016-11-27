"""Genetic Algorithmn Implementation
see:
http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
"""
##### this version toward to LARGE #####

import random
import heapq

class GeneticAlgorithm(object):
    def __init__(self, GA_operator):
        self.GA_operator = GA_operator # GA operator object
        pass

    def run(self):
        # "population" is a two dimention array, the first dimention is a chromosome while second dimention is a gene 
        population = self.GA_operator.initial(self.GA_operator.begin)
        # fits_pops => [(fitness1, [genes1]), ..., (fitnessN, [genesN])]
        fits_pops = [('', ch) for ch in population] # append the fitness value column
        self.GA_operator.aristogenics_fitind = (self.GA_operator.fitness(fits_pops[0][1]), fits_pops[0][1][:])
        self.GA_operator.aristogenics_fitind_g = (self.GA_operator.fitness(fits_pops[0][1]), fits_pops[0][1][:])
        while True:
             # fits_pops => [(fitness1, [genes1]), ..., (fitnessN, [genesN])]
            fits_pops = [ (self.GA_operator.fitness(ch, f), ch) for f, ch in fits_pops] # 'ch' is a chromosome
            now_best_ind = sorted(fits_pops)[-1]
            if(now_best_ind[0] > self.GA_operator.aristogenics_fitind_g[0]): 
                self.GA_operator.aristogenics_fitind_g = (now_best_ind[0],now_best_ind[1][:])
            if(now_best_ind[0] > self.GA_operator.aristogenics_fitind[0]):
                self.GA_operator.aristogenics_fitind = (now_best_ind[0],now_best_ind[1][:])
                self.GA_operator.trap = 0
            else: 
                self.GA_operator.trap += 1 
            
            if self.GA_operator.check_stop(fits_pops): break
            fits_pops = self.GA_operator.aristogenics(fits_pops) # aristogenics strategy
            fits_pops = self.iga_next(fits_pops)
            fits_pops = sorted(heapq.nlargest(self.GA_operator.size+1, fits_pops))[:self.GA_operator.size]
            pass
        return fits_pops

    def sga_next(self, fits):
        #parents_generator = self.GA_operator.parents(fits) #the original beautiful source code
        size = len(fits)
        nexts = []
        while len(nexts) < size:
            #parents = next(parents_generator) #the original beautiful source code
            parents = self.GA_operator.parents(fits)
            cross = random.random() < self.GA_operator.probability_crossover()
            children = self.GA_operator.crossover(parents) if cross else parents
            for ch in children:
                mutate = random.random() < self.GA_operator.probability_mutation()
                nexts.append(self.GA_operator.mutation(ch) if mutate else ch)
                pass
            pass
        return nexts[0:size]
        
    
    def iga_next(self, fits):
        #parents_generator = self.GA_operator.parents(fits) #the original beautiful source code
        size = len(fits)
        nexts = []
        while len(nexts) < size:
            #parents = next(parents_generator) #the original beautiful source code
            parents = self.GA_operator.parents(fits)
            cross = random.random() < self.GA_operator.probability_crossover()
            
            children = self.GA_operator.intelligent_crossover( parents ) if cross else parents

            for ch in children:
                #mutate = random.random() < self.GA_operator.probability_mutation()
                mutate = 1
                nexts.append( self.GA_operator.mutation(ch) if (mutate) else ch )
                pass
            pass
        return nexts[:]
        
    pass

class GeneticOperators(object):
    
    def __init__(self):
        r"""rewrite the __init__ subroutine"""
        self.n_dimention = 0
        self.feature_len = 0
    
    def OA_init(self, cut = 5):
        r"""returbn a orthogonal array used in IGA"""
        self.cutno = cut
        self.store_OA = self.gen_OA(self.cutno) # store the OA for further use
        self.aristogenics_fitind = () # aristogenics strategy
        self.trap = 0
        self.OA_fitspop =[]
        pass
    
    def probability_crossover(self):
        r"""returns rate of occur crossover(0.0-1.0)"""
        return 1.0
        
    def IGA_probability_crossover(self):
        r"""returns rate of occur IGA_crossover(0.0-1.0)"""
        return 0.5
        
    def IGA_trap(self):
        r"""returns if the GA is trapped. Trape is defined as the best individial is not changed"""
        return self.trap > 5
        #return 1

    def probability_mutation(self):
        r"""returns rate of occur mutation(0.0-1.0)"""
        return 0.0

    def initial(self):
        r"""returns list of initial population
        """
        return []

    def fitness(self, chromosome):
        r"""returns domain fitness value of chromosome
        """
        return len(chromosome)

    def check_stop(self, fits_populations):
        r"""stop run if returns True
        - fits_populations: list of (fitness_value, chromosome)
        """
        return False

    # def parents(self, fits_populations):
        # r"""generator of selected parents
        # """
        # gen = iter(sorted(fits_populations))
        # while TRUE:
            # f1, ch1 = next(gen)
            # f2, ch2 = next(gen)
            # yield(ch1,ch2)
        # return(ch1, ch2)
    
    def parents(self, fits_populations):
        father = self.tournament(fits_populations)
        mother = self.tournament(fits_populations)
        return (self.ind_cp(father), self.ind_cp(mother))
        
    ##### in the origianl source code --- keep it because it's beautiful but hard to understand #####
    # def parents(self, fits_populations):
        # while True:
            # father = self.tournament(fits_populations)
            # mother = self.tournament(fits_populations)
            # yield (father, mother)
            # pass
        # pass

    def OA_select(self, ndif):
        r"""store OA in the memry to decrease calculating. 
        """
        if(ndif == self.cutno):
            return self.store_OA
        else: # If the different of the chromosme is less than the factor number, generating new OA
            return self.gen_OA(ndif)   
        pass
        
    def gen_OA(self, factor = 5):
        r"""OA generatin subroutine """
        OA = []
        level=2
        temp= level-1

        J=1
        while (((level**J)-1)/temp)< factor:
            J+=1

        exp= level**J

        OA= [[0 for j in range(factor)] for i in range(exp)]

        remaind= exp
        pow_level_k= 1
        for k in range(0, J):
            j= (pow_level_k-1)/temp 
            remaind/= level 
            for i in range(0, exp):
                OA[i][int(j)]= int((i/int(remaind))%level)
            pow_level_k*= level

        pow_level_k= level
        for k in range(1, J):
            j= (pow_level_k-1)/temp 
            for s in range(0, int(j)): 
                for t in range(1, temp+1): 
                    if (t+j+s*temp)<factor:
                        for i in range(0, exp):
                            OA[i][int(t+j+s*temp)] = int((OA[i][s]*t+OA[i][int(j)])%level)
            pow_level_k*= level
        
        return(OA)
        pass
    
    # def crossover(self, parents):
        # father, mother = parents
        # index1 = random.randint(1, len(self.target) - 2)
        # index2 = random.randint(1, len(self.target) - 2)
        # if index1 > index2: index1, index2 = index2, index1
        # child1 = father[:index1] + mother[index1:index2] + father[index2:]
        # child2 = mother[:index1] + father[index1:index2] + mother[index2:]
        # return (child1, child2)
        
    def crossover(self, parents):
        father, mother = parents
        father_f, father_chrom = father
        mother_f, mother_chrom = mother
        candidate_cp = [ i for i in range(1,len(father_chrom)) if father_chrom[i] != mother_chrom[i] ] # make the candidate cut point list
        
        if(len(candidate_cp)==0):
            return( (father_f,father_chrom) , (mother_f,mother_chrom) )
            
        index1 = random.randint(1, len(father_chrom) - 2)
        index2 = random.randint(1, len(father_chrom) - 2)
        if index1 > index2: index1, index2 = index2, index1
        child1_chrom = father_chrom[:index1] + mother_chrom[index1:index2] + father_chrom[index2:]
        child2_chrom = mother_chrom[:index1] + father_chrom[index1:index2] + mother_chrom[index2:]
        #return ( ('',child1_chrom) , ('',child2_chrom) ) 
        return ( (self.fitness(child1_chrom),child1_chrom) , (self.fitness(child2_chrom),child2_chrom) )

    def intelligent_crossover(self, parents):
        father, mother = parents
        
        father_f, father_chrom = father
        mother_f, mother_chrom = mother
        
        #candidate_cp = [ i for i in range(1,len(father_chrom)) if father_chrom[i] != mother_chrom[i] ] # make the candidate cut point list
        # IBCGA cp
        candidate_cp = [ i for i in range(1,self.feature_len) 
                         if (
                            ( father_chrom[i] != mother_chrom[i] ) and 
                            ( sum(father_chrom[0:i]) == sum(mother_chrom[0:i]) )
                            )] # make the candidate cut point list
        candidate_cp += [i for i in range(self.feature_len, self.n_dimention) 
                         if ( father_chrom[i] != mother_chrom[i] )]

        # decide the cut point
        if(len(candidate_cp)<2):
            return (father, mother)
        elif(len(candidate_cp)==2):
        #elif(len(candidate_cp)>=2):
            child1_chrom = father_chrom[:candidate_cp[0]] + mother_chrom[candidate_cp[0]:candidate_cp[1]] + father_chrom[candidate_cp[1]:]
            child2_chrom = mother_chrom[:candidate_cp[0]] + father_chrom[candidate_cp[0]:candidate_cp[1]] + mother_chrom[candidate_cp[1]:]
            return ( (self.fitness(child1_chrom),child1_chrom) , (self.fitness(child2_chrom),child2_chrom) )
        else:
        
            ### decide the OA
            if(len(candidate_cp)>=self.cutno-1): # if cut points are more than 7, random choose 7 points
                random.shuffle(candidate_cp)
                candidate_cp = sorted(candidate_cp[:self.cutno-1])
                pass
            OA = self.OA_select(len(candidate_cp)+1)
            
            ### make OA population and calculate fitness
            OA_chrom = [ mother_chrom[:] , father_chrom[:] ]
            OA_popu = []
            candidate_cp = [0] + candidate_cp
            candidate_cp = candidate_cp + [len(father_chrom)]
            for OA_row in OA:
                OA_ele_no = 0
                child_temp = []
                for OA_ele in OA_row:
                    child_temp += OA_chrom[OA_ele][candidate_cp[OA_ele_no]:candidate_cp[OA_ele_no+1]]
                    OA_ele_no += 1
                    pass
                OA_popu.append(('',child_temp[:]))
                pass
            # assign the fitness of the OA_population
            OA_popfits = [(self.fitness(ch, f), ch) for f, ch in OA_popu]
            ### use paralle strategy ###
            #OA_popfits = self.mt_fitness(OA_popu)
            
            ### calculate MED
            MED_list = [ [0,0] for i in range(0,OA_ele_no)]
            fitness_arr = [f for f, ch in OA_popfits] # extract the fitness 
            # calculating MED
            OA_row_no = 0
            for OA_row in OA:
                OA_ele_no = 0
                for OA_ele in OA_row:
                    MED_list[OA_ele_no][OA_ele] += fitness_arr[OA_row_no]
                    OA_ele_no += 1
                    pass
                OA_row_no += 1
                pass
            # use MED to resconstruct theoritical optimal chromosome
            #MED_chrom = []
            child_temp = []
            OA_ele_no = 0
            for MED_col in MED_list:
                #MED_chrom.append( 1 if MED_col[1] > MED_col[0] else 0 )
                chr_sel = (1 if MED_col[1] > MED_col[0] else 0)
                child_temp += OA_chrom[chr_sel][candidate_cp[OA_ele_no]:candidate_cp[OA_ele_no+1]]
                OA_ele_no += 1
                pass
            OA_popfits.append((self.fitness(child_temp),child_temp))
            self.OA_fitspop += [ (f,ch[:]) for f, ch in OA_popfits[1:] ]
            OA_popfits.append((self.fitness(OA_chrom[0]),OA_chrom[0][:]))
            OA_popfits.append((self.fitness(OA_chrom[1]),OA_chrom[1][:]))
            child1 = (sorted(OA_popfits)[-1][0] , sorted(OA_popfits)[-1][1][:])
            child2 = (sorted(OA_popfits)[-2][0] , sorted(OA_popfits)[-2][1][:])
            
            return (child1,child2)

        pass
            
    
    def intelligent_mutation(self, chromosome):
        fitness_value , chrom = chromosome
        foriegn_chrom = self.random_chromo()
        mutant = chrom[:]
        mp = [ i for i in range(0,len(chrom)) ]
        random.shuffle(mp)
        candidate_mp = sorted(mp[:self.cutno-1])
        for index in candidate_mp:
            mutant[index] = mutant[index]^1 
            pass
        re_ind = self.intelligent_crossover( ( (self.fitness(mutant),mutant[:]), (fitness_value , chrom[:]) ) )
        return re_ind[1]
        
    
    def mutation(self, chromosome):
        fitness_value , chrom = chromosome[:]
        index = random.randint(0, len(chrom)-1)
        chrom[index] = chrom[index]^1 
        return (self.fitness(chrom),chrom)

    # internals
    def tournament(self, fits_populations):
        alicef, alice = self.select_random(fits_populations)
        bobf, bob = self.select_random(fits_populations)
        return (alicef,alice) if alicef > bobf else (bobf,bob)

    def select_random(self, fits_populations):
        return fits_populations[random.randint(0, len(fits_populations)-1)]
        
    def repair(self, fits_populations):
        new_fits_pop = []
        for ind in fits_populations:
            if(len(ind) == 2):
                new_fits_pop.append(ind)
                pass
            pass
        return new_fits_pop
        
    def aristogenics(self, fits_populations):
        fits_populations[0] = self.ind_cp(self.aristogenics_fitind)
        return fits_populations
        
    def ind_cp(self, chrom):
        return (chrom[0], chrom[1][:])
        


    pass


