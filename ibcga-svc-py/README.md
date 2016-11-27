# IBCGA
intelligent binary combinatorial genetic algorithm

## Short Intro
IBCGA aim to select a feature set with the same number during evolution process.
This version use Python and libsvm to implemet the whole feature selection and 
svm model building system.

Before you use, some files are needed:
1. ibcga_svc_ma.py : this is the main file to execute IBCGA-SVC
2. IGAFrmae.py : this file contains IBCGA and its operators
3. libsvm.dll : If you use the Win32 system, the version contain the libsvm operators in win32 system
4. libsvm.so.2 : If you use the Linux system, the version contain the libsvm operators in win32 system
5. svm.py : the API of libsvm
6. svmutil.py : some useful tools use the libsvm API. PLEASE use this version, because the author 
                modify some little scripts.
7. your training file in libsvm format

## parameters 
The SVC use RBF kernel, and use the classical C-SVC in libsvm. This parameters can be easy modify from 
the python source code if you want to use other kernel or SVC.

"-G", "--generation", default = 50, type = int , help=" Set the generation number of IBCGA (default: 10)"
"-O", "--population_size", default = 50, type = int , help=" Set the population size of IBCGA (default: 50)"
"-v", "--nfold", default = 10, type = int , help=" Set the cross validation number (default: 10)"
"-B", "--begin", default = 40, type = int , help=" Set the feature number in the begin (default: 40)"
"-E", "--end", default = 10, type = int , help=" Set the feature number in the end (default: 10)"
"-F", "--trainfile", type = str , help=" Indicate the training file (default: none)"

For example:
1. python ibcga_svc_ma.py -G 50 -B 10 -E 8 -v 5 -F heart_scale

   This will select 10 feature in heart_scale (which has 13 features) with 5 fold cross validation.
   10 features are firstly selected and run the evolution process. After 50 generation, the population
   will turn on one gene of each individual. Ultil the features left 8, the evolution process will stop.
   
2. python ibcga_svc_ma.py -G 50 -B 12 -E 10 -v 10 -O 128 -F heart_scale
   
   This will make 128 individuals in IBCGA for evolution and select 12 feature in heart_scale (which has 
   13 features) with 10 fold cross validation. 10 features are firstly selected and run the evolution 
   process. After 50 generation, the population will turn on one gene of each individual. Ultil the features 
   left 10, the evolution process will stop.

Some suggestion:
* -B usually set 50 or 40 depending on the needs
* -E usually set to 10 or 5 depending on the needs
* Since GA is a non-determinstic method for looking for the optimal solution, executing more than one run is 
   necessary. The suggestion is 30 runs.
* Each run will generate a report (report1, report2). If the folder already contain the files, ibcga_svc_ma.py 
   will skip to aviod override the existing file.



                
