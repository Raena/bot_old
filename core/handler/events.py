from enums.event import EventType
from core.handler.tasks import event_handler


def register_events(client):
    @client.event
    async def on_ready():
        print('Logged on as', client.user)
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        ctx = {"type": EventType.MESSAGE_NEW,
               "message": message}
        await event_handler(ctx)

    @client.event
    async def on_message_delete(message):
        if message.author == client.user:
            return
        ctx = {"type": EventType.MESSAGE_DELETE,
               "message": message}
        await event_handler(ctx)

    @client.event
    async def on_message_edit(before, after):
        if before.author == client.user:
            return
        ctx = {"type": EventType.MESSAGE_EDIT,
               "before": before,
               "after": after}
        await event_handler(ctx)

    @client.event
    async def on_reaction_add(reaction, user):
        if user == client.user:
            return
        ctx = {"type": EventType.REACTION_ADD,
               "reaction": reaction,
               "user": user}
        await event_handler(ctx)

    @client.event
    async def on_reaction_remove(reaction, user):
        if user == client.user:
            return
        ctx = {"type": EventType.REACTION_REMOVE,
               "reaction": reaction,
               "user": user}
        await event_handler(ctx)
