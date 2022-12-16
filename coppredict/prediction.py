# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import coppredict.preprocessing as pr


def split_train_validation(df, train_ratio):
    np.random.seed(10)
    train, validate = np.split(df.sample(frac=1), [int(train_ratio * len(df))])
    train = train.reset_index(drop=True)
    validate = validate.reset_index(drop=True)
    return train, validate


def prepare_validation_data(df):
    df = df.reset_index(drop=True)
    df['last_item'] = ''
    df['aux_pattern'] = ''
    df['convert_pattern'] = ''
    df = df.astype(object)
    
    #print("---------")
    #print(df.shape)

    for i in range(len(df)):
        element = df.loc[i, "patterns"]
        last_item = element[-1:]
        without_last_item = element[:-1]
        
        #df.iloc[i, 5] = pr.convert_pattern_to_string(last_item)
        #df.iloc[i, 6] = pr.convert_pattern_to_string(without_last_item)
        #df.iloc[i, 7] = pr.convert_pattern_to_string(element)
        
        df.iloc[:, 5].loc[i] = pr.convert_pattern_to_string(last_item)
        df.iloc[:, 6].loc[i] = pr.convert_pattern_to_string(without_last_item)
        df.iloc[:, 7].loc[i] = pr.convert_pattern_to_string(element)
        

    return df


def predict_itemsets(ept, pattern, df_patterns, n_top):
    """
    Description:
    Finds the value of each one of the prediction candidates of the target pattern, and
    get the n_top predictions. Returns a dataframe with the results

    """
    df_patterns.reset_index(drop=True)
    df_patterns['sup_aux_pattern'] = ''

    for i in range(len(df_patterns)):
        element = df_patterns.loc[i, "sup_pattern"]
        df_patterns.iloc[i, 2] = pr.convert_list_to_string(element)

    df_patterns.drop_duplicates(subset="sup_aux_pattern", keep='first', inplace=True)
    input_support = ept.is_pattern(pattern)

    if input_support:
        df_result = pd.DataFrame()
        for index, row in df_patterns.iterrows():
            candidate = row['sup_pattern']
            aux_support = row['weight']

            div = aux_support/input_support
            df_result = df_result.append({'predict_pattern': candidate, 'result': div}, ignore_index=True)
               
            if len(df_result) >= n_top:
                df_result = df_result.sort_values('result', ascending=False).head(n_top)
                df_result.reset_index(drop=True)
            else:
                df_result = df_result.sort_values('result', ascending=False)
                df_result.reset_index(drop=True)

            df_result.reset_index(drop=True)

        return df_result.reset_index(drop=True)


def prediction(ntop_start, ntop_end, penalization, df_val, ept):
    confidences = []
    for n_top in range(ntop_start, ntop_end + 1):
        # print("*** n_top:", n_top)
        confidence_total = 0
        unpredictable = 0
        cases = 0

        for i in range(len(df_val)):
            pattern = df_val.iloc[i, 6]
            if len(pattern) >= 1:
                if ept.is_pattern(pattern):
                    # print("\n")
                    # print("- Target Pattern:", pattern)
                    validate_pattern = df_val.iloc[i, 5]
                    df_result = ept.get_super_patterns(pattern)
                    ll = []
                    if type(df_result) != bool and type(df_result) != str and not df_result.empty:
                        cases = cases + 1
                        df_result['sup_aux_pattern'] = ''
                        df_result = df_result.astype(object)
                        for r in range(len(df_result)):
                            element = df_result.loc[r, "sup_pattern"]
                            df_result['weight'] = df_result['weight'].apply(pd.to_numeric)
                            df_result.iloc[r, 2] = pr.convert_list_to_string(element)
                        
                        predict_dataframe = predict_itemsets(ept, pattern, df_result, n_top)
                        predict_dataframe['result_pred'] = ''
                        predict_dataframe['result_pred'] = predict_dataframe['result_pred'].astype('object')   

                        # pattern_aux = pattern.copy()

                        for k in range(len(predict_dataframe)):
                            pattern_aux = pattern.copy()
                            prediction_n = predict_dataframe.loc[k, 'predict_pattern']
                           
                            prediction_test_n = [i for i in prediction_n
                                                 if i not in pattern_aux or pattern_aux.remove(i)]
                            prediction_test_n = list(map(lambda st: str.replace(st, "--", "-"), prediction_test_n))
                            predict_dataframe.at[k, 'result_pred'] = prediction_test_n
                            ll.extend(prediction_test_n)

                        lm = list(set(ll))

                        # print("Predict dataframe: ")
                        # display(HTML(predict_dataframe.to_html()))
                        # print(predict_dataframe)

                        validate_pattern = list(map(lambda st: str.replace(st, "--", "-"), validate_pattern))
                        # print("- Real prediction:", validate_pattern)
                        # print("- Prediction candidates: ", lm)

                        div_1 = len(set(validate_pattern) & set(lm))
                        print("div 1: ", set(validate_pattern) & set(lm), div_1)
                        if div_1 > 0:
                            confidence_total = confidence_total + 1
                        else:
                            lm_aux = list(map(lambda st: str.replace(st, "--", "-"), lm))
                            lm_aux = list(map(lambda st: str.replace(st, "-", ""), lm_aux))
                           
                            div_aux = len(set(validate_pattern) & set(lm_aux))
                            print("div aux: ", set(validate_pattern) & set(lm_aux), div_aux)
                            if div_aux > 0:
                                confidence_total = confidence_total + (1 - penalization)
                    elif type(df_result) == bool:
                        unpredictable = unpredictable + 1
                    elif type(df_result) == str and df_result == 'Not Super patterns':
                        unpredictable = unpredictable + 1
                    else:
                        unpredictable = unpredictable + 1
                elif type(df_result) == bool:
                    unpredictable = unpredictable + 1
                elif type(df_result) == str and df_result == 'Not Super patterns':
                    unpredictable = unpredictable + 1
                else:
                    unpredictable = unpredictable + 1
            else:
                unpredictable = unpredictable + 1
        confi_final = round(confidence_total * 100 / cases, 2)
        confidences.append(confi_final)

    coverage = round(cases * 100 / (cases + unpredictable), 2)

    return cases, confidences, coverage
