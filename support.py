import csv

support = ["blackhole-days", "technical-support", "project-subscription"]


def store_support(info, message):
  with open("support.csv", "a", newline="") as f:
    writer = csv.writer(f)
    info.append(message.channel.name)
    writer.writerows([info])


def get_support():
  data = ""
  with open("pending.csv") as f:
    reader = csv.reader(f)
    for row in reader:
      data = data + str(row) + "\n"
  return data.strip()


def get_csv_info_title(to_get):
  for _ in support:
    if to_get in _:
      return _
  return None


def get_csv_info_num(to_get):
  count = 0
  for _ in support:
    if to_get in _:
      to_get = _
  with open("pending.csv") as f:
    reader = csv.reader(f)
    for row in reader:
      if to_get in row:
        count += 1
  return count


def get_csv_info_field(to_get):
  data = ""
  present = False
  for _ in support:
    if to_get in _:
      to_get = _
      present = True
  if present is False:
    return None
  with open("pending.csv") as f:
    reader = csv.reader(f)
    for row in reader:
      if to_get in row:
        data = data + str(row) + "\n"
  print(data)
  return data.strip()


def store_pending(info, mode):
  with open("pending.csv", mode, newline="") as f:
    writer = csv.writer(f)
    # info.append(message.channel.name)
    writer.writerows([info])


deletedTicket = []


def remove_closed_tickets(to_rm):
  deletedTicket.append(to_rm)
  data = []
  with open("support.csv") as f:
    reader = csv.reader(f)
    for row in reader:
      if to_rm in row:
        pass
      else:
        data.append(row)
  print(data)
  store_pending(data, "w")
