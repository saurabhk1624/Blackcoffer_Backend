from datetime import datetime
from django.db.models import Func,FloatField
def format_date(date_str):
    if not date_str.strip() :
        return None
    try:
        formatted_date = datetime.strptime(date_str, "%B, %d %Y %H:%M:%S").strftime("%Y-%m-%d")
        return formatted_date
    except:
        return None



def valid_year(value):
    try:
        year = int(value) 
        if 1000 <= year <= 9999:  
            return year
        else:
            return None  
    except (ValueError, TypeError):  
        return None




def valid_integer(data):
    if isinstance(data, str):
        if data.strip() == '':
            return None
    elif isinstance(data, int):
        return data
    else:
        return None 


class Round(Func):
    function = 'ROUND'
    arity = 2
    output_field = FloatField() 