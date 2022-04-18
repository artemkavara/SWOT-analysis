import numpy as np
import pandas as pd
from base_topsis_vikor import BaseTopsisVikor


class Vikor(BaseTopsisVikor):

    def find_f_max_min(self):
        vikor_table = self.dec_matr.copy()
        vikor_table["f_max"] = vikor_table[["SO", "WO", "ST", "WT"]].max(axis=1)
        vikor_table["f_min"] = vikor_table[["SO", "WO", "ST", "WT"]].min(axis=1)
        return vikor_table

    def eval_s_r(self):
        vikor_table = self.find_f_max_min()
        eval_s = pd.Series([
            np.sum((vikor_table["f_max"] - vikor_table[col])*self.eval_criteria["w_i"].to_numpy()/(vikor_table["f_max"] - vikor_table["f_min"]))
            for col in ["SO", "WO", "ST", "WT"]])
        eval_r = pd.Series([
            np.max((vikor_table["f_max"] - vikor_table[col])*self.eval_criteria["w_i"].to_numpy()/(vikor_table["f_max"] - vikor_table["f_min"]))
            for col in ["SO", "WO", "ST", "WT"]])
        eval_s_r_df = pd.concat([eval_s, eval_r], axis=1).T
        eval_s_r_df = pd.concat([pd.Series(["S_j", "R_j"]), eval_s_r_df, pd.Series([eval_s.max(), eval_r.max()]),
                                 pd.Series([eval_s.min(), eval_r.min()])], axis=1)
        eval_s_r_df.index = ["Max Group Benefit", "Level of Individual Expenditures"]
        eval_s_r_df.columns = vikor_table.columns.values

        return pd.concat([vikor_table, eval_s_r_df]), eval_s_r_df

    def eval_q(self, v: int = 0.5):
        """
        Takes a dataframe from the eval_s_r method that consists of 7 columns and 2 rows.
            * Columns: 'feature', 'SO', 'WO', 'ST', 'WT', 'f_max', 'f_min'
            * Row Indexes: 'Max Group Benefit', 'Level of Individual Expenditures'
        :param v: relative coefficient of importance (default = 0.5)
        :return: an np.array with computed q for each strategy
        """
        _, eval_s_r_df = self.eval_s_r()

        def q(s, r, s_max, s_min, r_max, r_min):
            if s_max == s_min:
                return (r-r_max)/(r_min-r_max)
            elif r_max == r_min:
                return (s-s_max)/(s_min-s_max)
            else:
                return v*((s-s_max)/(s_min-s_max)) + (1-v)*((r-r_max)/(r_min-r_max))

        q_arr = np.array([q(eval_s_r_df.iloc[0, col], eval_s_r_df.iloc[1, col], eval_s_r_df.iloc[0, 5],
                            eval_s_r_df.iloc[0, 6], eval_s_r_df.iloc[1, 5], eval_s_r_df.iloc[1, 6])
                          for col in range(1, 5)])
        q_df = pd.Series(q_arr, index=["SO", "WO", "ST", "WT"], name="Q").to_frame().T

        return q_df

    def range(self, dq=1/3):
        q_df = self.eval_q().sort_values(by=["Q"], axis=1, ascending=False)
        _, eval_s_r_df = self.eval_s_r()
        eval_s_r_df.reset_index(drop=True, inplace=True)
        sorted_s = eval_s_r_df[["SO", "WO", "ST", "WT"]].sort_values(by=[0], axis=1, ascending=False)
        sorted_r = eval_s_r_df[["SO", "WO", "ST", "WT"]].sort_values(by=[1], axis=1, ascending=False)
        final_table = pd.concat([
            pd.Series(sorted_s.columns, name="S"),
            pd.Series(sorted_r.columns, name="R"),
            pd.Series(q_df.columns, name="Q")
        ], axis=1).T

        best_string = q_df.columns[-1] if q_df.iloc[0, -2] - q_df.iloc[0, -1] >= dq \
            else sorted_s.columns[0] if sorted_s.columns[0] == sorted_r.columns[0] else "not available"
        return final_table, best_string







