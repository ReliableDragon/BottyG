from datetime import datetime, timedelta, timezone
import re

"""
command format:
  !convert ${TZ} ${TIME} ${TIME_ZONES}...
"""

TIME_ZONES = {
  "CEST": 2,
  "CET": 1,
  "IST": 1,
  "GMT": 0,
  "UTC": 0,
  "EDT": -4,
  "EST": -5,
  "PDT": -7,
  "PST": -8,
}


# def convert_utc(base_tz, hour, minute, conversion_tzs):
#   utc_hour =
#   utc_time = datetime.datetime(
#       year=1970,
#       month=1,
#       day=1,
#       hour=hour,
#       minute=minute,
#       tzinfo=datetime.timezone.utc)
#   converted_times = {}
#
#   for conversion in conversion_tzs:
#     if conversion in TIME_ZONES:
#       offset = timedelta(hours=TIME_ZONES[conversion])
#       converted_time = utc_time + offset
#       converted_times[conversion] = (converted_time.hour, converted_time.minute)

def convert_times(base_tz, hour, minute, conversion_tzs):
  base_time = datetime(
      year=1970,
      month=1,
      day=1,
      hour=hour,
      minute=minute,
      tzinfo=timezone(
          timedelta(hours=TIME_ZONES[base_tz])))
  converted_times = {}

  for tz in conversion_tzs:
    if tz in TIME_ZONES:
      converted_time = base_time.astimezone(
          timezone(timedelta(hours=TIME_ZONES[tz])))
      converted_times[tz] = (converted_time.hour, converted_time.minute)

  return converted_times


def generate_time_zone_response(message):
  message = message.lower()
  command = "!convert "
  if not message.startswith(command):
    return None

  message = message[len(command):].strip()
  parts = message.split(" ")

  if len(parts) < 3:
    return "Usage: !convert {BASE_TZ} {TIME} {TIME_ZONE...}.\nEx: !convert UTC 05:30 CEST PDT"

  base_time_zone = parts[0].upper()
  base_time = parts[1]
  conversion_time_zones = parts[2:len(parts)]
  conversion_time_zones = [tz.upper() for tz in conversion_time_zones]
  all_time_zones = [base_time_zone] + conversion_time_zones

  if not all(tz in TIME_ZONES for tz in all_time_zones):
    unsupported_tzs = list(filter(lambda tz: tz not in TIME_ZONES, all_time_zones))
    msg = "Unsupported time zone(s):"
    for tz in unsupported_tzs:
      msg += " " + tz
    msg += "\nSupported time zones are:"
    for k in TIME_ZONES.keys():
      msg += " " + k
    msg += "\nIf you want another timezone added, contact ReliableDragon."
    return msg

  if not re.match(r'(?:[0-1]\d|2[03]):[0-5]\d', base_time):
    msg = ("Can't understand time {}. "
          "Please use HH:MM time format. "
          "(e.g., 05:30, 23:30, etc)").format(base_time)
    return msg

  hour = int(base_time[:2])
  minute = int(base_time[3:])

  converted_times = convert_times(base_time_zone, hour, minute, conversion_time_zones)
  msg = base_time + " " + base_time_zone + " is:"
  for tz, time in converted_times.items():
    hour = time[0]
    min = time[1]
    msg += "\n  {:02d}:{:02d} {}".format(hour, minute, tz)

  return msg
