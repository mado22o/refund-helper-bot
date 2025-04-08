from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, LabeledPrice
import logging
import os

API_TOKEN = os.getenv('API_TOKEN')
PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("Створити шаблон спору"))
main_kb.add(KeyboardButton("Інструкція для відео"))
main_kb.add(KeyboardButton("Преміум доступ"))
main_kb.add(KeyboardButton("Зв'язатися з оператором"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привіт! Я RefundHelperBot. Обери дію нижче:", reply_markup=main_kb)

@dp.message_handler(lambda message: message.text == "Створити шаблон спору")
async def handle_template(message: types.Message):
    template_text = (
        "**Шаблон для спору:**\n"
        "Hello, I received the package today but unfortunately the item is missing.\n"
        "I opened the box in front of the camera and there was nothing inside except some packaging.\n"
        "Please process a refund. Thank you."
    )
    await message.answer(template_text, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == "Інструкція для відео")
async def handle_instruction(message: types.Message):
    guide_text = (
        "**Інструкція для відео-доказу:**\n"
        "1. Знімайте одразу з коробкою, показуйте трек-номер.\n"
        "2. Відкривайте повільно, без монтажу.\n"
        "3. Показуйте, що всередині — нічого або не те.\n"
        "4. Повторіть ще раз вміст.\n"
        "\nВажливо: знімайте при хорошому освітленні."
    )
    await message.answer(guide_text, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == "Преміум доступ")
async def handle_premium(message: types.Message):
    prices = [LabeledPrice(label='Преміум доступ (PDF + гіди)', amount=10000)]
    await bot.send_invoice(
        message.chat.id,
        title='Преміум доступ RefundHelperBot',
        description='Отримай доступ до PDF-гайдів, шаблонів і приватного чату.',
        provider_token=PROVIDER_TOKEN,
        currency='UAH',
        prices=prices,
        start_parameter='premium-refund',
        payload='premium_access_refund'
    )

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    await message.answer("Дякуємо за оплату! Ось твій доступ до преміум-матеріалів:")
    await message.answer_document(open('premium_materials.pdf', 'rb'))

@dp.message_handler(lambda message: message.text == "Зв'язатися з оператором")
async def contact_operator(message: types.Message):
    await message.answer("Зв'яжись з нами через @YourOperatorUsername або на email: support@example.com")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
