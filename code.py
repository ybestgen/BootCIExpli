'''
This code illustrates the use of paired_bootstrap_interval and Fisher_Pitman_paired_test. It is based on dummy data. 
Examples on real data are proposed here, which allows to reproduce the experiments presented in 
"Please, Don't Forget the Difference and the Confidence Interval when Seeking for the State-of-the-Art Status", 
accepted at LREC 2022.

The first example compares the findings from the LeaderBoard with those from a significance test and a confidence interval. 
It shows a well-known phenomenon in statistics: the same difference in scores will be statistically significant or not 
depending on the sample size.

The second example confirms that "statistically significant does not mean important", 
a clarification requested by a reviewer of the paper.

The expected output is as follows:
Accuracy Niter = 1000 Alpha = 0.050000 Minimum possible p-value = 0.001000

Example 1 : For the same difference in the leaderboard, as the sample size increases, the p-value decreases as does the length of the confidence interval.
Sample_Size | Mean_1  Mean_2 |  diff   p_value |  [   Low    diff    High ]
       100  | 0.7000  0.6000 | 0.1000 0.180000 |  [-0.0300  0.1000  0.2300] 
       250  | 0.7000  0.6000 | 0.1000 0.026000 |  [ 0.0200  0.1000  0.1800] 
       500  | 0.7000  0.6000 | 0.1000 0.001000 |  [ 0.0440  0.1000  0.1600] (With n_iter=1000, the p-value cannot be smaller than 0.001, but the confidence interval can shrink.
      1000  | 0.7000  0.6000 | 0.1000 0.001000 |  [ 0.0550  0.1000  0.1420] 
      2000  | 0.7000  0.6000 | 0.1000 0.001000 |  [ 0.0740  0.1000  0.1310] 


Example 2: When the difference is small, but the sample is very large, the test (p-value) is highly significant, but the lower bound of the confidence interval is close to 0.
Sample_Size | Mean_1  Mean_2 |  diff   p_value |  [   Low    diff    High ]
      1000  | 0.6700  0.6400 | 0.0300 0.181000 |  [-0.0080  0.0300  0.0680] 
      4000  | 0.6700  0.6400 | 0.0300 0.007000 |  [ 0.0088  0.0300  0.0503] 

'''

import numpy as np
from sklearn.metrics import accuracy_score
import sys
from BootCI import paired_bootstrap_interval
from BootCI.Fisher_Pitman_paired_test import fpreptest


def stat(pred, rep):
  return(accuracy_score(rep, pred))


def makeone():
  tm1=0
  tm2=0
  diff=0
  p_value=0
  tBCaLow=0 
  tBCaHigh=0
  nbr1_y=int(sample_size*prop1_y)
  y= np.concatenate((np.ones(nbr1_y), np.zeros(sample_size-nbr1_y)), axis=0)
  for i in range(NbrSample):
    x1 = np.zeros(sample_size) 
    x1[np.random.choice(sample_size, int(sample_size*seuil_x1), replace=False)] = 1  
    x1 = np.absolute(x1 - y) # randomly switch sample_size*seuil_x1 between 0 and 1 
    x2 = np.zeros(sample_size) 
    x2[np.random.choice(sample_size, int(sample_size*seuil_x2), replace=False)] = 1  
    x2 = np.absolute(x2 - y) # randomly switch sample_size*seuil_x2 between 0 and 1
    m1=accuracy_score(y,x1)
    tm1+=m1
    m2=accuracy_score(y,x2)
    tm2+=m2
    diff+=m1-m2
    p_value+=fpreptest(x1, x2, y, accuracy_score, n_iter) # use of a callable function from sklearn
    bs = paired_bootstrap_interval.Bootstrap(x1,x2,y, stat=stat,n_iter=n_iter) # allow to use any (meaningful) function
    BCaLow, BCaHigh = bs.get_confidence_interval(alpha, method='percentile') #'bias_corrected')  # bias_corrected is recommended, but slower
    tBCaLow+=BCaLow
    tBCaHigh+=BCaHigh  
  sys.stdout.write("  %8ld  | %6.4lf  %6.4lf | %6.4lf %8.6lf |  [%7.4lf  %6.4lf %7.4lf] \n" % (sample_size,tm1/NbrSample,tm2/NbrSample,diff/NbrSample,p_value/NbrSample,tBCaLow/NbrSample,diff/NbrSample,tBCaHigh/NbrSample))

np.random.seed(94731)

n_iter=1000
alpha=0.05
NbrSample=1
prop1_y=0.60
measure='Accuracy'

sys.stdout.write("\n%s Niter = %ld Alpha = %lf Minimum possible p-value = %lf\n" % (measure,n_iter,alpha,1/n_iter))

sys.stdout.write("\nExample 1 : For the same difference in the leaderboard, as the sample size increases, the p-value decreases as does the length of the confidence interval.\n")

sys.stdout.write("Sample_Size | Mean_1  Mean_2 |  diff   p_value |  [   Low    diff    High ]\n")

seuil_x1=0.30
seuil_x2=0.40
for sample_size in (100, 250, 500, 1000, 2000):
  makeone()

sys.stdout.write("\n\nExample 2: When the difference is small, but the sample is very large, the test (p-value) is highly significant, but the lower bound of the confidence interval is close to 0.\n")

sys.stdout.write("Sample_Size | Mean_1  Mean_2 |  diff   p_value |  [   Low    diff    High ]\n")

seuil_x1=0.33 
seuil_x2=0.36 
for sample_size in (1000,4000):
  makeone()
