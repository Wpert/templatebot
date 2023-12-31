from aiogram import types, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from logic import states
from logic.texts import *
from logic.chat_logger import *
from logic import userDataBase

import sys

router = Router()

@router.message(Command('stop'))
@loggerChat(AccessStatus.admin)
async def stop(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """Полная остановка программы без сохранения локальных переменных"""
    await msg.reply('Бот сейчас же будет экстренно остановлен.')
    await state.set_state(states.UserMainMenu.menu)
    sys.exit(0)

@router.message(Command('setstatus'))
@loggerChat(AccessStatus.admin)
async def setStatus(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """"Установка пользователю уровня доступа"""
    parsedStr: str = command.args.split()
    if not len(parsedStr) == 2:
        return

    try:
        userId, userAccessStatus = parsedStr
        userDataBase[int(userId)]['status'] = int(userAccessStatus)

    except:
        await msg.reply("Возникла проблема с парсингом user_id или AccesStatus")
    
    await state.set_state(states.UserMainMenu.menu)


@router.message(Command('sendeveryone'))
@loggerChat(AccessStatus.moderator)
async def sendEveryone(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """Разослать всем пользователям сообщение в аргументах команды"""
    for userId in userDataBase.keys():
        try:
            await bot.send_message(userId, command.args, parse_mode="HTML")
        except:
            print(userId, "запретил мне сообщения :(")
    
    await state.set_state(states.UserMainMenu.menu)

@router.message()
@loggerChat(AccessStatus.default)
async def undefinedText(msg: types.Message, command: CommandObject, state: FSMContext) -> None:
    """сообщение которое не попало под обработку предыдущих функций"""
    await state.set_state(states.UserMainMenu.menu)
