from cogs.utils import default

version = "v1.0.0"
invite = "https://discord.gg/FeD6RUs"
owner = 589647651939549206


def is_owner(ctx):
    return ctx.author.id in owner