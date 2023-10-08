from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from db import *
from queries import *
from utils import *

BOT_TOKEN = 'YOUR TOKEN'

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str]] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()  # Состояние ожидания ввода имени
    fill_answer_1 = State()    # Состояние ожидания ввода ответа на вопрос 1
    fill_answer_2 = State()    # Состояние ожидания ввода ответа на вопрос 2
    fill_answer_3 = State()    # Состояние ожидания ввода ответа на вопрос 3
    fill_answer_4 = State()    # Состояние ожидания ввода ответа на вопрос 4
    fill_answer_5 = State()    # Состояние ожидания ввода ответа на вопрос 5
    fill_answer_6 = State()    # Состояние ожидания ввода ответа на вопрос 6
    fill_answer_7 = State()    # Состояние ожидания ввода ответа на вопрос 7
    fill_answer_8 = State()    # Состояние ожидания ввода ответа на вопрос 8
    fill_answer_9 = State()    # Состояние ожидания ввода ответа на вопрос 9
    fill_answer_10 = State()    # Состояние ожидания ввода ответа на вопрос 10
    fill_answer_11 = State()    # Состояние ожидания ввода ответа на вопрос 11
    fill_answer_12 = State()    # Состояние ожидания ввода ответа на вопрос 12
    fill_answer_13 = State()    # Состояние ожидания ввода ответа на вопрос 13
    fill_answer_14 = State()    # Состояние ожидания ввода ответа на вопрос 14
    fill_answer_15 = State()    # Состояние ожидания ввода ответа на вопрос 15
    fill_answer_16 = State()    # Состояние ожидания ввода ответа на вопрос 16
    fill_answer_17 = State()    # Состояние ожидания ввода ответа на вопрос 17
    fill_answer_18 = State()    # Состояние ожидания ввода ответа на вопрос 18
    fill_answer_19 = State()    # Состояние ожидания ввода ответа на вопрос 19
    fill_answer_20 = State()    # Состояние ожидания ввода ответа на вопрос 20


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к тестированию анкеты, отправив команду /exam
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    conn = await get_conn()

    total_questions = await conn.fetchval(GET_QUESTIONS_COUNT)

    await message.answer(
        text='Этот бот позволяет пройти пробную диагностическую руботу\n'
             'Сейчас в банке заданий - ' + str(total_questions) + ' вопроса.\n'
             'Для начала тестирования отправьте команду /exam')
    await conn.close()


# Этот хэндлер будет срабатывать на команду /exam
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands='exam'), StateFilter(default_state))
async def process_exam_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваши фамилию, имя и отчество.\nНапример: Иванов Иван Иванович')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода ответа на первый вопрос
@dp.message(StateFilter(FSMFillForm.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    conn = await get_conn()
    user_exists = await conn.fetchrow(GET_USER_BY_TG_ID, message.from_user.id)

    if not user_exists:
        user_id = await conn.fetchval(INSERT_NEW_USER, message.text, message.from_user.username, message.from_user.id)
    else:
        await message.answer(text='В прошлый раз Вы проходили тестирование под именем: ' + str(user_exists.get('name')) + '. Теперь Вы записаны под именем: ' + message.text)
        user_id = await conn.fetchval(UPDATE_USER, message.text, message.from_user.username, message.from_user.id)

    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)

    await state.update_data(user_id=user_id)

    # Генерация теста
    q = await generate_test(conn)

    attempt_id = await conn.fetchval(INSERT_ATTEMPT, user_id, q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15], q[16], q[17], q[18], q[19])
    await state.update_data(attempt_id=attempt_id)
    await state.update_data(question_1_id=q[0])
    await state.update_data(question_2_id=q[1])
    await state.update_data(question_3_id=q[2])
    await state.update_data(question_4_id=q[3])
    await state.update_data(question_5_id=q[4])
    await state.update_data(question_6_id=q[5])
    await state.update_data(question_7_id=q[6])
    await state.update_data(question_8_id=q[7])
    await state.update_data(question_9_id=q[8])
    await state.update_data(question_10_id=q[9])
    await state.update_data(question_11_id=q[10])
    await state.update_data(question_12_id=q[11])
    await state.update_data(question_13_id=q[12])
    await state.update_data(question_14_id=q[13])
    await state.update_data(question_15_id=q[14])
    await state.update_data(question_16_id=q[15])
    await state.update_data(question_17_id=q[16])
    await state.update_data(question_18_id=q[17])
    await state.update_data(question_19_id=q[18])
    await state.update_data(question_20_id=q[19])

    await message.answer(text='Сгенерирован вариант диагностической работы № ' + str(attempt_id))
    question_1 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, q[0])
    await message.answer(text='Дайте ответ на вопрос №1' + '(id=' + str(q[0]) + '):\n' + str(question_1))

    await conn.close()
    # Устанавливаем состояние ожидания ввода ответа на первый вопрос
    await state.set_state(FSMFillForm.fill_answer_1)


@dp.message(StateFilter(FSMFillForm.fill_answer_1))
async def process_answer_1(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_1_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_1, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_1 = similarity.item()
    await conn.execute(INSERT_RESULT_1, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_1_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_1_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')

    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_1))
    if result_1 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_2 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_2_id'))
    await message.answer(text='Дайте ответ на вопрос №2' + '(id=' + str(data.get('question_2_id')) + '):\n' + str(question_2))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_2)


@dp.message(StateFilter(FSMFillForm.fill_answer_2))
async def process_answer_2(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_2_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_2, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_2 = similarity.item()
    await conn.execute(INSERT_RESULT_2, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_2_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_2_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_2))
    if result_2 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_3 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_3_id'))
    await message.answer(text='Дайте ответ на вопрос №3' + '(id=' + str(data.get('question_3_id')) + '):\n' + str(question_3))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_3)


@dp.message(StateFilter(FSMFillForm.fill_answer_3))
async def process_answer_3(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_3_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_3, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_3 = similarity.item()
    await conn.execute(INSERT_RESULT_3, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_3_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_3_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_3))
    if result_3 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_4 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_4_id'))
    await message.answer(text='Дайте ответ на вопрос №4' + '(id=' + str(data.get('question_4_id')) + '):\n' + str(question_4))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_4)


@dp.message(StateFilter(FSMFillForm.fill_answer_4))
async def process_answer_4(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_4_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_4, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_4 = similarity.item()
    await conn.execute(INSERT_RESULT_4, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_4_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_4_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_4))
    if result_4 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_5 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_5_id'))
    await message.answer(text='Дайте ответ на вопрос №5' + '(id=' + str(data.get('question_5_id')) + '):\n' + str(question_5))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_5)


@dp.message(StateFilter(FSMFillForm.fill_answer_5))
async def process_answer_5(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_5_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_5, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_5 = similarity.item()
    await conn.execute(INSERT_RESULT_5, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_5_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_5_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_5))
    if result_5 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_6 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_6_id'))
    await message.answer(text='Дайте ответ на вопрос №6' + '(id=' + str(data.get('question_6_id')) + '):\n' + str(question_6))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_6)


@dp.message(StateFilter(FSMFillForm.fill_answer_6))
async def process_answer_6(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_6_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_6, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_6 = similarity.item()
    await conn.execute(INSERT_RESULT_6, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_6_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_6_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_6))
    if result_6 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_7 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_7_id'))
    await message.answer(text='Дайте ответ на вопрос №7' + '(id=' + str(data.get('question_7_id')) + '):\n' + str(question_7))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_7)


@dp.message(StateFilter(FSMFillForm.fill_answer_7))
async def process_answer_7(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_7_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_7, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_7 = similarity.item()
    await conn.execute(INSERT_RESULT_7, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_7_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_7_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_7))
    if result_7 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_8 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_8_id'))
    await message.answer(text='Дайте ответ на вопрос №8' + '(id=' + str(data.get('question_8_id')) + '):\n' + str(question_8))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_8)


@dp.message(StateFilter(FSMFillForm.fill_answer_8))
async def process_answer_8(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_8_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_8, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_8 = similarity.item()
    await conn.execute(INSERT_RESULT_8, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_8_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_8_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_8))
    if result_8 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_9 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_9_id'))
    await message.answer(text='Дайте ответ на вопрос №9' + '(id=' + str(data.get('question_9_id')) + '):\n' + str(question_9))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_9)


@dp.message(StateFilter(FSMFillForm.fill_answer_9))
async def process_answer_9(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_9_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_9, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_9 = similarity.item()
    await conn.execute(INSERT_RESULT_9, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_9_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_9_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_9))
    if result_9 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_10 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_10_id'))
    await message.answer(text='Дайте ответ на вопрос №10' + '(id=' + str(data.get('question_10_id')) + '):\n' + str(question_10))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_10)


@dp.message(StateFilter(FSMFillForm.fill_answer_10))
async def process_answer_10(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_10_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_10, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_10 = similarity.item()
    await conn.execute(INSERT_RESULT_10, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_10_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_10_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_10))
    if result_10 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_11 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_11_id'))
    await message.answer(text='Дайте ответ на вопрос №11' + '(id=' + str(data.get('question_11_id')) + '):\n' + str(question_11))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_11)


@dp.message(StateFilter(FSMFillForm.fill_answer_11))
async def process_answer_11(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_11_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_11, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_11 = similarity.item()
    await conn.execute(INSERT_RESULT_11, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_11_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_11_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_11))
    if result_11 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_12 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_12_id'))
    await message.answer(text='Дайте ответ на вопрос №12' + '(id=' + str(data.get('question_12_id')) + '):\n' + str(question_12))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_12)


@dp.message(StateFilter(FSMFillForm.fill_answer_12))
async def process_answer_12(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_12_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_12, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_12 = similarity.item()
    await conn.execute(INSERT_RESULT_12, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_12_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_12_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_12))
    if result_12 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_13 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_13_id'))
    await message.answer(text='Дайте ответ на вопрос №13' + '(id=' + str(data.get('question_13_id')) + '):\n' + str(question_13))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_13)


@dp.message(StateFilter(FSMFillForm.fill_answer_13))
async def process_answer_13(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_13_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_13, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_13 = similarity.item()
    await conn.execute(INSERT_RESULT_13, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_13_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_13_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_13))
    if result_13 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_14 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_14_id'))
    await message.answer(text='Дайте ответ на вопрос №14' + '(id=' + str(data.get('question_14_id')) + '):\n' + str(question_14))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_14)


@dp.message(StateFilter(FSMFillForm.fill_answer_14))
async def process_answer_14(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_14_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_14, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_14 = similarity.item()
    await conn.execute(INSERT_RESULT_14, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_14_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_14_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_14))
    if result_14 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_15 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_15_id'))
    await message.answer(text='Дайте ответ на вопрос №15' + '(id=' + str(data.get('question_15_id')) + '):\n' + str(question_15))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_15)


@dp.message(StateFilter(FSMFillForm.fill_answer_15))
async def process_answer_15(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_15_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_15, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_15 = similarity.item()
    await conn.execute(INSERT_RESULT_15, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_15_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_15_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_15))
    if result_15 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_16 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_16_id'))
    await message.answer(text='Дайте ответ на вопрос №16' + '(id=' + str(data.get('question_16_id')) + '):\n' + str(question_16))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_16)


@dp.message(StateFilter(FSMFillForm.fill_answer_16))
async def process_answer_16(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_16_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_16, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_16 = similarity.item()
    await conn.execute(INSERT_RESULT_16, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_16_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_16_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_16))
    if result_16 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_17 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_17_id'))
    await message.answer(text='Дайте ответ на вопрос №17' + '(id=' + str(data.get('question_17_id')) + '):\n' + str(question_17))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_17)


@dp.message(StateFilter(FSMFillForm.fill_answer_17))
async def process_answer_17(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_17_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_17, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_17 = similarity.item()
    await conn.execute(INSERT_RESULT_17, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_17_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_17_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_17))
    if result_17 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_18 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_18_id'))
    await message.answer(text='Дайте ответ на вопрос №18' + '(id=' + str(data.get('question_18_id')) + '):\n' + str(question_18))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_18)


@dp.message(StateFilter(FSMFillForm.fill_answer_18))
async def process_answer_18(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_18_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_18, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_18 = similarity.item()
    await conn.execute(INSERT_RESULT_18, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_18_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_18_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_18))
    if result_18 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_19 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_19_id'))
    await message.answer(text='Дайте ответ на вопрос №19' + '(id=' + str(data.get('question_19_id')) + '):\n' + str(question_19))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_19)


@dp.message(StateFilter(FSMFillForm.fill_answer_19))
async def process_answer_19(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_19_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_19, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_19 = similarity.item()
    await conn.execute(INSERT_RESULT_19, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_19_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_19_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_19))
    if result_19 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    question_20 = await conn.fetchval(GET_QUESTION_VAL_BY_ID, data.get('question_20_id'))
    await message.answer(text='Дайте ответ на вопрос №20' + '(id=' + str(data.get('question_20_id')) + '):\n' + str(question_20))
    await conn.close()
    await state.set_state(FSMFillForm.fill_answer_20)


@dp.message(StateFilter(FSMFillForm.fill_answer_20))
async def process_answer_20(message: Message, state: FSMContext):
    conn = await get_conn()
    data = await state.get_data()
    correct_answer = await conn.fetchval(GET_RIGHT_ANSWER_BY_ID, data.get('question_20_id'))
    current_attempt = await conn.fetchval(INSERT_ANSWER_20, message.text, data.get('attempt_id'))
    similarity = await calculate_similarity(message.text, correct_answer)
    result_20 = similarity.item()
    await conn.execute(INSERT_RESULT_20, data.get('attempt_id'), similarity.item())

    discipline_name = await conn.fetchval(GET_DISCIPLINE_BY_QUESTION, data.get('question_20_id'))
    competence_name = await conn.fetchval(GET_COMPETENCE_BY_QUESTION, data.get('question_20_id'))
    await message.answer(text=f'Это был вопрос по дисциплине: {discipline_name}\n'
                              f'Проверяемая компетенция: {competence_name}\n'
                              f'Вариант работы: {current_attempt}')
    await message.answer(text='Эталонный ответ на этот вопрос:\n' + correct_answer)
    await message.answer(text='Схожесть Вашего ответа с эталонным: ' + str(result_20))
    if result_20 >= 0.7:
        await message.answer(text='По моей предварительной оценке Вы ответили верно!')
    else:
        await message.answer(text='По моей предварительной оценке Вы ответили неправильно.')
    total_right_answers = await conn.fetchval(COUNT_RIGHT_ANSWERS, data.get('attempt_id'))
    await conn.fetchval(INSERT_TOTAL, data.get('attempt_id'), total_right_answers * 5)
    await conn.execute(SET_END_TIME, data.get('attempt_id'))
    attempt_time = await conn.fetchval(CALCULATE_ATTEMPT_TIME, data.get('attempt_id'))
    await message.answer(text=f'Вы завершили решение варианта работы №{current_attempt}\n'
                              f'Процент верных ответов: {total_right_answers * 5} %\n'
                              f'Затрачено времени на попытку: {attempt_time}\n'
                              f'Для новой попытки введите команду /exam')
    await conn.close()
    await state.clear()


# Запускаем поллинг
if __name__ == '__main__':
    dp.run_polling(bot)
