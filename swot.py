import pandas as pd
import numpy as np


class Swot(object):

    def __init__(self):
        self.st_table: pd.DataFrame = None
        self.so_table: pd.DataFrame = None
        self.wt_table: pd.DataFrame = None
        self.wo_table: pd.DataFrame = None
        self.str: pd.DataFrame = None
        self.weak: pd.DataFrame = None
        self.opp: pd.DataFrame = None
        self.thr: pd.DataFrame = None

    def assert_fields(self):
        assert self.st_table.shape[0] == self.so_table.shape[0], \
            f"Number of rows in ST table ({self.st_table.shape[0]})" \
            f" is not equal to number of rows in SO table ({self.so_table.shape[0]})"

        assert self.st_table.shape[1] == self.wt_table.shape[1], \
            f"Number of columns in ST table ({self.st_table.shape[1]})" \
            f" is not equal to number of columns in WT table ({self.wt_table.shape[1]})"

        assert self.wt_table.shape[0] == self.wo_table.shape[0], \
            f"Number of rows in WT table ({self.wt_table.shape[0]})" \
            f" is not equal to number of rows in WO table ({self.wo_table.shape[0]})"

        assert self.so_table.shape[1] == self.wo_table.shape[1], \
            f"Number of columns in SO table ({self.so_table.shape[1]})" \
            f" is not equal to number of columns in WO table ({self.wo_table.shape[1]})"

        assert self.st_table.shape[0] == self.str.shape[0], "Check number of strengths!"
        assert self.st_table.shape[1] == self.thr.shape[0], "Check number of threats!"
        assert self.wo_table.shape[0] == self.weak.shape[0], "Check number of weaknesses!"
        assert self.wo_table.shape[1] == self.opp.shape[0], "Check number of opportunities!"

    def update_indices_and_columns(self):
        self.st_table.index = self.str
        self.st_table.columns = self.thr
        self.wt_table.index = self.weak
        self.wt_table.columns = self.thr
        self.so_table.index = self.str
        self.so_table.columns = self.opp
        self.wo_table.index = self.weak
        self.wo_table.columns = self.opp

    def view_selected_table(self, selected_piece_of_table):
        return self.st_table.style.background_gradient(cmap="Purples", axis=None, low=0.5, high=1.0).set_precision(1) if selected_piece_of_table == "ST" else\
             self.so_table.style.background_gradient(cmap="Greens", axis=None, low=0.5, high=1.0).set_precision(1) if selected_piece_of_table == "SO" else\
             self.wt_table.style.background_gradient(cmap="Oranges", axis=None, low=0.5, high=1.0).set_precision(1) if selected_piece_of_table == "WT" else\
             self.wo_table.style.background_gradient(axis=None, low=0.5, high=1.0).set_precision(1)

    def create_full_table(self):
        strength_table = pd.concat([self.st_table, self.so_table], axis=1)
        strength_table.columns = np.append(self.thr, self.opp)
        weakness_table = pd.concat([self.wt_table, self.wo_table], axis=1)
        weakness_table.columns = np.append(self.thr, self.opp)
        full_table = pd.concat([strength_table, weakness_table])
        full_table.index = np.append(self.str, self.weak)
        return full_table.style\
                   .background_gradient(cmap="Purples", axis=None, low=0.5, high=1.0, subset=(self.str, self.thr))\
                   .background_gradient(cmap="Greens", axis=None, low=0.5, high=1.0, subset=(self.str, self.opp))\
                   .background_gradient(cmap="Oranges", axis=None, low=0.5, high=1.0, subset=(self.weak, self.thr))\
                   .background_gradient(axis=None, low=0.5, high=1.0, subset=(self.weak, self.opp))\
                   .set_precision(1)

    def sort_threats(self):
        sum_ts = self.st_table.sum(axis=0)
        sum_tw = self.wt_table.sum(axis=0)
        thr_values = sum_ts - sum_tw
        thr_values.index = self.thr
        thr_values.name = "D"
        return thr_values.sort_values()

    def sort_opportunities(self):
        sum_os = self.so_table.sum(axis=0)
        sum_ow = self.wo_table.sum(axis=0)
        opp_values = sum_os - sum_ow
        opp_values.index = self.opp
        opp_values.name = "H"
        return opp_values.sort_values(ascending=False)

    def sort_strengths(self):
        sum_so = self.so_table.sum(axis=1)
        sum_st = self.st_table.sum(axis=1)
        str_values = sum_so+sum_st
        str_values.index = self.str
        str_values.name = "F"
        return str_values.sort_values(ascending=False)

    def sort_weaknesses(self):
        sum_wo = self.wo_table.sum(axis=1)
        sum_wt = self.wt_table.sum(axis=1)
        weak_values = sum_wo+sum_wt
        weak_values.index = self.weak
        weak_values.name = "W"
        return weak_values.sort_values(ascending=False)






