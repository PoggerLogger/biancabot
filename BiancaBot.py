import Loaders
from discord.ext import commands

yaml_file = './tokens.yaml'
yaml_data = Loaders.yaml_loader(yaml_file)
token = yaml_data["token"]
client = commands.Bot(command_prefix='$')
client.load_extension('TaylorBowl')
client.run(token)
