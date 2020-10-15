from datetime import datetime
from pytz import timezone, utc
import dateutil.parser

local_tz = timezone('America/Sao_Paulo')

def timestampToDate(timestamp_str):
  date_time_obj = dateutil.parser.parse(timestamp_str).replace(tzinfo=utc).astimezone(local_tz).replace(microsecond=0)
 
  print('Date:', date_time_obj.date())
  print('Time:', date_time_obj.time())
  print('Date-time:', date_time_obj)

  return date_time_obj

def timeTuple(date):
  yyyy,mm,dd = str(date.date()).split('-');
  fmt = dd + '/' + mm + '/' + yyyy

  return (fmt, str(date.time()))

def timestampToTimeTuple(timestamp_str):
  return timeTuple(timestampToDate(timestamp_str))

def datetimeArrToTimeTupleArr(datetime_arr):
  arr = []
  for datetime in datetime_arr:
    arr.append(timestampToTimeTuple(str(datetime)))
  return arr
