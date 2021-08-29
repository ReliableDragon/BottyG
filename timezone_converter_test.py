import unittest

from timezone_converter import convert_times, generate_time_zone_response

class TestConvertTimes(unittest.TestCase):

  def test_midnight_utc(self):
    result = convert_times("UTC", 0, 0, ["EDT", "CEST"])
    self.assertDictEqual(result, {"EDT": (20, 0), "CEST": (2, 0)})

  def test_2359_pdt(self):
    result = convert_times("PDT", 23, 59, ["EST", "GMT", "CET"])
    self.assertDictEqual(result,
        {"EST": (1, 59), "GMT": (6, 59), "CET": (7, 59)})

  def test_0101_cest(self):
    result = convert_times("CEST", 1, 1, ["EST", "GMT", "PDT"])
    self.assertDictEqual(result,
        {"EST": (18, 1), "GMT": (23, 1), "PDT": (16, 1)})

class TestGenerateConversionMessage(unittest.TestCase):

  def test_no_reply_to_improper_prefix(self):
    result = generate_time_zone_response("!donvert")
    self.assertIsNone(result)

  def test_not_enough_parts(self):
    result = generate_time_zone_response("!convert CEST 02:00")
    msg =  ("Usage: !convert {BASE_TZ} {TIME} {TIME_ZONE...}.\n"
            "Ex: !convert UTC 05:30 CEST PDT")
    self.assertEqual(result, msg)

  def test_unsupported_time_zones(self):
    result = generate_time_zone_response("!convert EDU 07:00 GOV CET ORG")
    msg = ("Unsupported time zone(s): EDU GOV ORG\n"
          "Supported time zones are: CEST CET IST GMT UTC EDT EST PDT PST\n"
          "If you want another timezone added, contact ReliableDragon.")
    self.assertEqual(result, msg)

  def test_time_invalid_hour(self):
    result = generate_time_zone_response("!convert GMT 24:30 CET")
    msg = ("Can't understand time 24:30. "
          "Please use HH:MM time format. "
          "(e.g., 05:30, 23:30, etc)")
    self.assertEqual(result, msg)

  def test_time_invalid_minutes(self):
    result = generate_time_zone_response("!convert GMT 23:60 CET")
    msg = ("Can't understand time 23:60. "
          "Please use HH:MM time format. "
          "(e.g., 05:30, 23:30, etc)")
    self.assertEqual(result, msg)

  def test_time_invalid_not_HHMM(self):
    result = generate_time_zone_response("!convert GMT 5:30 CET")
    msg = ("Can't understand time 5:30. "
          "Please use HH:MM time format. "
          "(e.g., 05:30, 23:30, etc)")
    self.assertEqual(result, msg)

  def test_basic_conversion(self):
    result = generate_time_zone_response("!convert GMT 05:30 CET")
    msg = ("05:30 GMT is:\n"
          "  06:30 CET")
    self.assertEqual(result, msg)

  def test_multi_conversion(self):
    result = generate_time_zone_response("!convert PDT 23:59 EST GMT CET")
    msg = ("23:59 PDT is:\n"
          "  01:59 EST\n"
          "  06:59 GMT\n"
          "  07:59 CET")
    self.assertEqual(result, msg)


if __name__ == '__main__':
  unittest.main()
