import re

# check if command corresponds to channel id
def  validate_command(c_id, cmd):
  if c_id and cmd == "!create":
    return 1
  return 0

# check if it is a valid support event
def validate_support_event(help):
  print(help)
  support = ["blackhole-days", "technical-support", "project-subscription"]
  if help.lower() not in support:
    return 0
  else:
    return 1

# check if the hour is passed as a number
def check_hour(hour):
  try:
    h = int(hour)
    return 1
  except ValueError:
    return 0

# check if the minute is passed as a number
def check_min(min):
  try:
    m = int(min)
    return 1
  except ValueError:
    return 0

# check if time is in 24-hour format
# 0 indicates wrong hour
# -1 indicates wrong minute
# -2 indicates it is not the HH:MM format
def validate_24h_time(time_set):
  time_new = time_set.split(":")
  if len(time_new) != 2:
    return -2
  else:
    if check_hour(time_new[0]):
      if 0 <= int(time_new[0]) <= 24:
        return 1
      else:
        return 0
    if check_min(time_new[1]):
      if 0 <= int(time_new[1]) <= 60:
        return 1
      else:
        return -1

# check if valid year and if the year is passed as a number
def check_year(yr):
  years = [23, 24, 25]
  try:
    y = int(yr)
    if y not in years:
      return -1
    return 1
  except ValueError:
    return 0

# check if valid month and if the month is passed as a number
def check_month(mnth):
  try:
    m = int(mnth)
    if not 1 <= m <= 12:
      return -1
    return 1
  except ValueError:
    return 0

# check if valid date and if the date is passed as a number
def check_date(dt):
  try:
    d = int(dt)
    if not 1 <= d <= 31:
      return -1
    return 1
  except ValueError:
    return 0

# check if the date exceeds max amount of days in a month
def valid_date_in_month(dt, mnth):
  months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  if dt <= months[mnth]:
    return 1
  else:
    return 0

# check if date is in dd-mm-yy format
def validate_date(date_set):
  date_new = date_set.split("-")
  if len(date_new) != 3:
    return -2
  else:
    if check_year(date_new[2]) == 1:
      if check_month(date_new[1]) == 1:
        if check_date(date_new[0]) == 1:
          return 1
    return 0