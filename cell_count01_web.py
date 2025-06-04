import os
import streamlit as st

st.title("細胞計數計算機")

total_cells = st.number_input("4格內細胞總數", min_value=0.0, step=1.0)
desired_cells = st.number_input("需要的細胞數量 (個數)", min_value=0.0, step=1.0)
dilution_factor = st.number_input("原液稀釋倍數", min_value=1.0, step=1.0)

if st.button("計算"):
    try:
        num_squares = 4
        concentration = (total_cells / num_squares) * dilution_factor * 1e4 / 1000  # (個數/μl)
        volume_needed = desired_cells / concentration

        process_text = (
            f"濃度 = ({total_cells} / {num_squares}) × {dilution_factor} × 10⁴ ÷ 1000\n"
            f"濃度 = {concentration:.2f} 個數/μl\n"
            f"所需體積 = {desired_cells} ÷ {concentration:.2f}\n"
            f"所需體積 = {volume_needed:.2f} μl"
        )
        st.success(process_text)
        st.info(f"請取用體積: {volume_needed:.2f} μl")
    except Exception:
        st.error("請確認所有欄位皆為數字。")