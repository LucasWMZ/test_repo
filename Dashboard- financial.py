"""
Objective: Create a financial stock market dashboard
Date: Sep 2022
"""


import streamlit as st 
import requests
import yfinance as yf
import pandas as pd
import numpy as np
import cufflinks as cf
import datetime
import yahoo_fin.stock_info as yahoo

st.set_page_config(page_title = "Financial Data Summary", page_icon=":chart_with_upwards_trend:", layout= 'wide')

st.sidebar.title(":chart_with_upwards_trend: *Financial Data*")
st.sidebar.markdown("<h3><u>Query Parameter<u><h3>", True)
ticker = st.sidebar.text_input('Enter Ticker', "AAPL").upper()
button = st.sidebar.button('Select')

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)

def pv(fv,requiredRateOfReturn,years):
    return fv / ((1 + requiredRateOfReturn / 100) ** years)

def fv(pv,growth,years):
    return pv * (1 + growth)  ** years    



if button:
    requestString = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile%2Cprice"
    r = requests.get(f"{requestString}", headers={"USER-AGENT": "Mozilla/5.0"})
    json = r.json()
    data = json["quoteSummary"]["result"][0]
    tickerData = yf.Ticker(ticker)
    logo = '<p style="text-align:center;"><img src=%s>' % tickerData.info['logo_url']
    st.markdown(logo, unsafe_allow_html=True)

    st.write('#')

    st.text("Company name:  {0}".format(tickerData.info['longName']))
    st.text("Sector:        {0}".format(data["assetProfile"]["sector"]))
    st.text("Market Cap:    {0}".format(data["price"]["marketCap"]["fmt"]))

    with st.expander("About Company"):
        st.write(data["assetProfile"]["longBusinessSummary"])

    # end_date = st.date_input("End date", datetime.datetime.now())
    # start_date = st.date_input("Start date", datetime.datetime(end_date.year - 1, end_date.month, end_date.day))
    end_date = datetime.datetime.now()
    start_date = datetime.datetime(end_date.year - 4, end_date.month, end_date.day)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    # st.write(tickerDf)

    ### CHART ####
    st.header('**Market Price**')
    qf=cf.QuantFig(tickerDf,title= "Ticker:{0}  Current Price: {1} ".format(ticker, tickerData.info['currentPrice']),legend='top',name='GS')
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)


    # st.write(tickerData.info)
    # st.write(df)

    #Ratio
    ratio, ratio1, ratio2, ratio3 = st.columns(4)
    ratio.markdown("<h3>Price/Value<h3>", True)
    ratio1.metric("Price/Earning: ", tickerData.info['trailingPE'])
    ratio2.metric("Price/Book: ", tickerData.info['priceToBook'])
    ratio3.metric("Earning per share: ", tickerData.info['trailingEps'])

    moat, moat1, moat2, moat3 = st.columns(4)
    moat.markdown("<h3>Moat<h3>", True)
    moat1.metric("ROE: ", tickerData.info['returnOnEquity'])
    moat2.metric("ROA: ", tickerData.info['returnOnAssets'])
    moat3.metric(" ", " ")

    risk, risk1, risk2, risk3 = st.columns(4)
    risk.markdown("<h3>Risk<h3>", True)
    risk1.metric("Debt to Equity: ", tickerData.info['debtToEquity'])
    risk2.metric("Quick Ratio: ", tickerData.info['quickRatio'])
    risk3.metric("Current Ratio: ", tickerData.info['currentRatio'])

    div, div1, div2, div3 = st.columns(4)
    div.markdown("<h3>Dividend<h3>", True)
    div1.metric("Dividend Yield: ", tickerData.info['dividendYield'])
    div2.metric("Payout Ratio: ", tickerData.info['payoutRatio'])
    div3.metric(" ", " ")

    st.write('#')

    ###INCOME STATEMENT###
    st.markdown("<h3><u>Income Statement Summary<u><h3>", True)
    income_statment = yahoo.get_income_statement(ticker)
    income_years = income_statment.columns
    
    # df = pd.DataFrame({income_statment[income_years[4]]["endDate"]: [income_statment[income_years[4]]["totalRevenue"], income_statment[income_years[4]]["grossProfit"]]})
    df = pd.DataFrame({income_years[3]: [income_statment[income_years[3]]["totalRevenue"],income_statment[income_years[3]]["costOfRevenue"],income_statment[income_years[3]]["grossProfit"],income_statment[income_years[3]]["ebit"],income_statment[income_years[3]]["netIncome"]],
                        income_years[2]: [income_statment[income_years[2]]["totalRevenue"],income_statment[income_years[2]]["costOfRevenue"],income_statment[income_years[2]]["grossProfit"],income_statment[income_years[2]]["ebit"],income_statment[income_years[2]]["netIncome"]],
                        income_years[1]: [income_statment[income_years[1]]["totalRevenue"],income_statment[income_years[1]]["costOfRevenue"],income_statment[income_years[1]]["grossProfit"],income_statment[income_years[1]]["ebit"],income_statment[income_years[1]]["netIncome"]],
                        income_years[0]: [income_statment[income_years[0]]["totalRevenue"],income_statment[income_years[0]]["costOfRevenue"],income_statment[income_years[0]]["grossProfit"],income_statment[income_years[0]]["ebit"],income_statment[income_years[0]]["netIncome"]]},
                        index = ['Total Revenue', 'Cost of Revenue', 'Gross Profit', 'EBIT', 'Net Income'])

    st.write(df.to_html(), unsafe_allow_html=True)


    st.write('#')
    ###BALANCE SHEET###
    st.markdown("<h3><u>Balance Sheet Summary<u><h3>", True)
    balance_sheet = yahoo.get_balance_sheet(ticker)
    balance_years = balance_sheet.columns

    # bal3 = balance_sheet[balance_years[3]]["totalLiab"] - balance_sheet[balance_years[3]]["totalCurrentLiabilities"]
    # bal2 = balance_sheet[balance_years[2]]["totalLiab"] - balance_sheet[balance_years[2]]["totalCurrentLiabilities"]
    # bal1 = balance_sheet[balance_years[1]]["totalLiab"] - balance_sheet[balance_years[1]]["totalCurrentLiabilities"]
    # bal0 = balance_sheet[balance_years[0]]["totalLiab"] - balance_sheet[balance_years[0]]["totalCurrentLiabilities"]

    
    df2 = pd.DataFrame({balance_years[3]: [(balance_sheet[balance_years[3]]["totalAssets"] - balance_sheet[balance_years[3]]["totalCurrentAssets"]),balance_sheet[balance_years[3]]["totalCurrentAssets"],balance_sheet[balance_years[3]]["totalAssets"],(balance_sheet[balance_years[3]]["totalLiab"] - balance_sheet[balance_years[3]]["totalCurrentLiabilities"]),balance_sheet[balance_years[3]]["totalCurrentLiabilities"],balance_sheet[balance_years[3]]["totalLiab"]],
                        balance_years[2]: [(balance_sheet[balance_years[2]]["totalAssets"] - balance_sheet[balance_years[2]]["totalCurrentAssets"]),balance_sheet[balance_years[2]]["totalCurrentAssets"],balance_sheet[balance_years[2]]["totalAssets"],(balance_sheet[balance_years[2]]["totalLiab"] - balance_sheet[balance_years[3]]["totalCurrentLiabilities"]),balance_sheet[balance_years[2]]["totalCurrentLiabilities"],balance_sheet[balance_years[2]]["totalLiab"]],
                        balance_years[1]: [(balance_sheet[balance_years[1]]["totalAssets"] - balance_sheet[balance_years[1]]["totalCurrentAssets"]),balance_sheet[balance_years[1]]["totalCurrentAssets"],balance_sheet[balance_years[1]]["totalAssets"],(balance_sheet[balance_years[1]]["totalLiab"] - balance_sheet[balance_years[3]]["totalCurrentLiabilities"]),balance_sheet[balance_years[1]]["totalCurrentLiabilities"],balance_sheet[balance_years[1]]["totalLiab"]],
                        balance_years[0]: [(balance_sheet[balance_years[0]]["totalAssets"] - balance_sheet[balance_years[0]]["totalCurrentAssets"]),balance_sheet[balance_years[0]]["totalCurrentAssets"],balance_sheet[balance_years[0]]["totalAssets"],(balance_sheet[balance_years[0]]["totalLiab"] - balance_sheet[balance_years[3]]["totalCurrentLiabilities"]),balance_sheet[balance_years[0]]["totalCurrentLiabilities"],balance_sheet[balance_years[0]]["totalLiab"]]},
                        index = ['Non-Current Asset', 'Current Asset','Total Asset','Non-Current Liability','Current Liabilities', 'Total Liabilities'])
    
    
    
    st.write(df2.to_html(), unsafe_allow_html=True)


    link2  = f"""https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?"""
    modules2 = f"""modules=assetProfile%2Cprice%2CfinancialData%2CearningsTrend%2CdefaultKeyStatistics"""
    requestString2 = link2 + modules2

    request2 = requests.get(f"{requestString2}", headers={"USER-AGENT": "Mozilla/5.0"})
    json2 = request2.json()
    data2 = json2["quoteSummary"]["result"][0]

    st.session_state.data2 = data2

if 'data2' in st.session_state:


    data2 = st.session_state.data2

   
    st.markdown("", unsafe_allow_html=True)
    st.markdown("", unsafe_allow_html=True)  

    
    st.header("Valuation")
    currentPrice = data2["financialData"]["currentPrice"]["raw"]
    growth = data2["earningsTrend"]["trend"][ 4 ][ "growth" ][ "raw" ] * 100
    peFWD = data2["defaultKeyStatistics"]["forwardPE"]["raw"]
    epsFWD = data2["defaultKeyStatistics"]["forwardEps"]["raw"]
    requiredRateOfReturn = 10.0
    yearsToProject = 5

    growth = st.number_input("Growth", value=growth, step = 1.0)
    peFWD = st.number_input("P/E", value=peFWD, step = 1.0)
    requiredRateOfReturn = st.number_input("Required Rate Of Return", value=requiredRateOfReturn, step = 1.0)

    
    futureEPS = fv(epsFWD,growth/100,yearsToProject)
    futurePrice = futureEPS * peFWD 
    stickerPrice = pv(futurePrice, requiredRateOfReturn, yearsToProject)
    upside = (stickerPrice - currentPrice)/stickerPrice * 100

    
    st.metric("EPS", "{:.2f}".format(futureEPS))
    st.metric("Future Price", "{:.2f}".format(futurePrice))
    st.metric("Sticker Price", "{:.2f}".format(stickerPrice))
    st.metric("Current Price", "{:.2f}".format(currentPrice))
    st.metric("Upside", "{:.2f}".format(upside))