import scipy.stats as stats
import numpy as np
data_list = [ [3,3,3], [3,5,6], [4,8,9] ]



f,p = stats.f_oneway(data_list[0],data_list[1],data_list[2])
print(f,p)
