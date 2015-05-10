"""
AGP - calculate agp values given some glucose text
"""

import dateutil.parser
from openaps.uses.use import Use

class AGP (object):
  """
  The actual calculator.
  """
  def __init__ (self):
    # init empty values
    self.values = []
    # and empty buckets
    self.hour_buckets = {}
    # initialize all buckets with empty list
    for hour in range(0,24):
      self.hour_buckets[hour] = []
  def add_record (self, record):
    """ Add record to global list and assign to bucket
    """
    # clean/prep the record
    (time, glucose, trend) = record.strip().split()
    # get a proper datetime object
    datetime = dateutil.parser.parse(time)
    glucose = int(glucose)
    # ignore special values < 40
    if (glucose >= 39):
      # print datetime.hour, glucose, trend
      # append to internal list
      self.values.append((datetime, glucose, trend))
      # assign to bucket
      bucket = self.hour_buckets.get(datetime.hour, [])
      bucket.append(glucose)
  # process data and return new agp stats
  def __call__ (self, data):
    stats = [ ]
    # add all records
    for record in data:
      self.add_record(record)
    # calculate for stats each hour of day
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

##########################################
#
# openaps vendor example:
# The following shows what is needed to make the module available as a vendor
# plugin to openaps.
#

# Inherit from openaps.uses.use.Use class
class agp (Use):
  """ Calculate agp
  """

  # get_params helps openaps save your configurations
  def get_params (self, args):
    """
    Create a dict data type from args namespace so that config serializer can
    save these args for report generation.
    """
    return dict(input=args.input)

  # configure_app allows your plugin to specify command line parameters
  def configure_app (self, app, parser):
    """
    Set up any arguments needed by this use.
    """
    # get file based argument called input.
    parser.add_argument('input', default='glucose.txt')

  # main logic for the app
  def main (self, args, app):
    """
    Main logic for calculating agp
    """
    # print args
    # get parameters
    params = self.get_params(args)
    # print params.get('input')
    # create calculator
    parser = AGP( )
    with open(params.get('input'), 'r') as f:
      # calculate agp for all input
      return parser(f.readlines())

# set_config is needed by openaps for all vendors
# set_config is used by `device add` commands
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

