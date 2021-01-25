'''
Created on 15 mai 2016

@author: PASTOR Robert
'''

from datetime import  date, timedelta


def number_of_days_in_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    internalDate = next_month - timedelta(days=next_month.day)
    return internalDate.day


def computeListOfWeeks(year, month):
    setOfWeeks = set()
    startDate = date(year=year, month=month, day=1)
    for day in range(1, number_of_days_in_month(startDate)):
        internalDate = date(year=year, month=month, day=day)
        setOfWeeks.add(internalDate.isocalendar()[1])

    return list(setOfWeeks)


if __name__ == '__main__':
    for month in range(1,13):
        print ( ' month = {month}'.format(month=month) )
        for week in computeListOfWeeks(year=2016, month=month):
            print (week)

