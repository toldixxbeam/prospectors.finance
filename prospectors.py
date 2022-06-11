import pros

inventory = pros.inventory()
st.set_page_config(
    page_title="Prospectors",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    )
coal = inventory["coal"]
clay = inventory["clay"]
ore  = inventory["ore"]
stock = f"{coal} kg coal \n{clay} kg clay \n{ore} kg ore"
st.sidebar.title("Resources Currently In Stock")
st.sidebar.text(stock)

hide_streamlit_style = """ <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;} </style> """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
