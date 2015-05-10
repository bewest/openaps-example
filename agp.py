"""
AGP
"""

import dateutil.parser
from openaps.uses.use import Use

class AGP (object):
  def __init__ (self):
    self.values = []
    self.hour_buckets = {}
    for hour in range(0,24):
      self.hour_buckets[hour] = []
  def add_record (self, record):
    (time, glucose, trend) = record.strip().split()
    datetime = dateutil.parser.parse(time)
    glucose = int(glucose)
    if (glucose >= 39):
      # print datetime.hour, glucose, trend
      self.values.append((datetime, glucose, trend))
      bucket = self.hour_buckets.get(datetime.hour, [])
      bucket.append(glucose)
  def __call__ (self, data):
    stats = [ ]
    for record in data:
      self.add_record(record)
    for hour in range(0,24):
      stats.append((hour, calc_agp(self.hour_buckets[hour])))
    return stats

def calc_agp (bucket):
  vals_sorted = sorted(bucket)
  # print vals_sorted, bucket
  percentile_10 = []
  median = []
  percentile_25 = []
  percentile_75 = []
  percentile_90 = []
  if len(vals_sorted) > 0:
    percentile_10 = vals_sorted[int(len(vals_sorted)*.1)]
    median = vals_sorted[int(len(vals_sorted)/2)]
    percentile_25 = vals_sorted[int(len(vals_sorted)*.25)]
    percentile_75 = vals_sorted[int(len(vals_sorted)*.75)]
    percentile_90 = vals_sorted[int(len(vals_sorted)*.9)]
  return (percentile_10, percentile_25, median, percentile_75, percentile_90)


class agp (Use):
  """ Calculate agp
  """
  def get_params (self, args):
    return dict(input=args.input)
  def configure_app (self, app, parser):
    parser.add_argument('input', default='glucose.txt')

  def main (self, args, app):
    """
    AGP??
    """
    print args
    params = self.get_params(args)
    print params.get('input')
    parser = AGP( )
    with open(params.get('input'), 'r') as f:
      return parser(f.readlines())

def set_config (args, device):
  return

def display_device (device):
  return ''

def get_uses (device, config):
  return [ agp ]

if __name__ == '__main__':
  parser = AGP( )
  with open("glucose.txt") as f:
    for hour, vals in parser(f.readlines()):
      print hour, vals

