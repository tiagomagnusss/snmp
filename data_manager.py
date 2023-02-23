class DataManager():
  def __init__(self, session, tags: list):
    self.session = session
    self.tags = tags
    self.data_map = {}

  def get_data(self, timestamp: int, non_repeaters: int = 0, max_repetitions: int = 1) -> dict:
    if ( len(self.tags) == 0 ):
      return {}

    data = self.session.get_bulk(self.tags, non_repeaters, max_repetitions)
    new_data_map = {}
    for item in data:
      if ( item.snmp_type in ('COUNTER', 'GAUGE', 'INTEGER') ):
        if ( item.oid not in self.data_map ):
          self.data_map[item.oid] = []

        self.data_map[item.oid].append({ "timestamp": timestamp, "value": item.value })
        new_data_map[item.oid] = item.value

    return new_data_map

  def get_data_in_time(self, tag: str, time_start: int, time_end: int) -> list:
    if ( tag not in self.data_map ):
      return []

    data = self.data_map[tag]
    if ( len(data) < 2 ):
      return []

    if ( time_end < data[0]["timestamp"] ):
      return []

    if ( time_start > data[-1]["timestamp"] ):
      return []

    i = 0
    while ( time_start > data[i]["timestamp"] ):
      i += 1

    match_data = []
    while ( i < len(data) and data[i]["timestamp"] <= time_end ):
      match_data.append(data[i])
      i += 1

    return match_data

