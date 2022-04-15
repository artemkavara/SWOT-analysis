import pandas as pd
from swot import Swot
from IPython.display import display

swot_object = Swot()

full_file = r"C:\Users\Artem_Kavara\Desktop\Lab_5\data\SWOT.xlsx"

swot_elem = pd.read_excel(full_file, sheet_name=0)
swot_object.str = swot_elem["strengths"][swot_elem["strengths"].notna()]
swot_object.weak = swot_elem["weaknesses"][swot_elem["weaknesses"].notna()]
swot_object.opp = swot_elem["opportunities"][swot_elem["opportunities"].notna()]
swot_object.thr = swot_elem["threats"][swot_elem["threats"].notna()]

swot_object.st_table = pd.read_excel(full_file, sheet_name=1,
                                     header=None, decimal=',')
swot_object.so_table = pd.read_excel(full_file, sheet_name=2,
                                     header=None, decimal=',')
swot_object.wt_table = pd.read_excel(full_file, sheet_name=3,
                                     header=None, decimal=',')
swot_object.wo_table = pd.read_excel(full_file, sheet_name=4,
                                     header=None, decimal=',')

display(swot_object.sort_weaknesses())