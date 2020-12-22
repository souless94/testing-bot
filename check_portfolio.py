#Install the libaries
import pandas as pd
import datetime as dt
import yfinance as yf
from business.calendar import Calendar

calendar = Calendar(
  working_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
  # array items are either parseable date strings, or real datetime.date objects
  holidays=[],
  extra_working_dates=[],
)

# get stocks
# # Equity
# NIKKO Straits Times Index ETF
# NIKKO StraitsTrading Asia ex Japan REIT ETF
# Xtrackers MSCI China ETF
# iShares MSCI India Index

# # Fixed Income
# ABF Singapore Bond Index ETF
# NIKKO SGD Investment Grade Corporate Bond ETF
def validate(date_text):
    try:
        print("date_text : ",date_text)
        the_date = dt.datetime.strptime(date_text, '%Y-%m-%d')
        print("is business day ? : ",calendar.is_business_day(date_text))
        end = dt.datetime.today()
        print("is today a business day ? ",calendar.is_business_day(end))
        return calendar.is_business_day(the_date) and calendar.is_business_day(end)
    except ValueError as e:
        print(e)
        return False


def portfolio_check(date_invested):
    
    if (validate(date_invested)== False):
        end = dt.datetime.today()
        if calendar.is_business_day(end) == False:
            return "Today is a not a business day"
        else:
            return "Wrong input, please enter the date you invested : (YYYY-MM-DD)"
    else:
        equities = ["G3B.SI","CFA.SI","LG9.SI","INDA"]
        fixed_income = ["A35.SI","MBH.SI"]
        stocks = equities + fixed_income
        print("equities: ",equities)
        print("fixed: ",fixed_income)
        print("stocks:" , stocks)
        # get five years of data
        start = dt.datetime.today()-dt.timedelta(days=365*5)
        end = dt.datetime.today()
        cl_prices = pd.DataFrame()
        # looping over tickers and creating a dataframe with close prices
        for ticker in stocks:
            cl_prices[ticker] = yf.download(ticker,start,end)["Close"]
        
        print("============= data downloaded ==================")
        df = cl_prices.copy()
        df.fillna(method='ffill',inplace=True)
        df.sort_index(ascending=False,inplace=True)
        print(df.head(30))
        amount = 3000 # 5% is cash
        cash = 0.05*3000
        equity_percent = 0.52/len(equities)
        fixed_percent = 0.43/len(fixed_income)
        details ={}
        invested_date = dt.datetime.strptime(date_invested,'%Y-%m-%d')
        days_difference = end - invested_date
        days_difference = days_difference.days
        
        print("============== settings set =====================")
        if ( df.loc[date_invested].empty):
            return "there is no data for the requested invested date : " + date_invested

        for equity in equities:
            price = round(df[equity].loc[date_invested][0],2)
            units = round(equity_percent*amount/df[equity].loc[date_invested][0],2)
            details[equity] = {"units":units,"price":price}
        for fixed in fixed_income:
            price = round(df[fixed].loc[date_invested][0],2)
            units = round(fixed_percent*amount/df[fixed].loc[date_invested][0],2)
            details[fixed] = {"units":units,"price":price}
        ans = 0
        for items in stocks:
            ans += details[items]['units']*details[items]['price']

        offset = ans - amount

        details['returns']=0
        details['current value']=cash - offset
        print("===================== details ======================")
        print(details)

        today = str(dt.datetime.today().strftime("%Y-%m-%d"))
        if ( df.loc[date_invested].empty):
            return "there is no data for today : " + date_invested

        for the_stock in stocks:
            print("=============",the_stock,"==============")
            the_price = round(df[the_stock].loc[today][0],2)
            old_price = details[the_stock].loc['price'][0]
            current_stock_returns = (the_price-old_price)*details.loc[the_stock]['units'][0]
            details['current value'] += the_price* details[the_stock]['units'][0]
            details['returns']+=current_stock_returns
            print(current_stock_returns)

        # summary = {'date_invested':date_invested,'days_difference':days_difference,'cash':cash,
        # 'returns':details['returns'],'current_value':details['current value']}
        summary = "=================== SUMMARY ===================="+"\n" \
                + "date invested : " + str(date_invested) +"\n" \
                + "days invested : "+ str(days_difference) +"\n" \
                + "cash" + str(cash) +"\n" \
                + "returns : " + str(details['returns']) + "\n" \
                + "current value : " + details['current value'] +"\n" \
                + "========================================="

        return summary
    # print("=================== SUMMARY ====================")
    # print("date invested: ", date_invested)
    # print('days invested: ',days_difference)
    # print("cash: ",cash)
    # print("returns: ",details['returns'])
    # print("current value",details['current value'])
    # print("=========================================")