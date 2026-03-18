import random


async def handle_counter_commands(
    cmd_token,
    message,
    get_all_counts_async,
    mention_count_commands,
    all_counts_command):
  guild_scope = str(message.guild.id) if getattr(message, "guild", None) else "dm"
  counts = await get_all_counts_async(guild_scope)
  if cmd_token in mention_count_commands:
    keyword = mention_count_commands[cmd_token]
    count = counts.get(keyword, 0)
    await message.channel.send(
        f"'{keyword}' has been mentioned {count} time(s).")
    return True
  if cmd_token == all_counts_command:
    await message.channel.send(
        "Current mention totals:\n"
        f"rocket: {counts['rocket']}\n"
        f"james: {counts['james']}\n"
        f"loss: {counts['loss']}")
    return True
  return False


async def handle_simple_commands(
    cmd_token,
    message,
    logger,
    quotes,
    reaction_images,
    commands_msg,
    reaction_images_msg,
    randint_fn=random.randint,
):
  if cmd_token in ("!advice", "!quote"):
    logger.info('Sending advice.')
    rand_num = randint_fn(0, len(quotes) - 1)
    await message.channel.send(quotes[rand_num])
    return True
  if cmd_token in reaction_images:
    logger.info('Sending reaction image for {}.'.format(cmd_token))
    await message.channel.send(reaction_images[cmd_token])
    return True
  if cmd_token in ('!help', '!commands'):
    logger.info('Sending command list.')
    await message.channel.send(commands_msg)
    return True
  if cmd_token == '!reactions':
    logger.info('Sending reaction list.')
    await message.channel.send(reaction_images_msg)
    return True
  return False
