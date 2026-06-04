import logging
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Токен: переменная BOT_TOKEN (на сервере) или файл .env (локально)
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

PROMO_LINK = "https://app.metabox.global/register?promo=U4AU7WXU"

Q1, Q2, Q3, PRESENTATION = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я помогу тебе узнать, как нейросети могут изменить твою жизнь "
        "и работу — а потом покажу один очень крутой инструмент 🚀\n\n"
        "Готов? Отвечу на несколько коротких вопросов 👇"
    )
    keyboard = [[InlineKeyboardButton("🚀 Начать", callback_data="start_quiz")]]
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return Q1


async def question_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = "🤔 *Вопрос 1 из 3*\n\n*Для чего вы хотите использовать нейросеть?*"
    keyboard = [
        [InlineKeyboardButton("✍️ Создание контента", callback_data="q1_content")],
        [InlineKeyboardButton("💼 Работа и бизнес", callback_data="q1_business")],
        [InlineKeyboardButton("🎓 Учёба и саморазвитие", callback_data="q1_study")],
        [InlineKeyboardButton("🎨 Творчество и хобби", callback_data="q1_hobby")],
        [InlineKeyboardButton("🔍 Просто интересно", callback_data="q1_curious")],
    ]
    await query.edit_message_text(
        text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return Q2


async def question_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    answers = {
        "q1_content": "✍️ Создание контента",
        "q1_business": "💼 Работа и бизнес",
        "q1_study": "🎓 Учёба и саморазвитие",
        "q1_hobby": "🎨 Творчество и хобби",
        "q1_curious": "🔍 Просто интересно",
    }
    context.user_data["q1"] = answers.get(query.data, "—")

    text = "💡 *Вопрос 2 из 3*\n\n*Какой опыт работы с нейросетями у вас есть?*"
    keyboard = [
        [
            InlineKeyboardButton(
                "🐣 Новичок — слышал, но не пробовал", callback_data="q2_newbie"
            )
        ],
        [
            InlineKeyboardButton(
                "🌱 Немного пробовал ChatGPT/Midjourney", callback_data="q2_beginner"
            )
        ],
        [
            InlineKeyboardButton(
                "⚡ Активно использую несколько сервисов", callback_data="q2_active"
            )
        ],
        [
            InlineKeyboardButton(
                "🧑‍💻 Профессионал, работаю с API", callback_data="q2_pro"
            )
        ],
    ]
    await query.edit_message_text(
        text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return Q3


async def question_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    answers = {
        "q2_newbie": "🐣 Новичок",
        "q2_beginner": "🌱 Начинающий",
        "q2_active": "⚡ Активный пользователь",
        "q2_pro": "🧑‍💻 Профессионал",
    }
    context.user_data["q2"] = answers.get(query.data, "—")

    text = "💰 *Вопрос 3 из 3*\n\n*Сколько вы сейчас тратите на нейросети в месяц?*"
    keyboard = [
        [
            InlineKeyboardButton(
                "😅 Ничего — пользуюсь бесплатными", callback_data="q3_free"
            )
        ],
        [InlineKeyboardButton("💵 До $20 в месяц", callback_data="q3_low")],
        [InlineKeyboardButton("💸 $20–$100 в месяц", callback_data="q3_mid")],
        [InlineKeyboardButton("🤑 Больше $100 в месяц", callback_data="q3_high")],
    ]
    await query.edit_message_text(
        text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRESENTATION


async def presentation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import asyncio

    query = update.callback_query
    await query.answer()

    answers = {
        "q3_free": "😅 Бесплатные",
        "q3_low": "💵 До $20",
        "q3_mid": "💸 $20–$100",
        "q3_high": "🤑 Больше $100",
    }
    context.user_data["q3"] = answers.get(query.data, "—")

    await query.edit_message_text(
        "✅ *Отлично, спасибо за ответы!*\n\n"
        "Сейчас я покажу тебе инструмент, который решит всё это сразу 👇",
        parse_mode="Markdown",
    )

    await asyncio.sleep(1.5)

    intro_text = (
        "🌟 *Знакомься — Metabox!*\n\n"
        "Metabox — это единая платформа, которая собрала в одном месте "
        "*все лучшие нейросети мира*:\n\n"
        "🤖 ChatGPT (GPT-4o, GPT-4 Turbo)\n"
        "🧠 Claude (Anthropic)\n"
        "🔍 Gemini (Google)\n"
        "🎨 Midjourney, DALL·E, Stable Diffusion\n"
        "🎵 Suno AI (музыка), ElevenLabs (голос)\n"
        "📹 Runway, Kling (видео)\n"
        "...и десятки других!\n\n"
        "_Одна подписка — безлимитный доступ ко всему._"
    )
    keyboard = [
        [InlineKeyboardButton("💥 Узнать преимущества →", callback_data="show_benefits")]
    ]
    await query.message.reply_text(
        intro_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRESENTATION


async def show_benefits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    benefits_text = (
        "🏆 *Почему Metabox лучше, чем платить за каждый сервис отдельно?*\n\n"
        "✅ *1. Экономия до 80%*\n"
        "ChatGPT Plus — $20/мес, Midjourney — $10/мес, Claude Pro — $20/мес...\n"
        "Metabox даёт всё это *в разы дешевле* в одной подписке.\n\n"
        "✅ *2. Один кабинет — все инструменты*\n"
        "Не нужно переключаться между десятками вкладок. "
        "Всё в одном месте: текст, картинки, видео, музыка, голос.\n\n"
        "✅ *3. Без VPN и иностранных карт*\n"
        "Сервис работает в СНГ — оплата картой РФ/СНГ, "
        "не нужно искать обходные пути.\n\n"
        "✅ *4. Актуальные модели без задержек*\n"
        "Новые версии нейросетей появляются в Metabox сразу после релиза.\n\n"
        "✅ *5. Для любого уровня*\n"
        "Удобный интерфейс для новичков и API-доступ для профи."
    )
    keyboard = [
        [InlineKeyboardButton("🎯 Для кого это? →", callback_data="show_usecases")]
    ]
    await query.edit_message_text(
        benefits_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_usecases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    usecases_text = (
        "🎯 *Кому особенно полезен Metabox?*\n\n"
        "✍️ *Контент-мейкерам и блогерам*\n"
        "→ Пиши посты, делай картинки и видео в 10 раз быстрее\n\n"
        "💼 *Предпринимателям и маркетологам*\n"
        "→ Автоматизируй рутину: тексты, презентации, аналитика\n\n"
        "🎨 *Дизайнерам и творческим людям*\n"
        "→ Генерируй изображения, редактируй фото, создавай арты\n\n"
        "🎓 *Студентам и тем, кто учится*\n"
        "→ Объяснения, конспекты, переводы, помощь с задачами\n\n"
        "🧑‍💻 *Разработчикам*\n"
        "→ Код, дебаггинг, документация через лучшие модели\n\n"
        "🏠 *Обычным пользователям*\n"
        "→ Ответы на любые вопросы, помощь в быту и работе"
    )
    keyboard = [
        [InlineKeyboardButton("🚀 Получить доступ →", callback_data="show_final")]
    ]
    await query.edit_message_text(
        usecases_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    final_text = (
        "🎁 *Специальное предложение для тебя!*\n\n"
        "Ты можешь прямо сейчас зарегистрироваться в Metabox "
        "по эксклюзивной ссылке и получить *бонус при регистрации*.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👇 *Нажми на кнопку ниже и начни пользоваться*\n"
        "*всеми нейросетями мира уже сегодня:*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💬 Если есть вопросы — просто напиши мне, помогу разобраться!"
    )
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Зарегистрироваться в Metabox", url=PROMO_LINK
            )
        ],
        [InlineKeyboardButton("🔄 Пройти ещё раз", callback_data="restart")],
    ]
    await query.edit_message_text(
        final_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()

    keyboard = [[InlineKeyboardButton("🚀 Начать", callback_data="start_quiz")]]
    await query.edit_message_text(
        "👋 Начнём заново! Готов отвечать на вопросы?\n\n"
        "Нажми кнопку ниже 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return Q1


def main():
    if not BOT_TOKEN:
        print("Задайте BOT_TOKEN в .env или в переменных окружения на сервере")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Q1: [
                CallbackQueryHandler(question_1, pattern="^start_quiz$"),
                CallbackQueryHandler(restart, pattern="^restart$"),
            ],
            Q2: [CallbackQueryHandler(question_2, pattern="^q1_")],
            Q3: [CallbackQueryHandler(question_3, pattern="^q2_")],
            PRESENTATION: [
                CallbackQueryHandler(presentation, pattern="^q3_"),
                CallbackQueryHandler(show_benefits, pattern="^show_benefits$"),
                CallbackQueryHandler(show_usecases, pattern="^show_usecases$"),
                CallbackQueryHandler(show_final, pattern="^show_final$"),
                CallbackQueryHandler(restart, pattern="^restart$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=False,
    )

    app.add_handler(conv_handler)

    print("Бот запущен! Нажми Ctrl+C для остановки.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
