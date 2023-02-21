class DataManager():
  def __init__(self, session, tags: list):
    self.session = session
    self.tags = tags

  def get_data(self, non_repeaters: int = 0, max_repetitions: int = 1) -> dict:
    if ( len(self.tags) == 0 ):
      return {}

    data = self.session.get_bulk(self.tags, non_repeaters, max_repetitions)
    data_map = {}
    for item in data:
      if ( item.snmp_type in ('COUNTER', 'GAUGE', 'INTEGER') ):
        data_map[item.oid] = item.value

    return data_map
