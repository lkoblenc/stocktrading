"""CSC 161 Project: Milestone II


"""

def open_file(filename):
    try:
        file = open(filename, 'r')
        return file
    except FileNotFoundError as error:
        print(error)
        exit()


def parse_data(file):
    data = []
    for lines in file.readlines():
        line = lines.strip().split(',')
        data.append(line)
    return data



def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

       Args:
            filename: A string for the filename containing the stock data,
                      in CSV format.

            col: A string of either "date", "open", "high", "low", "close",
                 "volume", or "adj_close" for the column of stock market data to
                 look into.

                 The string arguments MUST be LOWERCASE!

            day: An integer reflecting the absolute number of the day in the
                 data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
                 in the file.

        Returns:
            A value selected for the stock on some particular day, in some
            column col. The returned value *must* be of the appropriate type,
            such as float, int or str.
    """


cols = ["date", "open", "high", "low", "close", "volume", "adj_close"]
file = open_file(filename)
data = parse_data(file)
for i in range(len(cols)):
    if (cols[i] == col):
        colNum = i
val = data[day][colNum]
file.close()
return val


def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookeeping function to help make stock transactions.

       Args:
            funds: An acoount balance, a float; it is a value of how much money
                   you have, currently.

            stocks: An int, representing the number of stock you currently own.

            qty: An int, representing how many stock you wish to buy or sell.

            price: An float reflecting a price of a signle stock.

            buy: This option parameter, if set to true, will inititate a buy.

            sell: this option paramenter, if set to true, will initiate a sell.

        Returns:
            Two values *must* be returned. The first (a float) is the new account
            balance (funds) as the transaction is completed. The second is the number
            of stock now owned (an int) after the transaction is complete.

            Error condition #1: If the `buy` and `sell` keyword parameters are both
            set to true, or both false. You *must* print an error message, and then
            return then `funds` and `stocks` parameters unaltered. This is an ambiguous
            trancsaction request!

            Error condition #2: If you buy, or sell without enough funds or stocks to
            sell, respectively. You *must* print an error message, and then return the
            `funds` and `stocks` parameters unaltered. This is an ambiguous transaction
            request!
    """

qty = int(qty)
price = float(price)
total = price*qty

if (buy):
    if (sell):
        print("Ambiguous transaction! Can't determine whether to buy or sell. No action\
              performed.")
        return funds, stocks
    elif (funds < total):
        print("Insufficient funds: purchase of {0} at ${1:.2f} requires {2:.5f}, but\
                ${3:.2f} available!".format(qty, price, total, funds))
    
        return funds, stocks
    else:
        stocks_owned = stocks + qty
        cash_balance = funds - total
        return cash_balance, stocks_owned
elif (sell):
    if (stocks < qty):
        print("Insufficient stock: {0} stocks owned, but selling {1}!".format(stocks, qty))
        return funds, stocks
    else:
        stocks_owned = stocks - qty
        cash_balance = funds + total
        return cash_balance, stocks_owned
else:
    print("Ambiguous transaction! Can't determine whether to buy or sell. No action\
            performed.")
    return funds, stocks


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to make decisions
    using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower than the moving
    average.
    - You must sell shares if the current day price is 5% higher, ore more than the
    moving average.
    - You must buy, or sell 10 stocks per transaction.
    - You are free to choose which column of stock data to use (open, close, low, high, etc)

    Args:
        A filename, as a string.

    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.        
    """

stocks_owned = 0
cash_balance = 1000
open_values = []
qty = 0
current_average = 0
file = open_file(filename)
data = parse_data(file)

del data[0]
for i in range(len(data)):
    open_values.append(float(data[i][1]))
for i in range(len(open_values)):
    if (i >= 20):
        current_average = sum(open_values[i-20:i])/20
        print(current_average)
        current_price = open_values[i]
        if (current_average <= (0.95*current_price)):
            cash_balance, stocks_owned = transact(
                cash_balance, stocks_owned, 10, current_price, True, False)
        elif ((current_average >= (1.05*current_price)) and
                  (stocks_owned >= 10)):
            cash_balance, stocks_owned = transact(
                cash_balance, stocks_owned, 10, current_price, False, True)
    if (i == (len(open_values)-1)):
            cash_balance, stocks_owned = transact(
                cash_balance, stocks_owned, stocks_owned, current_price, False, True)

file.close()
return stocks_owned, cash_balance


def main():
    filename = input("Enter a filename for stock data (CSV format): ")
    alg1_stocks, alg1_balance = alg_moving_average(filename)
    print(alg1_stocks, "{0:.2f}".format(alg1_balance))


if __name__ == '__main__':
    main()





