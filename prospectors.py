import pros
import requests
import time
import configparser
import json

def inventory():
  def gpsConvert(xandy):
    x = xandy.split("/")[0]
    y = xandy.split("/")[1]
    x = int(x) | 0
    y = int(y) | 0
    if x < 0:
      x+=65536
    if y < 0:
      y+=65536
    loc = str(((x*65536)+y))
    return loc
  lands = configparser.ConfigParser()
  lands.read('lands.ini')
  lands = lands["LANDS"]
  rss_num = {'coal':4,
          'clay':5,
          'ore':6}
  all_rss = {'coal':0,
          'clay':0,
          'ore':0}
  for land in lands:
    coords = land
    rss = lands[land]
    loc = gpsConvert(coords)
    url = "https://wax.greymass.com/v1/chain/get_table_rows"
    data = '{"json":true,"code":"prospectorsn","scope":"prospectorsn","table":"loc","lower_bound":"'+loc+'","upper_bound":null,"index_position":1,"key_type":"","limit":"1",>
    storage = requests.get(url,data=data).json()['rows'][0]['storage']
    for s in storage:
      if s["type_id"] == rss_num[rss]:
        rss_amount = s["amount"]/1000
        rss_avail = round(rss_amount/3)
        all_rss[rss]+=rss_avail
  return all_rss

#############
def waxUSD():
    url = "https://api.crypto.com/v2/public/get-ticker?instrument_name=WAXP_USDT"
    response = requests.get(url).json()
    return response['result']['data']['l']

def alcor(token):
    url = "https://wax.alcor.exchange/api/markets"
    response = requests.get(url).json()
    for r in response:
        reply = r['quote_token']['symbol']['name']
        if reply == token:
            last_price = r['last_price']
    return last_price


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



