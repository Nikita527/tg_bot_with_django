import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import DJANGO_API_URL

router = Router()


@router.message(Command("start"))
async def start(message: Message) -> None:
    args = message.text.strip().split()
    if len(args) > 1:
        token = args[1]
        telegram_id = message.from_user.id
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        username = message.from_user.username or ""

        data = {
            "token": token,
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(DJANGO_API_URL, json=data) as response:
                    if response.status == 200:
                        await message.answer(
                            "Вы успешно авторизовались на сайте!"
                        )
                    else:
                        error_text = await response.text()
                        await message.answer(
                            f"Ошибка авторизации: {error_text}"
                        )
            except Exception as e:
                await message.answer(
                    f"Произошла ошибка при обращении к серверу: {e}"
                )

    else:
        await message.answer(
            "Пожалуйста, перейдите по ссылке с сайта для авторизации."
        )
