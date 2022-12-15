# -*- coding: utf-8 -*-

import coppredict.util as util
import pandas as pd
from ast import literal_eval


def load_patterns_file(path, filename):
    path_res = '%s/%s' % (path, filename)
    df_patterns = util.extract_patterns(path_res)
    df_patterns['patterns'] = df_patterns.patterns.apply(lambda x: literal_eval(str(x)))
    df_patterns['len'] = df_patterns['patterns'].str.len()
    df_patterns = df_patterns.sort_values(by='len', ascending=False)
    df_patterns.reset_index(drop=True)

    return df_patterns


def load_weights(path, filename):
    path_res = '%s/%s' % (path, filename)
    weights = pd.read_csv(path_res)
    
    return weights


def calculate_weights_pattern(df, weights, variable, measure):
    size_df = len(df)
    label_patterns = 'patterns'

    for i in range(size_df):
        weight_pattern = 0
        element = df.loc[i, label_patterns]
        # supp = df.loc[i, label_support]

        for j in element:
            if isinstance(j, list):
                for k in j:
                    aux_ratio = weights.loc[weights[variable] == k][measure].values[0]
                    weight_pattern = weight_pattern + aux_ratio
            else:
                aux_ratio = weights.loc[weights[variable] == j][measure].values[0]
                weight_pattern = weight_pattern + aux_ratio

        weight_pattern = round(weight_pattern / size_df, 3)
        df.loc[i, 'weight'] = weight_pattern

    return df



def order_by_sublen(df):
    """
    In case of k-itemsets allow sort by subsequence size

    Atribute:
        df: dataframe to be sort
    Example:

    """
    for i in range(len(df)):
        element = df.loc[i, "patterns"]
        df.loc[i, "sublen"] = 0

        for j in element:
            if isinstance(j, list):
                df.loc[i, "sublen"] = len(j)
            else:
                continue

    df.sort_values(['len', 'sublen'], ascending=[False, False], inplace=True)
    df = df.reset_index(drop=True)

    return df


def convert_pattern_to_string(pattern):
    """
    Converts a pattern to explicit format where "-" indicates the beginning of an
    itemset inside the main pattern and "--" indicates that the next item belongs to that itemset.
    Each "-" means the begin of a new itemset of length greater than 1.

    Atributes:
        original_pattern: Pattern to convert

    Example:
        [C1,C2,[C3,C1],[C2,C3,C4]] => [C1,C2,-C3,--C1,-C2,--C3,--C4]

    """
    result_pattern = []
    for ix in pattern:
        # Flag to check if it's the beginning of an itemset inside pattern.
        first = True
        # Check if the item is an itemset of length greater than 1 (list).
        if isinstance(ix, list):
            for jj in ix:
                if first:
                    # If it's the beginning, add a "-"
                    result_pattern.append('-'+jj)
                    first = False
                else:
                    # If it's the continuation of the itemset, add "--"
                    result_pattern.append('--'+jj)
        else:
            result_pattern.append(ix)

    return result_pattern


def convert_list_to_string(lists):
    """
    Atributes:
        lists: list to convert
    Example:
        [C1, C2, C3] => "C1C2C3"
    """
    str1 = ""
    return str1.join(lists)


def get_disjoint(a, b):
    """
    Atributes

    Example:
         
    """
    return not set(a).isdisjoint(b)
