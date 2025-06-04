import streamlit as st

st.title("動物施打劑量與溶液配置計算機")

st.header("填入基本信息")
dose = st.number_input("給藥劑量 (mg/kg)", min_value=0.0, step=0.1)
weight = st.number_input("動物平均體重 (g)", min_value=0.0, step=0.1)
inj_vol = st.number_input("給藥體積 (ul)", min_value=0.0, step=0.1)
n_animal = st.number_input("動物數量 (隻)", min_value=1, step=1, format="%d")
stock_conc = st.number_input("母液濃度 (mg/ml)", min_value=0.0, step=0.1)

st.header("填入配方組成")
st.markdown(
    """
    <span style='color:red'>
    DMSO ≤ 5%；EtOH ≤ 5%；PEG400 ≤ 10–20%；Tween 80 ≤ 5%；HPCD（水合環糊精）≤ 10–20%
    </span>
    """, unsafe_allow_html=True
)

if '配方' not in st.session_state:
    st.session_state['配方'] = {
        'DMSO': 0.0,
        'EtOH': 0.0,
        'PEG400': 0.0,
        'Tween80': 0.0,
        'HPCD': 0.0,
        'ddH2O': 0.0
    }

dmsoper = st.number_input(
    "DMSO (%)", min_value=0.0, max_value=100.0, step=0.1, value=float(st.session_state['配方']['DMSO'])
)
etohper = st.number_input(
    "EtOH (%)", min_value=0.0, max_value=100.0, step=0.1, value=float(st.session_state['配方']['EtOH'])
)
pegper = st.number_input(
    "PEG400 (%)", min_value=0.0, max_value=100.0, step=0.1, value=float(st.session_state['配方']['PEG400'])
)
tweenper = st.number_input(
    "Tween 80 (%)", min_value=0.0, max_value=100.0, step=0.1, value=float(st.session_state['配方']['Tween80'])
)
hpcdper = st.number_input(
    "HPCD（水合環糊精）(%)", min_value=0.0, max_value=100.0, step=0.1, value=float(st.session_state['配方']['HPCD'])
)
# ddH2O 不讓使用者手動填寫，計算時自動補

# 更新 session_state
st.session_state['配方'] = {
    'DMSO': dmsoper,
    'EtOH': etohper,
    'PEG400': pegper,
    'Tween80': tweenper,
    'HPCD': hpcdper,
    'ddH2O': 0.0  # 這裡不讓使用者手動填，計算時自動補
}

if st.button("計算配方"):
    try:
        # 基本資訊計算
        if inj_vol == 0 or stock_conc == 0 or n_animal == 0:
            raise Exception
        work_conc = dose * (weight / 1000) / (inj_vol / 1000)
        total_vol = inj_vol * n_animal
        stock_vol = (work_conc * total_vol / 1000) / stock_conc * 1000  # ul

        # 母液百分比
        stock_per = stock_vol / total_vol * 100
        # 其他溶劑百分比總和
        user_sum = dmsoper + etohper + pegper + tweenper + hpcdper
        # ddH2O 百分比 = 100 - (母液百分比 + 其他溶劑百分比)
        ddh2oper = 100 - (stock_per + user_sum)
        if ddh2oper < 0:
            ddh2oper = 0

        # 各溶劑體積
        dmsovol = total_vol * dmsoper / 100
        etohvol = total_vol * etohper / 100
        pegvol = total_vol * pegper / 100
        tweenvol = total_vol * tweenper / 100
        hpcdvol = total_vol * hpcdper / 100
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