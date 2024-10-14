from tradingview_screener import Query, Column
import pandas as pd

# for all classes to return, as __str__() determines what value comes out of every function:


# user input:
uInput = input("Enter a stock name (e.g. NVDA): ")
uInput = uInput.upper()
# upper() so that it does not matter if input is lower/upper case, it will always be upper

exact_name_query = (Query()
                    .select('name')
                    .where(Column('name') == uInput)
                    .get_scanner_data())
# exact_name_query is a query for matched exact name, it returns e.g.

# (1,          ticker    name
# 0         NASDAQ:NVDA  NVDA


class NameLike:
    def __init__(self):
        count, self.query = (Query()
                             .select('name')
                             .where(Column('name').like(uInput))
                             .get_scanner_data())
        # self.query would return this as a dataframe at this stage, "count," to remove COUNT(*) at top left e.g.:
        #          ticker  name
        # 0   NASDAQ:NVDA  NVDA
        # 1   NASDAQ:AMZN  AMZN
        # 2   NASDAQ:COIN  COIN

        nested_list = self.query.values.tolist()
        # nested_list returns this:
        # [['NASDAQ:NVDA', 'NVDA'], ['NASDAQ:AMZN', 'AMZN']]

        global namelist
        namelist = []
        # namelist to append after extracting the short names from nested list

        # working steps to extracting the short names
        for each_list in nested_list:  # initial each_list would print e.g. ['NASDAQ:NVDA', 'NVDA']
            for each_element in each_list:
                y = each_list.pop()  # to retrieve the removed short name, assign it to y and append it to namelist
                namelist.append(y)
                # I named each_list.pop() as each_list would print e.g. 'NASDAQ:NVDA', the leftover
                # the positioning of each_list and y acts like (x,y) in the original value of each_list

    def query(self):
        value = self.query
        return value

    def __str__(self):
        try_msg = "I'm sorry, did you mean {0}, {1} or {2}? Try again"
        value = try_msg.format(namelist[0], namelist[1], namelist[2])
        return value


# loop for if the name of uInput is not matched, will return a try again with 'try' suggestions:
if exact_name_query[0] == 0:
    print(NameLike())
    uInput = input("Enter a stock name (e.g. NVDA): ").upper()


class FromInput:
    def __init__(self, column):
        self.column = column
        self.query = (Query()
                      .select(self.column)
                      .where(Column('name') == uInput)
                      .get_scanner_data())
        value = ""

    def query(self):
        value = self.query
        return value

    # FromInput(column_name).query returns initial query

    def get_info(self):
        value = self.query
        self.query = list(self.query)
        self.query = self.query.pop()
        value = self.query.at[0, self.column]  # gets whatever value based on column searched
        return value

    # FromInput(column name).get_info() returns value from column e.g.
    # 78.657387

    # self.query.pop() due to the initial query returning:

    # (1, ticker            column_name
    # 0  NASDAQ:NVDA             x    )

    def __str__(self):
        value = self
        return value


def inputinfo(column):  # to get one specific number/name
    value = FromInput(column).get_info()
    if column == 'Recommend.All':
        if value >= 0.5:
            value = 'Strong Buy'
        elif value >= 0.1:
            value = 'Buy'
        elif value >= -0.1:
            value = 'Neutral'
        elif value >= -0.5:
            value = 'Sell'
        else:
            return 'Strong Sell'
    return value
#  for naming convenience and to format ratings


# exact_name_query[0] = (3318, ----> a COUNT(*),
# if there is 0 COUNT(*), the exact name is not found,
# hence prompting the user to try again and showcasing similar stock names

# uIndustry - The parameter describing the industry belonging to uInput (user input)
uIndustry = FromInput('industry').get_info()


def comparedata(column):
    count, df = (Query()
                 .select('price_sales_ratio', 'price_earnings_ttm', 'net_income',
                         'total_revenue', 'price_earnings_growth_ttm', 'dividends_per_share_fq',
                         'earnings_per_share_fq', 'return_on_equity', 'return_on_assets',
                         'debt_to_equity', 'price_free_cash_flow_ttm')
                 .where(Column('industry') == uIndustry)
                 .get_scanner_data())
    # get all the required columns' data
    df = df.dropna()
    # remove rows with even one 'nan' on it
    value = list(df[column])
    # convert to list for easy comparison when using the values within to calculate the mean and standard deviation
    return value


def statement(column, input_data):  # function for each statement
    # Convert input_data to a DataFrame for easier calculations
    df = pd.DataFrame(input_data)

    # Helper functions
    def valuefor(column):  # column value
        return round(df[column].iloc[0], 2)

    def stringfor(column):  # string version of column value
        return str(valuefor(column))

    def sd(column):  # standard deviation
        return float(df[column].std())

    def mean(column):  # mean
        return float(df[column].mean())

    def calc(column):  # multiplier
        return str(round(float(df[column].iloc[0] / mean(column)), 2)) + " of the average stock"

    # Shortening of long variable names using the DataFrame
    p_fcf = df['price_free_cash_flow_ttm'].iloc[0]
    roe = df['return_on_equity'].iloc[0]
    roa = df['return_on_assets'].iloc[0]
    dte = df['debt_to_equity'].iloc[0]

    # Define a mapping of cases to their respective functions
    case_map = {
        "price_sales_ratio": lambda: handle_price_sales_ratio(),
        "price_earnings_ttm": lambda: handle_price_earnings_ttm(),
        "total_revenue": lambda: handle_total_revenue(),
        "price_earnings_growth_ttm": lambda: handle_price_earnings_growth_ttm(),
        "earnings_per_share_fq": lambda: handle_earnings_per_share_fq(),
        "price_free_cash_flow_ttm": lambda: handle_price_free_cash_flow_ttm(),
        "return_on_equity": lambda: handle_return_on_equity(),
        "return_on_assets": lambda: handle_return_on_assets(),
        "debt_to_equity": lambda: handle_debt_to_equity(),
    }

    def handle_price_sales_ratio():
        ratio = df['price_sales_ratio'].iloc[0]
        if ratio > 0:
            return f"You are paying ${stringfor('price_sales_ratio')} per $1 of sales"
        elif ratio < 0:
            return None
        else:
            return "Data for amount per $1 of sales could not be found"

    def handle_price_earnings_ttm():
        ttm = df['price_earnings_ttm'].iloc[0]
        if ttm > 0:
            diff = round(ttm - df['price_sales_ratio'].iloc[0], 2)
            return f"You are paying ${stringfor('price_earnings_ttm')} per $1 of earnings, which amounts to ${diff} per $1 of expenses"
        elif ttm < 0:
            return f"You are paying ${stringfor('price_earnings_ttm')} per $1 of loss"
        else:
            return "Data for amount per $1 of earnings could not be found"

    def handle_total_revenue():
        net_income = df['net_income'].iloc[0]
        revenue = df['total_revenue'].iloc[0]
        if net_income > 0:
            profitmargin = round(net_income / revenue * 100, 2)
            msg = f"The profit margin of the company is {profitmargin}%"
            if profitmargin > 100:
                msg += ", which implies that the company's income is greater than its equity"
            return msg
        else:
            return "Data for profit margin could not be found"

    def handle_price_earnings_growth_ttm():
        growth = df['price_earnings_growth_ttm'].iloc[0]
        term = "the stock's price, its earning, and the expected growth of the company"
        if growth > 0:
            return f"You are paying ${stringfor('price_earnings_growth_ttm')} premium per $1 of {term}"
        elif growth < 0:
            amt = abs(valuefor('price_earnings_growth_ttm'))
            return f"You would get a ${amt} discount per $1 of {term}"
        else:
            return "Data for amount per $1 of premium/discount could not be found"

    def handle_earnings_per_share_fq():
        eps = df['earnings_per_share_fq'].iloc[0]
        if eps > 0:
            divpayout = round(df['dividends_per_share_fq'].iloc[0] / eps * 100, 2)
            msg = f"The dividend payout of the company is {divpayout}%, at ${round(df['dividends_per_share_fq'].iloc[0], 2)} per share"
            if divpayout > 100:
                msg += ", which implies that the company's income is greater than its equity"
            return msg
        else:
            return "Data for dividend payout could not be found"

    def handle_price_free_cash_flow_ttm():
        if p_fcf >= sd('price_free_cash_flow_ttm') + mean('price_free_cash_flow_ttm'):
            return "The stock is premium by x" + calc('price_free_cash_flow_ttm')
        elif mean('price_free_cash_flow_ttm') <= p_fcf > 1:
            return "The stock is fairly priced at x" + calc('price_free_cash_flow_ttm')
        elif 1 > p_fcf > 0:
            return "The stock is undervalued at x" + calc('price_free_cash_flow_ttm')
        elif p_fcf < 0:
            return "The stock is at a loss by x" + calc('price_free_cash_flow_ttm') + "\nThis means more cash left a company's bank account than went into it"
        else:
            return "Data for price-to-free-cash-flow ratio could not be found"

    def handle_return_on_equity():
        if roe > 100:
            return f"The return on equity is {round(roe, 2)}%, implying that the income generated by the company is greater than its equity"
        elif 100 > roe > 20:
            return f"The return on equity is {round(roe, 2)}%, implying that the company's management is VERY efficient in generating income and growth"
        elif 20 >= roe > 15:
            return f"The return on equity is {round(roe, 2)}%, implying that the company's management is efficient in generating income and growth"
        elif 5 >= roe > 0:
            return f"The return on equity is {round(roe, 2)}%, implying that the company is in a harmful zone in managing their income and growth"
        elif roe < 0:
            return f"The return on equity is {round(roe, 2)}%, implying that the company, especially the shareholders'(investments), are experiencing a loss"
        else:
            return "Data for return on equity could not be found"

    def handle_return_on_assets():
        if 100 > roa > 20:
            return f"The return on assets is {round(roa, 2)}%, implying that the company's management is VERY efficient in generating income via assets"
        elif 20 >= roa > 15:
            return f"The return on assets is {round(roa, 2)}%, implying that the company's management is efficient in generating income via assets"
        elif 5 >= roa > 0:
            return f"The return on assets is {round(roa, 2)}%, implying that the company is in a harmful zone in using assets to generate income"
        elif roa < 0:
            return f"The return on assets is {round(roa, 2)}%, implying that the company is unable to acquire/use its assets optimally to generate profit"
        else:
            return "Data for return on assets could not be found"

    def handle_debt_to_equity():
        if dte >= sd('debt_to_equity') + mean('debt_to_equity'):
            return f"The debt-to-equity of the company is high at {round(dte, 2)}%, implying that the company has been increasing its debt to finance its assets"
        elif dte < 2:
            return f"The debt-to-equity of the company is at {round(dte, 2)}%"
        elif 2 >= dte > 1:
            return f"The debt-to-equity of the company is at {round(dte, 2)}%, which is favorable"
        elif 1 >= dte > 0:
            return f"The debt-to-equity of the company is at {round(dte, 2)}%, which is VERY favorable"
        elif dte < 0:
            return f"The debt-to-equity of the company is at {round(dte, 2)}%, which means that the total value of the company's assets is less than the total amount of debt and other liabilities"
        else:
            return "Data for debt-to-equity could not be found"

    # Call the corresponding function based on the column input
    return case_map.get(column, lambda: "Invalid column")()


# Sample input data (replace ... with actual values)
input_data = {
    'price_sales_ratio': [inputinfo('price_sales_ratio')],  # Wrap scalar values in lists
    'price_earnings_ttm': [inputinfo('price_earnings_ttm')],
    'total_revenue': [inputinfo('total_revenue')],
    'price_earnings_growth_ttm': [inputinfo('price_earnings_growth_ttm')],
    'earnings_per_share_fq': [inputinfo('earnings_per_share_fq')],
    'price_free_cash_flow_ttm': [inputinfo('price_free_cash_flow_ttm')],
    'return_on_equity': [inputinfo('return_on_equity')],
    'return_on_assets': [inputinfo('return_on_assets')],
    'debt_to_equity': [inputinfo('debt_to_equity')],
    'net_income': [inputinfo('net_income')],
    'dividends_per_share_fq': [inputinfo('dividends_per_share_fq')],
    'Recommend.All': [inputinfo('Recommend.All')]  # Make sure this key exists for rating
}

# Prepare the DataFrame from input_data
df = pd.DataFrame(input_data)

# Define the columns for which the statements will be generated
columns = ['price_sales_ratio', 'price_earnings_ttm', 'total_revenue',
           'price_earnings_growth_ttm', 'earnings_per_share_fq',
           'price_free_cash_flow_ttm', 'return_on_equity',
           'return_on_assets', 'debt_to_equity']

# Map the columns with the function together for faster data processing
map_x = map(lambda col: statement(col, df), columns)

# List map_x or it will return something like <mapObject found>
map_list = list(map_x)

# *map_list to unlock each element, and separate them as a new line for each column
# The final line will be the Rating
print(*map_list, sep='\n', end='\n' + "Rating: " + str(input_data['Recommend.All'][0]))  # Access the first element





