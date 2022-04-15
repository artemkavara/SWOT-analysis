import pandas as pd
import numpy as np


class BaseTopsisVikor(object):

    def __init__(self):
        self.dec_matr: pd.DataFrame = None
        self.eval_criteria: pd.DataFrame = None
        self.str: pd.DataFrame = None
        self.weak: pd.DataFrame = None
        self.opp: pd.DataFrame = None
        self.thr: pd.DataFrame = None
        self.index: np.array = None

    def assert_data(self):
        assert self.dec_matr.shape[0] == self.eval_criteria.shape[0], "Check number of weights!"
        assert self.dec_matr.shape[0] == self.str.shape[0]+self.weak.shape[0]+self.opp.shape[0]+self.thr.shape[0], \
            "Incorrect column names!"
        assert round(self.eval_criteria["w_i"].sum(),2) == 1, "Incorrect sum of weights!"

    def update_indices(self):
        self.dec_matr.columns.values[0] = "feature"
        self.index = np.append(self.str, [self.weak, self.opp, self.thr])
        self.dec_matr.index = self.index
