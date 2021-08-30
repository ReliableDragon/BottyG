import re
import logging

ZERO_WIDTH_SPACE = "​"

class RocketGenerator():

  def __init__(self, emojis):
    self.logger = logging.getLogger("root")

    self.EMOJIS = emojis
    assert('spotty3') in self.EMOJIS.keys()
    assert('spotty4') in self.EMOJIS.keys()
    assert('spotty_fire') in self.EMOJIS.keys()
    assert('spotty_nose_cone') in self.EMOJIS.keys()
    assert('spotty_nose_cone_rev') in self.EMOJIS.keys()
    assert('spotty_thruster') in self.EMOJIS.keys()
    assert('spotty_thruster_rev') in self.EMOJIS.keys()

    self.ROCKET = self._gen_rocket()
    self.ROCKET_REV = self._gen_rocket_rev()
    self.ROCKET_NOSE = self._gen_rocket_nose()
    self.ROCKET_NOSE_REV = self._gen_rocket_nose_rev()
    self.ROCKET_THRUST = self._gen_rocket_thrust()
    self.ROCKET_THRUST_REV = self._gen_rocket_thrust_rev()
    self.ROCKET_BODY = self._gen_rocket_body()
    self.ROCKET_BODY_REV = self._gen_rocket_body_rev()

  def _gen_rocket(self):
    return "{}{}{}{}{}".format(
        self.EMOJIS['spotty_fire'],
        self.EMOJIS['spotty_thruster'],
        self.EMOJIS['spotty3'],
        self.EMOJIS['spotty4'],
        self.EMOJIS['spotty_nose_cone'])

  def _gen_rocket_rev(self):
    return "{}{}{}{}{}".format(
        self.EMOJIS['spotty_nose_cone_rev'],
        self.EMOJIS['spotty4'],
        self.EMOJIS['spotty3'],
        self.EMOJIS['spotty_thruster_rev'],
        self.EMOJIS['spotty_fire'])

  def _gen_rocket_nose(self):
    return self.EMOJIS['spotty_nose_cone']

  def _gen_rocket_nose_rev(self):
    return self.EMOJIS['spotty_nose_cone_rev']

  def _gen_rocket_thrust(self):
    return "{}{}".format(
        self.EMOJIS['spotty_fire'],
        self.EMOJIS['spotty_thruster'])

  def _gen_rocket_thrust_rev(self):
    return "{}{}".format(
        self.EMOJIS['spotty_thruster_rev'],
        self.EMOJIS['spotty_fire'])

  def _gen_rocket_body(self):
    return "{}{}".format(
        self.EMOJIS['spotty3'],
        self.EMOJIS['spotty4'])

  def _gen_rocket_body_rev(self):
    return "{}{}".format(
        self.EMOJIS['spotty4'],
        self.EMOJIS['spotty3'])

  async def gen_rocket_command_responses(self, message):
    msg = message.content.lower()

    if re.match(r'^!ro{0,5}cket', msg):
      await self._send_rocket_message(message)

    elif re.match(r'^!ro{6,}cket', msg):
      await self._send_rocket_failure(message)

    elif msg.startswith('!payload'):
      await self._send_payload(message)

    elif msg.startswith('!crash'):
      await self._send_crash(message)

    # Rocket mashups
    elif re.match(r'^!(?:ro|or|ck|kc|et|te){2,6}\b', msg):
      await self._send_wonky_rocket(message)

  async def _send_rocket_message(self, message):
    msg = message.content.lower()
    self.logger.info('Sending rocket')
    rocket = ZERO_WIDTH_SPACE
    rocket += self.ROCKET_THRUST
    stop = msg.find('cket')
    rocket += self.ROCKET_BODY
    for _ in range(msg[:stop].count('o')):
      rocket += self.ROCKET_BODY
    rocket += self.ROCKET_NOSE
    await message.channel.send(rocket)

  async def _send_rocket_failure(self, message):
    rocket = ZERO_WIDTH_SPACE
    rocket += self.ROCKET_THRUST
    rocket += self.ROCKET_BODY
    rocket += '💥  💥'
    rocket += self.ROCKET_BODY
    rocket += self.ROCKET_NOSE
    await message.channel.send(rocket)
    await message.channel.send('Oh the humanity!')

  async def _send_payload(self, message):
    payload = message.content[8:].strip()
    self.logger.info('Sending rocket with payload: {}'.format(payload))
    await message.channel.send(
        '{}{}{}{}{}'.format(
            ZERO_WIDTH_SPACE,
            self.ROCKET_THRUST,
            self.ROCKET_BODY,
            payload,
            self.ROCKET_NOSE))

  async def _send_crash(self, message):
    self.logger.info('Sending crash.')
    await message.channel.send("{}{}💥{}".format(
        ZERO_WIDTH_SPACE, self.ROCKET, self.ROCKET_REV))

  async def _send_wonky_rocket(self, message):
    msg = message.content.lower()
    self.logger.info('Sending wonky rocket: {}'.format(msg[:11]))
    rocket_map = {
      'ro': self.ROCKET_THRUST,
      'or': self.ROCKET_THRUST_REV,
      'ck': self.ROCKET_BODY,
      'kc': self.ROCKET_BODY_REV,
      'et': self.ROCKET_NOSE,
      'te': self.ROCKET_NOSE_REV,
    }
    i = 1
    wonky_rocket = ZERO_WIDTH_SPACE
    while i < len(msg) and msg[i:i+2] in rocket_map:
      wonky_rocket += rocket_map[msg[i:i+2]]
      i += 2
    await message.channel.send(wonky_rocket)
