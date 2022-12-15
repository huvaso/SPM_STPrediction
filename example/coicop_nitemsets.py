from coppredict import preprocessing as pr
from coppredict.patricia import Patricia
from coppredict import evaluation as ev
from coppredict import prediction as pdt

import numpy as np

np.random.seed(10)

path = 'patterns'
filename = 'Results_ps_f_spmf_at_274132_bank_full_sizek_rt_50_.txt'
df_patterns = pr.load_patterns_file(path, filename)
#print(df_patterns)

path = 'weights'
filename = 'banks_weights2.csv'
weights = pr.load_weights(path, filename)
# print(weights)


### TODO: Modularize
variable = 'coicop'
measure = 'ratio_sol'
df_patterns_weight = pr.calculate_weights_pattern(df_patterns, weights, variable, measure)
print(df_patterns_weight)

### TODO: Modularize
train, validate = pdt.split_train_validation(df_patterns_weight, 0.9)
train = pr.order_by_sublen(train)
print(train)

### TODO: Modularize
# time_start = ev.get_time()
# mem_start = ev.get_process_memory()

X_trie = Patricia()

for i in range(len(train)):
    X_trie.add_pattern(train.loc[i, "patterns"], round(train.loc[i, "weight"], 4))

# time_end = ev.get_time()
# mem_end = ev.get_process_memory()

# ev.get_time_build(time_start, time_end, "Patricia built in ")
# ev.get_memory_build(mem_start, mem_end, "Patricia built using ")

# print(X_trie._data)
# print(X_trie._data['C1'])
### TODO: Modularize

validate = pdt.prepare_validation_data(validate)
print(validate)
### TODO: Modularize

# X_trie.get_super_patterns_print(['-C1', '--C10'])

time_start = ev.get_time()
mem_start = ev.get_process_memory()

cases, confidences, coverage = pdt.prediction(1, 10, 0.05, validate, X_trie)

time_end = ev.get_time()
mem_end = ev.get_process_memory()


# print(confidences)

# print(coverage)

# casos válidos

# print(cases)

# ev.print_time_build(time_start, time_end, "Prediction in ")

# ev.printMemoryBuild(mem_start, mem_end, "Prediction using ")

####