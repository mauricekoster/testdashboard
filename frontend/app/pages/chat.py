from nicegui import APIRouter, ui, background_tasks, Event

from datetime import datetime
from uuid import uuid4

from app.client.websocket import connection
from app.core.user import current_user
from app.pages.templates.landing import landingpage
import logging


messages: list[tuple[str, str, str, str, str]] = []
logger = logging.getLogger(__name__)


@ui.refreshable
def chat_messages(own_id: str) -> None:
    if messages:
        for user_id, name, avatar, text, stamp in messages:
            ui.chat_message(name=name, text=text, stamp=stamp, avatar=avatar, sent=own_id == user_id)
    else:
        ui.label('No messages yet').classes('mx-auto my-36')
    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')



def on_message_recieved(data):
    logger.info("WS Message recieved for 'chat'")
    avatar = f'https://robohash.org/{data["sender"]}?bgset=bg2'
    messages.append((data['sender'], data['user'], avatar, data['data'], data['timestamp']))
    chat_messages.refresh()


router = APIRouter()


@router.page("/chat")
async def show_chat():
    user_id = current_user.id or '0000'
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    async def send() -> None:
        
        logger.info("CHAT Send message")
        stamp = datetime.now().strftime('%X')
        avatar = f'https://robohash.org/{user_id}?bgset=bg2'
        messages.append((user_id, current_user.full_name, avatar, text.value, stamp))
        await connection.send_json(dict(
            event='chat',
            sender=user_id,
            timestamp=datetime.now().isoformat(),
            data=dict(message=text.value, user=current_user.full_name)
        ))
        text.value = ''
        chat_messages.refresh()
    
    
    await ui.context.client.connected()  # chat_messages(...) uses run_javascript which is only possible after connecting
    #connection.set_default_handler(on_message_recieved)
    connection.on('chat', on_message_recieved)

    with landingpage("chat"):

        logger.info("CHAT Start Background task")
        background_tasks.create(connection.start_task(user_id), name='chat')

        with ui.row().classes('w-full no-wrap items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .on('keydown.enter', send) \
                .props('rounded outlined input-class=mx-3').classes('flex-grow')

    
        with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
            chat_messages(user_id)

    