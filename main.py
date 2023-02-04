import os
import openai
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from loguru import logger


def init():
    load_dotenv()
    openai.api_key = os.getenv("OPENAPI_API_KEY")
    logger.success("App initialized!")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = "Type something random to get started!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)
    logger.info(start_text)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = chatgpt_response(text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    logger.info(response)


async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Something went wrong: {context.error}")
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    logger.error(f"Update: {update_str}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Something went wrong! Try again later.")


def chatgpt_response(prompt: str) -> str:
    model_engine = "text-davinci-003"
    logger.debug(f"Prompt: {prompt}")
    response = openai.Completion.create(
        model=model_engine,
        prompt=prompt,
        temperature=0.6,
        max_tokens=1024
    )
    logger.debug(f"ChatGPT Response: {response}")

    return response.choices[0].text.strip()


def main():
    init()
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()
    start_handler = CommandHandler('start', start_command)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler)

    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    application.add_error_handler(error)
    logger.success("Bot started successfully!")
    logger.success("Start sending messages to https://t.me/tgram_chatgpt_ph_bot")
    application.run_polling()


if __name__ == '__main__':
    main()
