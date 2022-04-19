import re
import pandas as pd
import streamlit as st
from swot import Swot
from topsis import Topsis
from vikor import Vikor
from constants import Constants


st.set_page_config(layout="wide", page_title="SWOT Analysis")
st.title('SWOT Analysis')

swot_object = Swot()
topsis_object = Topsis()
vikor_object = Vikor()
constants = Constants()
color_dict = {"S": "rgba(39, 245, 196, 0.25)",
            "W": "rgba(245, 131, 39, 0.25)",
            "O": "rgba(221, 39, 245, 0.25)",
            "T": "rgba(245, 39, 110, 0.25)",
            "REST": "rgba(33, 37, 2, 0.25)"}
match_str = r'\w\d'

col_01, col_02 = st.columns(2)

with col_01:
    full_file = st.file_uploader("Choose a file with your data for SWOT analysis in .xlsx format",
                                 type=[".xls", ".xlsx"])

with col_02:
    st.write("### Advanced Techniques")
    topsis_bool = st.checkbox("TOPSIS")
    vikor_bool = st.checkbox("VIKOR")

if topsis_bool or vikor_bool:
    with col_01:
        adv_file = st.file_uploader("Choose a file with your data for TOPSIS/VIKOR analysis in .xlsx format",
                                    type=[".xls", ".xlsx"])
        if vikor_bool:
            dq = st.number_input("Enter minimum threshold for Q(A2)-Q(A1): ", value=1/3)

if full_file is not None:
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

    swot_object.assert_fields()
    swot_object.update_indices_and_columns()

    st.write("### Full table")
    st.table(swot_object.create_full_table())
    selected_piece_of_table = st.selectbox("Select to view a standalone table (ST, SO, WT, WO)",
                                             ["ST", "SO", "WT", "WO"])
    st.write(f"### {constants.__getattribute__(selected_piece_of_table)} Table")
    st.table(swot_object.view_selected_table(selected_piece_of_table))

    col_1, col_2 = st.columns(2)
    col_3, col_4 = st.columns(2)

    with col_1:
        st.write("### Threats sorted by power (ascending)",
                 swot_object.sort_threats().to_frame().style.background_gradient(gmap=swot_object.sort_threats()
                                                                                 .apply(lambda elem: -elem)))

    with col_2:
        st.write("### Opportunities sorted by power",
                 swot_object.sort_opportunities().to_frame().style.background_gradient(cmap="Purples"))

    with col_3:
        st.write("### Strengths sorted by power",
                 swot_object.sort_strengths().to_frame().style.background_gradient(cmap="Greens"))

    with col_4:
        st.write("### Weaknesses sorted by power",
                 swot_object.sort_weaknesses().to_frame().style.background_gradient(cmap="Oranges"))

if topsis_bool and adv_file is not None:

    topsis_elem = pd.read_excel(adv_file, sheet_name=0)
    topsis_object.str = topsis_elem["strengths"][topsis_elem["strengths"].notna()]
    topsis_object.weak = topsis_elem["weaknesses"][topsis_elem["weaknesses"].notna()]
    topsis_object.opp = topsis_elem["opportunities"][topsis_elem["opportunities"].notna()]
    topsis_object.thr = topsis_elem["threats"][topsis_elem["threats"].notna()]

    topsis_object.dec_matr = pd.read_excel(adv_file, sheet_name=1, decimal=',')
    topsis_object.eval_criteria = pd.read_excel(adv_file, sheet_name=2, decimal=',')
    topsis_object.assert_data()
    topsis_object.update_indices()

    st.write("## Input Data for TOPSIS Analysis")
    col_t_1, col_t_2 = st.columns([2, 1])
    with col_t_1:
        st.write("### Decision Matrix")
        st.table(topsis_object.dec_matr.style.applymap(
            lambda elem: f"background-color: {color_dict[elem[0]]}", subset=["feature"]
        ).set_precision(2))
    with col_t_2:
        st.write("### Evaluation Criteria")
        st.table(topsis_object.eval_criteria.style.applymap(
            lambda elem: f"background-color: {color_dict[elem[0]]}", subset=["alternative"]
        ).set_precision(2))

    st.write("## Results of TOPSIS Analysis")

    st.table(topsis_object.best_worst_sol().style.applymap(
            lambda elem: f"background-color: {color_dict[elem[0]]}", subset=["feature"]
        ).highlight_max(subset=["SO", "WO", "ST", "WT"], axis=1, props="background-color: rgba(0, 255, 0, 0.5)")\
        .highlight_min(subset=["SO", "WO", "ST", "WT"], axis=1, props="background-color: rgba(255, 0, 0, 0.5)"))

    eval_str_df = topsis_object.eval_of_strategies()
    st.table(eval_str_df.style.highlight_max(subset=("C_j",), axis=1, color="yellow"))
    st.write(f"#### Best strategy (TOPSIS) is {constants.__getattribute__(eval_str_df.columns[eval_str_df.iloc[2,:].argmax()])}")

if vikor_bool and adv_file is not None:
    vikor_elem = pd.read_excel(adv_file, sheet_name=0)
    vikor_object.str = vikor_elem["strengths"][vikor_elem["strengths"].notna()]
    vikor_object.weak = vikor_elem["weaknesses"][vikor_elem["weaknesses"].notna()]
    vikor_object.opp = vikor_elem["opportunities"][vikor_elem["opportunities"].notna()]
    vikor_object.thr = vikor_elem["threats"][vikor_elem["threats"].notna()]

    vikor_object.dec_matr = pd.read_excel(adv_file, sheet_name=1, decimal=',')
    vikor_object.eval_criteria = pd.read_excel(adv_file, sheet_name=2, decimal=',')
    vikor_object.assert_data()
    vikor_object.update_indices()

    st.write("## Input Data for VIKOR Analysis")
    col_v_1, col_v_2 = st.columns([2, 1])
    with col_v_1:
        st.write("### Decision Matrix")
        st.table(vikor_object.eval_s_r()[0].style.applymap(
            lambda elem: f"background-color: {color_dict[elem[0]] if re.match(match_str, elem) else color_dict['REST']}",
            subset=(["feature"])
        ).highlight_max(subset=(["Max Group Benefit"], ["SO", "WO", "WT", "ST"]), color="green", axis=1)
         .highlight_max(subset=(["Level of Individual Expenditures"], ["SO", "WO", "WT", "ST"]), color="green", axis=1)
         .highlight_min(subset=(["Max Group Benefit"], ["SO", "WO", "WT", "ST"]), color="red", axis=1)
         .highlight_min(subset=(["Level of Individual Expenditures"], ["SO", "WO", "WT", "ST"]), color="red", axis=1)
         .set_precision(5))

    st.table(vikor_object.eval_q().style.highlight_min(subset=("Q",), axis=1, color="yellow").set_precision(5))

    with col_v_2:
        st.write("### Evaluation Criteria")
        st.table(vikor_object.eval_criteria.style.applymap(
            lambda elem: f"background-color: {color_dict[elem[0]]}", subset=["alternative"]
        ).set_precision(2))

    st.write("## Sequence of alternatives based on S, R and Q")
    final_table, best_string = vikor_object.range(dq)
    st.table(final_table)
    st.write(f"#### Best strategy (VIKOR) is " +
             f"{constants.__getattribute__(best_string) if not best_string == 'not available' else best_string}")






