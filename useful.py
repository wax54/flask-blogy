
def create_get_query_string(dictionary, path="/"):
    """creates a query string out of the supplied dictionary and appends it to the path
    note: only strings and numbers are accepted, all others will be ignored"""

    redirect_string = path
    if dictionary:
        redirect_string += '?'
    else:
        return redirect_string

    arg_strings = []

    for k, v in dictionary.items():
        if isinstance(k, (str, float, int)) and isinstance(v, (str, float, int)):
            arg_strings.append(f"{ k }={ v }")

    redirect_string += "&".join(arg_strings)
    return redirect_string


def format_money(symbol, amount):
    """ ensurses the amount contains two decimal places and prepends the symbol 
    returns the resulting string
    """
    if amount < 0:
        amount = amount * -1
        symbol = "-"+symbol
    rounded = '{:.2f}'.format(amount)
    return symbol + str(rounded)
