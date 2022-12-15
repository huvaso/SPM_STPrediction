# COPpredict

## Created by
**Author:** Hilda Ana Samame Jimenez <br />
**Contact Details:** hsamame@pucp.edu.pe <br />
**Advisors:** Hugo Alatrista-Salas / Miguel Nuñez del Prado <br />
**Contact Details:** halatrista@pucp.pe <br />
**Maintainer:** Yoshitomi Eduardo Maehara Aliaga <br />
**Maintainer Details:** ye.maeharaa@up.edu.pe <br />
**Institution:** Pontificia Universidad Catolica del Peru
<br />

## Description
Algoritm for predicting next items using Temporal Restricted Sequential Pattern Mining. 

Link to pur paper: https://link.springer.com/article/10.1007/s12652-022-03808-x

Please, cite us using the following text.

> Alatrista-Salas, A., Maehara, Y., Nunez-del-Prado, M., Samamé, H.(2020). Recommender Systems using Temporal Restricted Sequential Patterns. *Artificial Intelligence and it's Application in Healthcare* (Submited)
<!---[[link]](https://link.springer.com/chapter/10.1007/978-3-030-57524-3_20)--->

Bibtex:
```
@inbook{alatrista2020recomender,
  title={Recommender Systems using Temporal Restricted Sequential Patterns},
  author={Alatrista-Salas, A. and Maehara, Y. and Nunez-del-Prado, M. and Samamé, H},
  booktitle={Artificial Intelligence and it's Application in Healthcare},
  pages={},
  year={2020},
  organization={CRC PRESS}
}
```

## Install
### Install COPpredict by Source Code

If you clone repository or download the source you can install in your environment you will use:
```
python setup.py install
```
or if you would install in your development environment you will use:
```
python setup.py develop
```
### Install COPpredict by PIP
you can install last release using:
```
pip install git+https://github.com/hsamame/tesishildavf.git
```
or a specific version using:
```
pip install git+https://github.com/hsamame/tesishildavf.git@v1.0
```

``coppredict`` depends on the following packages which will be installed by pip during the installation process
- ``pandas``
- ``numpy``
- ``psutil``
- ``IPython``

## Usage
## COPredict usage example
1. Read the CSV of WinCopper or Copper patterns dataset (an example of the input file is shown in the example folder). 
```python
from coppredict import preprocessing as pr
from coppredict.patricia import Patricia
from coppredict import evaluation as ev
from coppredict import prediction as pdt
path = 'patterns'
filename = 'Results_ps_f_spmf_at_274132_bank_full_sizek_rt_50_.txt'
df_patterns = pr.load_patterns_file(path, filename)
```
```
[['C1', 'C12', 'C1', 'C1', 'C1', 'C12', 'C12', 'C1', 'C1'], 274141, 0.5000173274505119]
[['C1', 'C1', 'C1', ['C1', 'C12'], 'C1', 'C1', 'C1', 'C1', ['C1', 'C12']], 274143, 0.5000209753348301]
[['C1', 'C12', 'C1', 'C1', 'C12', 'C12', 'C1', ['C1', 'C12']], 274145, 0.5000246232191484]
[['C12', 'C1', 'C1', 'C10', 'C1', 'C1', ['C1', 'C12']], 274150, 0.5000337429299442]
[['C1', 'C1', 'C1', 'C12', 'C1', 'C1', 'C12', 'C12', 'C1'], 274152, 0.5000373908142625]
[['C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C12', 'C12', 'C12'], 274156, 0.5000446865828991]
[['C1', 'C1', 'C12', 'C1', 'C1', 'C12', 'C12', 'C1', 'C1'], 274160, 0.5000519823515357]
[['C12', 'C12', 'C1', 'C12', ['C1', 'C12'], 'C1'], 274160, 0.5000519823515357]
[['C1', 'C1', 'C12', 'C1', 'C10', 'C1', ['C1', 'C12']], 274169, 0.500068397830968]
[['C3', ['C1', 'C12'], ['C1', 'C12']], 274177, 0.5000829893682411]
[['C1', ['C1', 'C12'], 'C1', ['C1', 'C3']], 274191, 0.5001085245584692]
...
```
2. Read the CSV of weights dataset (an example of the input file is shown in the example folder).
```python
path = 'weights'
filename = 'banks_weights2.csv'
weights = pr.load_weights(path, filename)
```
```
coicop,ratio_sol,ratio_usd,stddev,stddev.1
C1,63.67153415576611,19.632862871829406,156.185486703636,48.159170082683296
C2,61.253996571753525,18.887424827246093,224.982104627787,69.37233203291579
C3,87.27373059969138,26.910505735205433,311.359451877867,96.00644154858959
C4,288.2458042304866,88.87944077466852,517.554625539149,159.585898541847
C5,130.8184286626975,40.33733920555214,501.413658656495,154.608895993367
C6,110.22933123127815,33.988773367834476,480.76162710822604,148.240924671703
C7,56.099906071117,17.29818163765733,202.71255319761002,62.505604928487394
C8,61.13122631601993,18.849569109660315,112.42639097274599,34.666227950881
C9,482.7988450373302,148.86909267060116,657.3225044203369,202.682764950913
C10,86.41848307644429,26.646793582264486,304.736695984678,93.96434126036421
C11,156.57556260988437,48.27944842885606,444.496705792871,137.058781244502
C12,107.051075269127,33.00877087186558,628.878671563135,193.912222876487
```

3. Select variables to use in prediction and calculate weights for each patterns
```python
variable = 'coicop'
measure = 'ratio_sol'
df_patterns_weight = pr.calculate_weights_pattern(df_patterns, weights, variable, measure)
```

4. Perform data division in train and validation dataset
```python
# for this example have proportion 90 (train) /10 (validate)
train, validate = pdt.split_train_validation(df_patterns_weight, 0.9)
train = pr.order_by_sublen(train)

```

## References
[TODO]
