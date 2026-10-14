"""
Telegram Bot для запуска Dark Medieval RPG Mini App (WebApp) на базе aiogram 3.x.

Возможности:
1. По команде /start отправляет атмосферное средневековое приветствие с иллюстрацией
   и Inline-кнопкой «⚔️ Войти в мир» (WebAppInfo), а также Reply-кнопкой для прямой
   передачи данных через window.Telegram.WebApp.sendData().
2. Принимает и обрабатывает JSON-данные обратно от веб-приложения (F.web_app_data),
   формируя красивую сводку подвигов героя в чате.
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

# =====================================================================
# КОНФИГУРАЦИЯ БОТА
# =====================================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8862224626:AAE5lZa-0hgnYUMTKIljaoJ5GlLTQdSrkL8")
WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    "https://aristovyura23123-commits.github.io/medieval-rpg/"
)

# Атмосферная иллюстрация темного средневековья для приветственного сообщения
WELCOME_BANNER_URL = (
    "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
    "?auto=format&fit=crop&w=1200&q=80"
)

router = Router(name="dark_medieval_rpg_router")


def build_inline_webapp_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    """Создает Inline-клавиатуру с кнопкой запуска Telegram Mini App."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚔️ Войти в мир",
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ]
    )


def build_reply_webapp_keyboard(webapp_url: str) -> ReplyKeyboardMarkup:
    """
    Создает Reply-клавиатуру с WebAppInfo.
    Позволяет веб-приложению отправлять данные обратно боту через Telegram.WebApp.sendData().
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⚔️ Войти в мир (Синхронизация летописи)",
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ],
        resize_keyboard=True,
    )


@router.message(CommandStart())
async def cmd_start_handler(message: Message) -> None:
    """Обработчик команды /start: отправляет баннер и кнопку запуска RPG Mini App."""
    first_name = message.from_user.first_name if message.from_user else "Странник"

    caption_text = (
        f"🕯 <b>Приветствую тебя у ворот Вороньего Брода, {first_name}!</b>\n\n"
        "Тьма сгущается над трактом, в Проклятом чащобнике воют волколаки, "
        "а в Склепе Древних пробудились мёртвые короли.\n\n"
        "• 🏰 <b>Таверна:</b> Залечи раны у камина, испытай удачу в костях (2d6) и бери заказы со старостиной доски.\n"
        "• ⚔️ <b>Вылазки:</b> Сражайся в пошаговых боях, собирай трофеи и редкую добычу.\n"
        "• 🎒 <b>Герой и Кузница:</b> Прокачивай Силу, Живучесть и Ловкость, куй воронёную сталь и вари эликсиры.\n\n"
        "<i>Нажми кнопку ниже, чтобы обнажить клинок и шагнуть в мир Пепла и Стали:</i>"
    )

    inline_kb = build_inline_webapp_keyboard(WEBAPP_URL)

    try:
        await message.answer_photo(
            photo=WELCOME_BANNER_URL,
            caption=caption_text,
            reply_markup=inline_kb,
        )
    except Exception:
        # Фолбэк на текстовое сообщение, если внешний URL изображения недоступен
        await message.answer(
            text=caption_text,
            reply_markup=inline_kb,
        )

    # Дополнительно предоставляем Reply-кнопку для работы window.Telegram.WebApp.sendData()
    await message.answer(
        text="📜 <i>Для отправки летописи подвигов из игры прямо в этот чат используй нижнюю кнопку меню:</i>",
        reply_markup=build_reply_webapp_keyboard(WEBAPP_URL),
    )


@router.message(F.web_app_data)
async def handle_webapp_data(message: Message) -> None:
    """
    Принимает данные обратно от веб-приложения через window.Telegram.WebApp.sendData(JSON).
    """
    if not message.web_app_data or not message.web_app_data.data:
        return

    raw_data = message.web_app_data.data
    try:
        payload: Dict[str, Any] = json.loads(raw_data)
    except json.JSONDecodeError:
        await message.answer(
            f"📜 <b>Получена депеша из Вороньего Брода:</b>\n<code>{raw_data}</code>"
        )
        return

    hero_name = payload.get("hero_name", "Странник")
    level = payload.get("level", 1)
    gold = payload.get("gold", 0)
    monsters_slain = payload.get("monsters_slain", 0)
    power_rating = payload.get("power_rating", 0)
    weapon = payload.get("weapon", "Ржавый клинок")
    armor = payload.get("armor", "Стёганый гамбезон")

    herald_text = (
        "🦅 <b>Воронья почта доставила летопись героя!</b>\n\n"
        f"🛡 <b>Имя:</b> {hero_name} (Уровень {level})\n"
        f"⚔️ <b>Боевая мощь:</b> {power_rating}\n"
        f"💰 <b>Золотые кроны:</b> {gold}\n"
        f"💀 <b>Повержено чудовищ:</b> {monsters_slain}\n"
        f"🗡 <b>Оружие:</b> {weapon}\n"
        f"🥋 <b>Доспех:</b> {armor}\n\n"
        "<i>Да хранит тебя пламя очага в следующем походе!</i>"
    )
    await message.answer(herald_text)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
