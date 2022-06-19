# BootCIExpli

This code illustrates the use of paired_bootstrap_interval and Fisher_Pitman_paired_test. It is based on dummy data. Examples on real data are proposed here: https://github.com/ybestgen/BootCIRealData, which allows to reproduce the experiments presented in "Please, Don't Forget the Difference and the Confidence Interval when Seeking for the State-of-the-Art Status", accepted at LREC 2022.


## Installation
Package is [available on PyPI](https://pypi.org/project/BootCI/) and can be installed using pip:  
``` pip install BootCI ```

## Contents

### paired\_bootstrap\_interval.py

This python function allows to compute bootstrap confidence intervals (CIs) for paired samples. It is based on the *bootstrap\_interval* module by Alexander Neshitov  (https://pypi.org/project/bootstrap-interval/, MIT Licence) which implements the bootstrap CI for one sample. 

For its use, see the paper and code.py. The performance measure can be any measure provided by a standard python library or defined by the user. It must be provided in a function called *stat*. It should be noted that this function has a significant impact on the computation time since it is called twice for each resampling (and also twice the number of instances in the test material if the BCa method (which is recommended) is used).

If you use this function, I would appreciate a citation to the following paper:
Bestgen, Y. 2022. Please, don't forget the difference and the confidence interval when seeking for the state-of-the-art status. *Proceedings of the 13th Conference on Language Resources and Evaluation (LREC 2022)*.

### Fisher\_Pitman\_Paired\_Test.py

This python function implements the Fisher-Pitman test for paired samples. As the bootstrap CI, this test is based on a resampling procedure.

For its use, see the paper and code.py. The performance measure can be any measure provided by a standard python library or defined by the user. It must be provided in a function called *stat*. It should be noted that this function has a significant impact on the computation time since it is called twice for each resampling.

If you use this function, I would appreciate a citation to the following paper:
Bestgen, Y. 2022. Please, don't forget the difference and the confidence interval when seeking for the state-of-the-art status. *Proceedings of the 13th Conference on Language Resources and Evaluation (LREC 2022)*.

### code.py

The first example compares the findings from the LeaderBoard with those from a significance test and a confidence interval. It shows a well-known phenomenon in statistics: the same difference in scores will be statistically significant or not depending on the sample size.

The second example confirms that "statistically significant does not mean important", a clarification requested by a reviewer of the paper.

To run this code, you can
- Install BootCI package with pip
- Download code.py
- Run `python3 code.py`.

The expected output is as follows:
```
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
```

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

## References

Bestgen, Y. 2022. Please, don't forget the difference and the confidence interval when seeking for the state-of-the-art status. *Proceedings of the 13th Conference on Language Resources and Evaluation (LREC 2022)*.

