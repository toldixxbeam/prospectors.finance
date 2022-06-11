import requests
import pandas as pd
import streamlit as st

#ore = requests.get("https://grandland.prospectors.io/ore.2125dae7.png")
#st.set_page_config(
st.set_page_icon=("https://grandland.prospectors.io/ore.2125dae7.png")
st.set_page_config(layout='wide')
st.title("Atomic Hub Land Listings")
listing_select = st.radio('Select one:', ['Currently Listed', 'Sales History'])
list_dict = {'Currently Listed': 1, 'Sales History': 3}
listing_status = list_dict[listing_select]

url = 'https://wax.api.atomicassets.io/atomicmarket/v1/sales?state='+str(listing_status)+'&collection_name=prospectorsa&schema_name=grandland&page=1&limit=100&order=desc&sort=updated'

response = requests.get(url).json()['data']
price = []
gps = []
resources = gold,wood,stone,coal,clay,ore,building = [],[],[],[],[],[],[]
for listing in response:
    p = round(int(listing['price']['amount'])/100000000)
    rss = listing['assets'][0]['mutable_data']
    try: loc = str(listing['assets'][0]['immutable_data']['x'])+'/'+str(listing['assets'][0]['immutable_data']['y'])
    except: loc = 'N/A'
    #print(price,'wax ',loc,rss)
    ### Find Ore
    price.append(p)
    gps.append(loc) 
    try:
        gold.append(rss['gold'])
    except:
        gold.append('0')
    try:
        wood.append(rss['wood'])
    except:
        wood.append('0')
    try:
        stone.append(rss['stone'])
    except:
        stone.append('0')
    try:
        coal.append(rss['coal'])
    except:
        coal.append('0')
    try:
        clay.append(rss['clay'])
    except:
        clay.append('0')
    try:
        ore.append(rss['ore'])
    except:
        ore.append('0')
    try:
        building.append(rss['building'])
    except:
        building.append('No Building')

dict_df = {'Price':price,'Location':gps,'Gold':gold,'Wood':wood,'Stone':stone,'Coal':coal,'Clay':clay,'Ore':ore,'Building':building}

pros_df = pd.DataFrame.from_dict(dict_df)
#print(pros_df)



st.write(pros_df)




hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
