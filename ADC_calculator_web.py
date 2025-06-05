import streamlit as st

st.title("動物施打劑量與溶液配置計算機")

st.header("填入基本信息")
dose = st.text_input("給藥劑量 (mg/kg)")
weight = st.text_input("動物平均體重 (g)")
inj_vol = st.text_input("給藥體積 (ul)")
n_animal = st.text_input("動物數量 (隻)")
stock_conc = st.text_input("母液濃度 (mg/ml)")

st.header("填入配方組成")
st.markdown(
    """
    <span style='color:red'>
    DMSO ≤ 5%；EtOH ≤ 5%；PEG400 ≤ 10–20%；Tween 80 ≤ 5%；HPCD（水合環糊精）≤ 10–20%
    ("請先確認藥物是否有相關文獻或是說明，確認其溶劑的安全性與使用比例。")
    </span>
    """, unsafe_allow_html=True
)

if '配方' not in st.session_state:
    st.session_state['配方'] = {
        'DMSO': "",
        'EtOH': "",
        'PEG400': "",
        'Tween80': "",
        'HPCD': "",
        'ddH2O': 0.0
    }

dmsoper = st.text_input("DMSO (%)", value=st.session_state['配方']['DMSO'], key="dmsoper")
etohper = st.text_input("EtOH (%)", value=st.session_state['配方']['EtOH'], key="etohper")
pegper = st.text_input("PEG400 (%)", value=st.session_state['配方']['PEG400'], key="pegper")
tweenper = st.text_input("Tween 80 (%)", value=st.session_state['配方']['Tween80'], key="tweenper")
hpcdper = st.text_input("HPCD（水合環糊精）(%)", value=st.session_state['配方']['HPCD'], key="hpcdper")

# 更新 session_state
st.session_state['配方'] = {
    'DMSO': dmsoper,
    'EtOH': etohper,
    'PEG400': pegper,
    'Tween80': tweenper,
    'HPCD': hpcdper,
    'ddH2O': 0.0
}

if st.button("計算配方"):
    try:
        # 轉型，沒填寫自動為0
        dose_f = float(dose or 0)
        weight_f = float(weight or 0)
        inj_vol_f = float(inj_vol or 0)
        n_animal_f = float(n_animal or 0)
        stock_conc_f = float(stock_conc or 0)
        dmsoper_f = float(dmsoper or 0)
        etohper_f = float(etohper or 0)
        pegper_f = float(pegper or 0)
        tweenper_f = float(tweenper or 0)
        hpcdper_f = float(hpcdper or 0)

        if inj_vol_f == 0 or stock_conc_f == 0 or n_animal_f == 0:
            raise Exception
        work_conc = dose_f * (weight_f / 1000) / (inj_vol_f / 1000)
        total_vol = inj_vol_f * n_animal_f
        stock_vol = (work_conc * total_vol / 1000) / stock_conc_f * 1000  # ul

        stock_per = stock_vol / total_vol * 100
        user_sum = dmsoper_f + etohper_f + pegper_f + tweenper_f + hpcdper_f
        ddh2oper = 100 - (stock_per + user_sum)
        if ddh2oper < 0:
            ddh2oper = 0

        # 各溶劑體積
        dmsovol = total_vol * dmsoper_f / 100
        etohvol = total_vol * etohper_f / 100
        pegvol = total_vol * pegper_f / 100
        tweenvol = total_vol * tweenper_f / 100
        hpcdvol = total_vol * hpcdper_f / 100
        ddh2ovol = total_vol * ddh2oper / 100

        st.info(
            f"工作濃度: {work_conc:.2f} mg/ml\n"
            f"總體積: {total_vol:.0f} ul\n"
            f"母液體積: {stock_vol:.0f} ul"
        )
        st.info(
            f"ddH2O 百分比自動補齊：{ddh2oper:.2f}%"
        )
        st.success(
            f"動物體內施打配方配置方法：\n"
            f"取 {stock_vol:.0f} ul 母液，\n"
            f"加入 {dmsovol:.0f} ul DMSO + {etohvol:.0f} ul EtOH + "
            f"{pegvol:.0f} ul PEG400 + {tweenvol:.0f} ul Tween 80 + "
            f"{hpcdvol:.0f} ul HPCD（水合環糊精） + {ddh2ovol:.0f} ul ddH2O\n"
            f"補足至總體積 {total_vol:.0f} ul，即可達到工作濃度"
        )
    except Exception:
        st.error("請確認所有欄位皆已填寫且不可為零。")
