
import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

import altair as alt
import pandas as pd
import streamlit as st
import plotly
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components
import pros

inventory = pros.inventory()
coal = inventory["coal"]
clay = inventory["clay"]
ore  = inventory["ore"]
stock = f"{coal} kg coal \n{clay} kg clay \n{ore} kg ore"
st.sidebar.title("Resources Currently In Stock")
st.sidebar.text(stock)


def itemList():
    url = 'http://prospectors.online/grand/trades/deals-stats.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ##scrape RSS
    all_items = soup.find_all('tr')[1:]
    item_list = list()
    for find in all_items:
        item_name = find.find('td')
        try: item_list.append(item_name.text)
        except: pass
    return item_list[:-1]

def itemPrice(item):

    url = 'http://prospectors.online/grand/trades/deals-stats.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ##scrape RSS
    all_items = soup.find_all('tr')[1:]
    for i,find in enumerate(all_items):
        item_name = find.find('td')
        try:
            if item_name.text == item:
                r = all_items[i].find_all('td')[3:25]

                itemList = list()
                for habit in r:
                    price = habit.find_all('span')[-1].text
                    itemList.append(price)
        except: pass

    return itemList[0]


def chartItem(item):
    url = 'http://prospectors.online/grand/trades/deals-stats.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ##scrape RSS
    all_items = soup.find_all('tr')[1:]
    for i,find in enumerate(all_items):
        item_name = find.find('td')
        #print(item_name.text)
        try:
            if item_name.text == item:
                #tr = i
                #print(item)

                r = all_items[i].find_all('td')[3:25]

                ##Create List for Dates
                dates = list()
                r_date = soup.find_all('tr')[0].find_all('th')[3:25]
                for habit in r_date:
                    dates.append(habit.text)

                ##Ceate list for item
                item_list = list()
                for habit in r:
                    price = habit.find_all('span')[-1].text
                    item_list.append(price)
                break
        except: pass

    return dates[::-1],item_list[::-1]


#st.sidebar.write("Select Resources and Tools")

itemList = itemList()
rssList = itemList[:5]
tool_list = itemList[25:33]
repairtool_list = itemList[39:41]
all_tools = tool_list+repairtool_list

default_rss = ['coal','clay','ore']


rss_choices = []

#tool_choices = st.sidebar.multiselect("Choose Tools",all_tools)#,default=tool_list)

col1, col2 = st.columns(2)

##Create charts for RSS
rss_data = list()
for choice in default_rss:

    items_to_graph = chartItem(choice)
    y_items = items_to_graph[1]
    x_dates = items_to_graph[0]


    item_dict = {'Date':x_dates,'Price':y_items}
    item_df = pd.DataFrame(item_dict)

    line_chart = go.Scatter(x=item_dict['Date'],y=item_dict['Price'],name=choice)
    rss_data.append(line_chart)

##Create charts for Tools
#tool_data = list()
#for choice in all_tools:

#    items_to_graph = chartItem(choice)
#    y_items = items_to_graph[1]
#    x_dates = items_to_graph[0]


#    item_dict = {'Date':x_dates,'Price':y_items}
#    item_df = pd.DataFrame(item_dict)

#    line_chart = go.Scatter(x=item_dict['Date'],y=item_dict['Price'],name=choice)
#    tool_data.append(line_chart)




rss_fig = go.Figure(data=rss_data)
rss_fig.update_layout(title="<b>Resources</b>")
#tool_fig = go.Figure(data=tool_data)
#tool_fig.update_layout(title="<b>Tools</b>")
#fig = px.line(item_df, x = "Date", y = "Price", title = choices)

    #col2.plotly_chart(fig)

col1.plotly_chart(rss_fig)
#col1.plotly_chart(tool_fig)

c = col2#.container()

with c:
       with st.form(key="rss"):

            buy_item = st.radio('Select item',['coal','clay','ore'])
            buy_amount = st.number_input('Amount')

            item_cost = itemPrice(buy_item)
            buy_total = round(float(item_cost)*float(buy_amount),2)/1000*0.9

            #invoice = st.form_submit_button("Estimate")
            if st.form_submit_button("Estimate"):
                st.write(f"Your total for {buy_amount} {buy_item} is: {buy_total} PGL \n \nThis is taking into consideration a 10% discount with current market rate. \n \nFree Shipping and Handling!")

            #if buy_amount > 0:
            with c.form(key="invoice"):
                customer_wax = st.text_input("Wax Account to Receive in Game")
                customer_loc = st.text_input("Location to Receive")
                customer_tg = st.text_input("Telegram For Invoice")
                buy = st.form_submit_button("Generate Invoice")
                if buy:
                    if buy_item and buy_amount > 0 and customer_wax and customer_loc and customer_tg:
                        url = 'https://docs.google.com/forms/d/e/1FAIpQLScQu5ewcim8magdlXWGlidN1aLJRRJipWxxQddWxMa8dI0BLQ/viewform?usp=pp_url&entry.2056394064='+str(buy_item)+'&entry.1426332526='+str(buy_amount)+'&entry.948927672='+str(customer_wax)+'&entry.1197930162='+str(customer_loc)+'&entry.1634629381='+str(customer_tg)+'&entry.1556280284='+str(buy_total)

                        st.write(f"Click the link to complete purchace [BUY NOW]({url})")
                    else:
                        st.write("Please Generate Invoice and Fill out all fields")


hide_streamlit_style = """ <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;} </style> """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
