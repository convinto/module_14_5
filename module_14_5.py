from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = '#'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить') #В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
button4 = KeyboardButton(text='Регистрация')

kb.add(button1)
kb.add(button2)
kb.add(button3) #В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
kb.add(button4) #Кнопки главного меню дополните кнопкой "Регистрация".


#Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4". У всех кнопок назначьте callback_data="product_buying"
in_buy = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
    [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
    [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
    [InlineKeyboardButton(text='Product4', callback_data="product_buying")],
    ], resize_keyboard=True
)

user = get_all_products()

#Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
@dp.message_handler(text = 'Купить')
async def  get_buying_list(message):
    with open("ran_1.jpg", "rb") as img:
        await message.answer(f"Название: {user[0][1]} | Описание: {user[0][2]} | Цена: {user[0][3]} руб.")
        await message.answer_photo(img)
    with open("ran_2.jpg", "rb") as img:
        await message.answer(f"Название: {user[1][1]} | Описание: {user[1][2]} | Цена: {user[1][3]} руб.")
        await message.answer_photo(img)
    with open("ran_3.jpg", "rb") as img:
        await message.answer(f"Название: {user[2][1]} | Описание: {user[2][2]} | Цена: {user[2][3]} руб.")
        await message.answer_photo(img)
    with open("ran_4.jpg", "rb") as img:
        await message.answer(f"Название: {user[3][1]} | Описание: {user[3][2]} | Цена: {user[3][3]} руб.")
        await message.answer_photo(img)
    await message.answer(text='Выберите продукт для покупки:', reply_markup=in_buy)


#Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(text="Вы успешно приобрели продукт!")
    await call.answer

inkb = InlineKeyboardMarkup(resize_keyboard=True)
but1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data = "calories")
but2 = InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas')
inkb.add(but1)
inkb.add(but2)

@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup = inkb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(text="10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(usnam=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(em=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(ag=message.text)
    data = await state.get_data()
    add_user(data['usnam'], data['em'], data['ag'])
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text = "calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    await message.answer(f'Ваша норма {result} ккал/день')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
