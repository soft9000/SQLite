import datetime
# File:    DateSortable.py
# Version: 1.0
# Updated: 2020/05/08

''' Mission: 
Enumerate calendar-accurate, sortable, year-first
be-dated tuples, strings & encoded integers.
'''

def enum_year_dates(yyyy, mm, dd, total):
    ''' Enumerate a year-first, integral tuple, series. '''
    offs = 0
    sdate = datetime.datetime(int(yyyy), int(mm), int(dd))
    for ignored in range(0, total):
        sdate = sdate.fromordinal(sdate.toordinal() + offs)
        yield sdate.year, sdate.month, sdate.day
        offs = 1


def enum_date(yyyy, mm, dd, total, sep='/'):
    ''' Pure YYYY/MM/DD, as a sortable string. '''
    for zcode in enum_year_dates(yyyy, mm, dd, total):
        mm = str(zcode[1]).zfill(2)
        dd = str(zcode[2]).zfill(2)
        yield f"{zcode[0]}{sep}{mm}{sep}{dd}"


def enum_int_date(yyyy, mm, dd, total):
    ''' Pure YYYYMMDD, as a sortable integer. '''
    for zcode in enum_date(yyyy, mm, dd, total, sep=''):
        yield int(f"{zcode}")


if __name__ == '__main__':
    for code in enum_int_date(2021, 2, 1, 45):
        print(code)
