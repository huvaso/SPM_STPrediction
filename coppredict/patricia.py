# -*- coding: utf-8 -*-

import pandas as pd
import coppredict.preprocessing as pre


class Patricia:
    def __init__(self):
        self._data = {}

    def check_index(self, pattern, ind, case):
        """
        Atributes:
        pattern
        ind
        case


        """
        try:
            if case == 1:
                val = pattern[ind]
                return val

            elif case == 2:
                val = pattern[ind:]
                return val

        except IndexError:
            return ''

    def add_pattern(self, pattern, support):
        """
        Creates and adds a pattern

        Atributes:
            pattern
            support

        Example:
            [C1,C2,-C3,--C1,-C2,--C3,--C4] => C1C2-C3--C1-C2--C3--C4

        """
        data = self._data
        i = 0

        pattern = pre.convert_pattern_to_string(pattern)

        while 1:
            try:
                tmp = pattern[i]
                if isinstance(tmp, str):
                    node = data[tmp]
            except KeyError:
                if data:
                    ind = pattern[i]
                    rest = pattern[i+1:]
                    data[ind] = [rest, {support}]
                    return
                else:
                    if tmp == '':
                        return
                    else:
                        if i != 0:
                            data[''] = ['', {}]
                        data[pattern[i]] = [pattern[i+1:], {support}]
                    return
            i += 1

            if self.starts_with_sublist(pattern, node[0], i):
                if len(pattern[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            node[1]['']
                        except KeyError:
                            data = node[1]
                            data[''] = ['', {support}]
                    return
                else:
                    i += len(node[0])
                    data = node[1]
            else:
                ii = i
                j = 0
                while ii != len(pattern) and j != len(node[0]) and pattern[ii:ii+1] == node[0][j:j+1]:
                    ii += 1
                    j += 1
                tmp_data = {node[0][j]: [node[0][j + 1:], node[1]]}

                ind1 = self.check_index(pattern, ii, 1)
                ind2 = self.check_index(pattern, ii + 1, 2)
                tmp_data[ind1] = [ind2, {support}]
                data[pattern[i-1]] = [node[0][:j], tmp_data]
                return

    def starts_with_sublist(self, l, sub, i):
        """
        Check if a list starts with a sublist.

        """
        # It's independent of class scope
        return l[i:len(sub)+i] == sub

    def is_prefix(self, pattern):
        """
        Check if a pattern is a prefix.

        """
        data = self._data
        i = 0
        patternlen = len(pattern)
        while 1:
            try:
                node = data[pattern[i:i+1]]
            except KeyError:
                return False
            i += 1

            if pattern.startswith(node[0][:patternlen-i], i):
                if patternlen - i > len(node[0]):
                    i += len(node[0])
                    data = node[1]
                else:
                    return True
            else:
                return False

    def is_pattern(self, pattern):
        """
        Check if a pattern belongs to the Patricia Trie, if not, returns false.
        If yes, returns the weight stored.

        Atributes:
            pattern
        """
        data = self._data
        i = 0

        while 1:
            try:
                node = data[pattern[i]]
            except KeyError:
                return False
            except TypeError:
                return False
            i += 1
            if pattern[i:len(node[0])+i] == node[0]:
                if len(pattern[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            vl = node[1]['']
                        except KeyError:
                            return False
                        except IndexError:
                            return False
                        except TypeError:
                            aux = node[1]

                            return next(iter(aux))
                    aux = node[1][''][1]

                    return next(iter(aux))
                else:
                    i += len(node[0])
                    data = node[1]
            else:
                return False

    def remove_pattern(self, pattern):
        """
        Not used.

        """
        data = self._data
        i = 0
        while 1:
            try:
                node = data[pattern[i:i+1]]
            except KeyError:
                print("Pattern is not in trie.")
                return
            i += 1
            if pattern.startswith(node[0], i):
                if len(pattern[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            vl = node[1]['']
                            node[1].pop('')
                        except KeyError:
                            print("Pattern is not in trie.")
                        return
                    data.pop(pattern[i-1:i])
                    return
                else:
                    i += len(node[0])
                    data = node[1]
            else:
                print("Pattern is not in trie.")
                return

    def get_super_patterns(self, pattern):
        """
        Finds all the supper patterns of the input pattern and returns a dataframe with each supper pattern and its weight.

        """
        data = self._data

        df_sup = pd.DataFrame(columns=['sup_pattern', 'weight']).astype('object')
        i = 0
        patternlen = len(pattern)

        while 1:
            try:
                node = data[pattern[i]]
            except KeyError:
                return False

            i += 1

            if pattern[i:len(node[0])+i] == node[0]:
                if len(node[0]) == 0 and patternlen - i > 0:

                    i += len(node[0])
                    data = node[1]
                else:
                    for key in node[1]:

                        flag_float = isinstance(key, float)
                        if key == "":

                            node[1][key]
                        elif flag_float:
                            return "Not Super patterns"
                        else:
                            keylen = len(key)
                            if keylen >= 2:
                                # Prefix "-"
                                if key[0] == "-" and key[1] != "-":
                                    aux3 = pattern[:]
                                    aux3.append(key)
                                    aux_list = node[1][key]
                                    for aux in aux_list:
                                        if isinstance(aux, dict):
                                            for k, v in aux.items():
                                                aux4 = aux3.copy()
                                                aux4.append(k)
                                                if isinstance(v[1], dict):
                                                    for z, x in v[1].items():
                                                        if z != "":
                                                            if isinstance(x, list):
                                                                for ll in x:
                                                                    if isinstance(ll, dict):
                                                                        for m, n in ll.items():
                                                                            if m != "":
                                                                                # print("m!=")
                                                                                continue
                                                                            else:
                                                                                weight = self.is_pattern(aux4)
                                                                                if weight != False:
                                                                                    df_sup = df_sup.append({'sup_pattern': aux4, 'weight': weight}, ignore_index=True)

                                                                weight = self.is_pattern(aux4)
                                                                if weight != False:
                                                                    df_sup = df_sup.append({'sup_pattern': aux4, 'weight': weight}, ignore_index=True)
                                                        else:
                                                            weight = self.is_pattern(aux4)
                                                            if weight != False:
                                                                df_sup = df_sup.append({'sup_pattern': aux4, 'weight': weight}, ignore_index=True)
                                                if isinstance(v[1], set):
                                                    weight = self.is_pattern(aux4)
                                                    if weight != False:
                                                        df_sup = df_sup.append({'sup_pattern': aux4, 'weight': weight}, ignore_index=True)

                                        else:
                                            aux4 = aux3.copy()
                                            if isinstance(aux, list):
                                                if len(aux) != 0:
                                                    aux4.append(aux[0])
                                                    weight = self.is_pattern(aux4)
                                                    if weight != False:
                                                        df_sup = df_sup.append({'sup_pattern': aux4, 'weight': weight}, ignore_index=True)
                                else:
                                    # Prefix "--"
                                    if key[1] != "-":
                                        aux2 = pattern[:]
                                        aux2.append(key)
                                        weight = self.is_pattern(aux2)
                                        if weight != False:
                                            df_sup = df_sup.append({'sup_pattern': aux2, 'weight': weight}, ignore_index=True)
                            else:
                                aux6 = pattern[:]
                                aux6.append(key)
                                weight = self.is_pattern(aux6)
                                if weight != False:
                                    df_sup = df_sup.append({'sup_pattern': aux6, 'weight': weight}, ignore_index=True)
                    return df_sup
            else:
                return False

    __getitem__ = is_pattern
