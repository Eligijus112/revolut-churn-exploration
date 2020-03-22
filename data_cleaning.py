import pandas as pd 
import datetime 

def convert_time(
    date_string: str, 
    time_format='%Y-%m-%d %H:%M:%S.%f'
    )-> datetime.datetime:
    """
    A method to convert a string that represents datetime to a datetime object in python
    """
    # Converting the time col 
    try: 
        date_string = datetime.datetime.strptime(date_string, time_format)
    except Exception as e:
        print(f'Cannot convert to datetime {e}')

    # Returning the results
    return date_string


def dollar_band(
    amount: float,
    dollar_bands = [
        (0, 10), 
        (10, 20),
        (20, 40),
        (40, 60),
        (60, 100), 
        (100, 200),
        (200, 400),
        (400, 1000),
        (1000, 2000),
        (2000, 4000),
        (4000, 8000), 
        (8000, 20000)
    ]   
    ) -> str:
    """
    A method to create dollar bands from the amount sent
    """
    if amount >= 0:
        dollar_band = '20000+'

        for band in dollar_bands:
            if band[0] < amount <= band[1]:
                dollar_band = f"{band[0]}-{band[1]}"

        return dollar_band

def dollar_band_middle_point(
    dollar_band: str
    ) -> float: 
    """
    Returns the middle point of a given dollar band
    """
    # Trying to split by the middle simbol
    middle_point = None 
    try:
        bands = dollar_band.split('-')
        if len(bands)==2:
            middle_point = (int(bands[0]) + int(bands[1]))/2 

        # If it is the last band it will have a '+' at the end
        if len(bands)==1:
            middle_point = int(bands[0].split('+')[0])
    except Exception as e:
        print(f'Cannot create middle point {e}')       
    
    return middle_point