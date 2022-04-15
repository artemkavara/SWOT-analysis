import numpy as np
import pandas as pd
from base_topsis_vikor import BaseTopsisVikor


class Topsis(BaseTopsisVikor):

    def norm_dec_matr(self):
        norm_dec_matr = self.dec_matr[["SO", "WO", "ST", "WT"]].to_numpy(copy=True)
        norm = np.linalg.norm(norm_dec_matr)
        res = self.dec_matr.copy()
        res = pd.concat([res["feature"], res[["SO", "WO", "ST", "WT"]].applymap(lambda elem: elem/norm)], axis=1)
        return res

    def weighted_norm_dec_matr(self):
        norm_dec_matr_df = self.norm_dec_matr()
        res = pd.concat([norm_dec_matr_df["feature"],
                         pd.Series(norm_dec_matr_df["SO"].to_numpy() * self.eval_criteria["w_i"].to_numpy(), name="SO", index=self.index),
                         pd.Series(norm_dec_matr_df["WO"].to_numpy() * self.eval_criteria["w_i"].to_numpy(), name="WO", index=self.index),
                         pd.Series(norm_dec_matr_df["ST"].to_numpy() * self.eval_criteria["w_i"].to_numpy(), name="ST", index=self.index),
                         pd.Series(norm_dec_matr_df["WT"].to_numpy() * self.eval_criteria["w_i"].to_numpy(), name="WT", index=self.index)], axis=1)
        return res

    def best_worst_sol(self):
        weighted_norm_dec_matr_df = self.weighted_norm_dec_matr()
        weighted_norm_dec_matr_df["A+"] = weighted_norm_dec_matr_df[["SO", "WO", "ST", "WT"]].max(axis=1)
        weighted_norm_dec_matr_df["A-"] = weighted_norm_dec_matr_df[["SO", "WO", "ST", "WT"]].min(axis=1)
        return weighted_norm_dec_matr_df

    def eval_of_strategies(self):
        best_worst_sol_df = self.best_worst_sol()
        eval_d_plus = np.array([np.linalg.norm(best_worst_sol_df[col] - best_worst_sol_df["A+"])
                                for col in ["SO", "WO", "ST", "WT"]])
        eval_d_minus = np.array([np.linalg.norm(best_worst_sol_df[col] - best_worst_sol_df["A-"])
                                for col in ["SO", "WO", "ST", "WT"]])
        eval_cc = eval_d_minus/(eval_d_plus+eval_d_minus)
        eval_df = pd.concat([pd.Series(eval_d_plus), pd.Series(eval_d_minus), pd.Series(eval_cc)], axis=1).T
        eval_df.index = ["D_j+", "D_j-", "C_j"]
        eval_df.columns = ["SO", "WO", "ST", "WT"]
        return eval_df






