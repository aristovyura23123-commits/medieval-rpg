# Правила проекта «Пепел и Сталь» (Dark Medieval RPG)
- Фронтенд находится в `@dark_medieval_rpg.html`, бэкенд бота — в `@telegram_rpg_bot.py` (на базе aiogram 3.x).
- Строго сохраняй палитру Dark Medieval: фон `#12100e`, карточки `#1c1917` и `#292524`, акцент `#d4af37`, HP `#991b1b`, шрифты `Cinzel` и `Inter`, мобильную верстку `100dvh` без горизонтального скролла.
- При добавлении новых предметов в `ITEM_CATALOG` или локаций в `DUNGEONS` сохраняй обратную совместимость структуры `localStorage` (`dark_medieval_rpg_save_v1`).
- Любые новые поля, отправляемые через `Telegram.WebApp.sendData()`, синхронно добавляй в обработчик `handle_webapp_data` внутри `@telegram_rpg_bot.py`.