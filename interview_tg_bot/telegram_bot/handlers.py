import random

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
# from aiogram.utils.emoji import emojize

from .keyboards import make_keyboard
from .models import Topic, Question, Answer


class Interview(StatesGroup):
    topic = State()
    answer = State()


async def start_cmd(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        "Hi!\nI'm Python Interview Bot!",
        reply_markup=make_keyboard(['/topic'])
    )


async def choose_topic(message: types.Message):
    topics = await Topic.all_topics()
    kb = make_keyboard(topics)
    await Interview.topic.set()
    await message.answer(
        "Choose topic of questions.",
        reply_markup=kb
    )


async def get_question(message: types.Message, state: FSMContext):
    if message.text.lower() != 'continue':
        topic = message.text
        await state.update_data(topic=topic)
    else:
        data = await state.get_data()
        topic = data['topic']

    await Interview.next()

    questions = await Question.find_by_topic(topic)
    question = random.choice(questions).name
    await message.answer(question)

    answers = await Answer.find_by_question(question)
    kb = make_keyboard(list(range(1, len(answers) + 1)))
    random.shuffle(answers)
    answers = {str(i+1): j for i, j in enumerate(answers)}
    print(answers)
    await state.update_data(answer=answers)
    await message.answer(
        '\n\n'.join(
            [f'{k}. {v[0]}' for k, v in answers.items()]),
        reply_markup=kb
    )


async def answer_question(message: types.Message, state: FSMContext):
    if message.text.lower() not in ['continue', 'change topic']:
        data = await state.get_data()
        answer = data['answer'][message.text]

        if answer[1] is True:
            await message.answer(f':check_mark_button You are right!\n\n{answer[0]}')
        else:
            correct_answer = list(filter(lambda a: a[1][1] is True, data['answer'].items()))[0][1][1]
            await message.answer(f':cross_mark Correct answer is:\n\n {correct_answer}')

        keyboard = make_keyboard(['Continue', 'Change Topic'])
        await message.answer('Continue or change topic?', reply_markup=keyboard)
    else:

        if 'topic' in message.text.lower():
            await state.finish()
            await choose_topic(message)
        else:
            await state.set_state(Interview.topic.state)
            await get_question(message, state)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


def register_handlers(dp: Dispatcher) -> Dispatcher:
    dp.register_message_handler(
        start_cmd, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(
        cancel_handler,
        Text(equals='cancel', ignore_case=True), state='*'
    )
    dp.register_message_handler(
        choose_topic,
        lambda message: 'topic' in message.text.lower(),
        state=None
    )
    dp.register_message_handler(get_question, state=Interview.topic)
    dp.register_message_handler(answer_question, state=Interview.answer)

    return dp
