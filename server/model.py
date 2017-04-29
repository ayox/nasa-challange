# library for timeout
from functools import wraps
import errno
import os
import signal
# library import
import csv
import json
import csvmapper
import pandas as pd


class PerdictionClient():
    ''' Generic perdiction'''

    def __init__(self):
        # initialize model
        self.initialized = True

    def get_perdiction(self):
        """get perdiction"""

        iter_csv = pd.read_csv('data/data.csv', header=0, names=["latitude", "longitude", "brightness", "bright_t31",
                                                                 "confidence", "acq_time", "acq_date", "net_lat_o", "net_lat", "net_lon_o", "net_lon"],
                               iterator=True, chunksize=1000)
        df = pd.concat([chunk[chunk['acq_date'] != '']
                        for chunk in iter_csv])
        print df
        return df.to_json(orient='records')


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
# csvfile = open('data/data.csv', 'r')

    # fieldnames = ("latitude", "longitude", "brightness", "bright_t31", "confidence",
    #               "acq_time", "acq_date", "net_lat_o", "net_lat", "net_lon_o", "net_lon")
    # reader = csv.DictReader(csvfile, fieldnames)
    # return reader

    # how does the object look
    # mapper = csvmapper.DictMapper([
    #     [
    #         {'name': 'index'},
    #         {'name': 'latitude'},
    #         {'name': 'longitude'},
    #         {'name': 'brightness'},
    #         {'name': 'bright_t31'},
    #         {'name': 'confidence'},
    #         {'name': 'acq_time'},
    #         {'name': 'acq_date'},
    #         {'name': 'net_lat_o'},
    #         {'name': 'net_lat'},
    #         {'name': 'net_lon_o'},
    #         {'name': 'net_lon'}
    #     ]
    # ])

    # # parser instance
    # parser = csvmapper.CSVParser('data/data.csv', mapper)
    # # conversion service
    # converter = csvmapper.JSONConverter(parser)
    # # print converter.doConvert(pretty=True)
    # return converter.doConvert()
