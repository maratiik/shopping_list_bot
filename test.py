'''items_list = request_items(call)
item_url = ''
if items_list != None:
    for value in items_list:
        if HTTP in value:
            item_name = value[:value.find(HTTP)-1]
            item_url = value[value.find(HTTP):]
        item = Item(item_name, item_url)
        print(f'{item.name}, {item.url}, {item.markdown_name}')
        shopping_list.append(item)
        print(shopping_list)
        item_buttons.append(types.InlineKeyboardButton(item.name, callback_data=item_name))
        print(item_buttons)
        bot.answer_callback_query(call.id, f'Вы добавили {item.name}')

def request_items(call):
    request_message = 'Что добавить?'
    bot.send_message(call.message.chat.id, request_message)
    @bot.message_handler()
    def message_to_list(message):
        text = message.text.split(sep=', ')
        return text
'''

from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter

API_TOKEN = '6489686700:AAGvaOAVkzLrxM3naxmXYHgD98snoi3784Q'
PRODUCTS = [
    {'id': '0', 'name': 'xiaomi mi 10', 'price': 400},
    {'id': '1', 'name': 'samsung s20', 'price': 800},
    {'id': '2', 'name': 'iphone 13', 'price': 1300}
]

bot = TeleBot(API_TOKEN)
products_factory = CallbackData('product_id', prefix='products')


def products_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=product['name'],
                    callback_data=products_factory.new(product_id=product["id"])
                )
            ]
            for product in PRODUCTS
        ]
    )


def back_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text='⬅',
                    callback_data='back'
                )
            ]
        ]
    )


class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


@bot.message_handler(commands=['products'])
def products_command_handler(message: types.Message):
    bot.send_message(message.chat.id, 'Products:', reply_markup=products_keyboard())


# Only product with field - product_id = 2
@bot.callback_query_handler(func=None, config=products_factory.filter(product_id='2'))
def product_one_callback(call: types.CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Not available :(', show_alert=True)


# Any other products
@bot.callback_query_handler(func=None, config=products_factory.filter())
def products_callback(call: types.CallbackQuery):
    callback_data: dict = products_factory.parse(callback_data=call.data)
    product_id = int(callback_data['product_id'])
    product = PRODUCTS[product_id]

    text = f"Product name: {product['name']}\n" \
           f"Product price: {product['price']}"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=back_keyboard())


@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back_callback(call: types.CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Products:', reply_markup=products_keyboard())


bot.add_custom_filter(ProductsCallbackFilter())
bot.infinity_polling()