#!/usr/bin/python3
import IGAFrame
import svmutil

import argparse
import random
import math
import re
import os.path
import threading

class IBCGA_SVC(IGAFrame.GeneticOperators):
    def __init__(self, n_dimention, label, feature,
                 begin = 40,
                 end = 10,
                 nfold = 5, 
                 limit= 500, 
                 size= 128,
                 prob_crossover = 0.9, 
                 prob_mutation = 0.2
                 ):
        self.nfold = nfold
        self.n_dimention = int(n_dimention) + 4 + 4
        self.feature_len = int(n_dimention)
        self.generation = 0
        self.label = label
        self.feature = feature
        self.limit = limit
        self.size = size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation
        self.OA_init()
        self.fitnessn = 0
        self.begin = begin
        self.end = end
        self.aristogenics_fitind = ()
        self.aristogenics_fitind_g = ()
        
        report_no = 0
        while True:
            report_no += 1
            if (os.path.isfile('report'+str(report_no)) ):
                pass
            else:
                #self.report_tab = open('report'+str(report_no)+'.tab','w')
                self.report_txt = open('report'+str(report_no),'w')
                break
        
        pass

    # GeneticFunctions interface impls
    def probability_crossover(self):
        return self.prob_crossover

    def probability_mutation(self):
        return self.prob_mutation

    def initial(self,active_feature_no):
        return [self.random_chromo(active_feature_no) for j in range(self.size)]
        
    def pop_change_one(self, fits_pop):
        pop = [ ch for f, ch in fits_pop ]
        if(self.begin > self.end):
            for ind in pop:
                zero_index = []
                one_index = []
                for i in range(0,self.feature_len):
                    if (ind[i] == 1):
                        one_index.append(i)
                    else:
                        zero_index.append(i)
                    pass
                #ind[one_index[random.randint(0,len(one_index))]] = 0
                ind[random.choice(one_index)] = 0
                pass
        else:
            for ind in pop:
                zero_index = []
                one_index = []
                for i in range(0,self.feature_len):
                    if (ind[i] == 1):
                        one_index.append(i)
                    else:
                        zero_index.append(i)
                    pass
                ind[random.choice(zero_index)] = 0
                pass
            pass
        return [ (self.fitness(ch), ch) for ch in pop ]
    
    def fitness(self, chromo, fitness_value = ''):
        if (fitness_value):
            return fitness_value
            pass
        else:
            self.fitnessn += 1
            ddata = self.decode(chromo)
            cmd = '-v ' + str(self.nfold) + \
                  ' -c ' + str(ddata['params']['c']) + \
                  ' -g ' + str(ddata['params']['gamma'])+ \
                  ' -q'
            res = svmutil.svm_train(self.label, ddata['Ddata'], cmd)
            return res
            pass
        pass
        
    def mt_fitness(self, fitspop):
        threads = []
        for i in range(0,len(fitspop)):
            thread_ele = GA_fitness_thread(fitspop[i], self)
            thread_ele.start()
            threads.append(thread_ele)
            pass
        for i in threads:
            i.join()
            pass
        return fitspop
        pass

    def check_stop(self, fits_populations):
        check_stop_flag = False
        self.generation += 1
        best_match = list(sorted(fits_populations))[-1][1]
        fits = [f for f, ch in fits_populations]
        best = max(fits)
        #best = self.aristogenics_fitind[0]
        worst = min(fits)
        ave = sum(fits) / len(fits)
        
        #### double check #####
        #now_best_ind = (self.fitness(sorted(fits_populations)[-1][1][:]) , sorted(fits_populations)[-1][1][:])
        now_best_ind = sorted(fits_populations)[-1]
        if(now_best_ind[0] >= self.aristogenics_fitind_g[0]): 
            self.aristogenics_fitind_g = (now_best_ind[0],now_best_ind[1][:])
        if(now_best_ind[0] >= self.aristogenics_fitind[0]):
            self.aristogenics_fitind = (now_best_ind[0],now_best_ind[1][:])
        #######################

        print(
            "[G %3d] score=(%.2f, %.2f, %.2f) Fitness:%4d trap:%4d Feature no:%4d" %
            (self.generation, best, ave, worst, self.fitnessn, self.trap, sum(best_match[0:self.feature_len]))
            )
        
        if(self.generation >= self.limit ):
            result_decode = self.decode(self.aristogenics_fitind[1])
            self.report_txt.write(
            "score= %.2f Feature no:%4d Features:" %
            (self.aristogenics_fitind[0], sum(self.aristogenics_fitind[1][0:self.feature_len]))
            )
            self.report_txt.write("\n")
            self.report_txt.write(','.join( [ str(i+1) for i in result_decode['features']]))
            self.report_txt.write("\n")
            
            if(sum(best_match[0:self.feature_len]) == self.end):
                check_stop_flag = True
                
                print(''.join(['=' for i in range(0,50)]))
                self.report_txt.write('\n')
                self.report_txt.write(''.join(['=' for i in range(0,50)]))
                self.report_txt.write('\n')
                
                print(
                "Final result: Score:%.2f Feature_no:%4d, Feature:" %
                (self.aristogenics_fitind_g[0], sum(self.aristogenics_fitind_g[1][0:self.feature_len]) )
                )
                print(result_decode['features'])
                print(
                "c:%.8f g:%.8f" %
                (result_decode['params']['c'], result_decode['params']['gamma'] )
                )

                result_decode = self.decode(self.aristogenics_fitind_g[1])
                self.report_txt.write(
                "Final result: Score:%.2f Feature_no:%4d, Feature:" %
                (self.aristogenics_fitind[0], sum(self.aristogenics_fitind_g[1][0:self.feature_len]) )
                )
                self.report_txt.write("\n")
                self.report_txt.write(','.join( [ str(i+1) for i in result_decode['features']]))
                self.report_txt.write(
                " c:%.8f g:%.8f" %
                (result_decode['params']['c'], result_decode['params']['gamma'] )
                )
                
                self.report_txt.close()
                
            else:
                self.pop_change_one(fits_populations)
                self.aristogenics_fitind = (fits_populations[0][0], fits_populations[0][1][:])
                self.generation = 0
                
        return check_stop_flag # true if you want to stop evolution
        
    # def encode(self, in_arr):
        # out_arr = []
        # for i in in_arr:
            # out_arr.append( 1 if i < 0 else 0)
            # i = abs(i)
            # for j in range(0,9):
                # out_arr.append(i%2)
                # i = int(i/2)
        
        # return out_arr
        
    def mutation(self, chromosome):
        fitness_value , chrom = chromosome[:]
        zero_index = []
        one_index = []
        for i in range(0,self.feature_len):
            if (chrom[i] == 1):
                one_index.append(i)
            else:
                zero_index.append(i)
            pass
        chrom[random.choice(zero_index)] = 1
        chrom[random.choice(one_index)] = 0
        return (self.fitness(chrom),chrom)
    
    def decode(self, in_arr):
        c = [2**i for i in range(-4, 12)] # 4
        gamma = [ 2**i for i in range(-13, 3) ] # 4
        params={}
        
        # decode C
        bit_cnt = 0
        ele_cnt = 0
        for i in in_arr[self.feature_len:self.feature_len+4]: # c
            ele_cnt += (2 ** bit_cnt) * i
            bit_cnt += 1
        params['c'] = c[ele_cnt]
        #print(ele_cnt)
        
        # decide gamma
        bit_cnt = 0
        ele_cnt = 0
        for i in in_arr[self.feature_len+4:self.n_dimention]: # gamma
            #print(ele_cnt)
            ele_cnt += (2 ** bit_cnt) * i
            bit_cnt += 1
        params['gamma'] = gamma[ele_cnt]
        #print(ele_cnt)
                 
        feature_arr = [i for i in range(0, self.feature_len) if in_arr[i] == 1]
        
        sub_training_data = []
        for training_data_x in self.feature:
            new_idx = 0
            new_dataset = {}
            for i in feature_arr:
                new_idx = new_idx + 1
                try:
                    new_dataset[new_idx] = training_data_x[i]
                except:
                    pass
            sub_training_data += [new_dataset]
        #print(feature_arr)
        
        return({'params':params,
                'features':feature_arr,
                'Ddata':sub_training_data
                })
        pass

    def random_chromo(self, active_feature_no):
        chrom  = [1 for i in range(0,active_feature_no)]
        chrom += [0 for i in range(active_feature_no,self.feature_len)]
        random.shuffle(chrom)
        chrom += [random.randint(0, 1) for i in range(self.feature_len, self.n_dimention)]
        return chrom
        pass
    
    pass

class GA_fitness_thread(threading.Thread):
    def __init__(self, ind, ibcga_op):
        threading.Thread.__init__(self)
        self.ind = ind
        self.ibcga_op = ibcga_op
        pass
    
    def run(self):
        self.ind[0] = self.ibcga_op.fitness(self.ind[1], self.ind[0])
        return self
        pass
    
    
if __name__ == '__main__':
    cmdpar = argparse.ArgumentParser()
    #cmdpar.add_argument("-F", "--File", help=" indicate the training file")
    cmdpar.add_argument("-G", "--generation", default = 50, type = int , help=" Set the generation number of IBCGA (default: 10)")
    cmdpar.add_argument("-O", "--population_size", default = 50, type = int , help=" Set the population size of IBCGA (default: 50)")
    cmdpar.add_argument("-v", "--nfold", default = 10, type = int , help=" Set the cross validation number (default: 10)")
    cmdpar.add_argument("-B", "--begin", default = 40, type = int , help=" Set the feature number in the begin (default: 40)")
    cmdpar.add_argument("-E", "--end", default = 10, type = int , help=" Set the feature number in the end (default: 10)")
    cmdpar.add_argument("-F", "--trainfile", type = str , help=" Indicate the training file (default: none)")

    args = cmdpar.parse_args()

    # read and check parameters
    if ( os.path.isfile(args.trainfile) ):
        pass
    else:
        print("The training file " + args.trainfile + " is not existed")
        exit(1)
    
    training_data = {}
    training_data['labels'],training_data['features'],training_data['max_index'] = svmutil.svm_read_problem_ibcga(args.trainfile)
    
    if(int(args.begin) > int(training_data['max_index'])):
        print("The desired feature number is %2d, while the file contains %2d features" % ( int(args.begin), int(training_data['max_index'] )))
        exit(1)
    
    # run IBCGA
    IGAFrame.GeneticAlgorithm(IBCGA_SVC(training_data['max_index'], 
                                       training_data['labels'], 
                                       training_data['features'],
                                       nfold = args.nfold,
                                       limit = args.generation, 
                                       size = args.population_size,
                                       begin = args.begin,
                                       end = args.end
                                       )).run()
    pass


