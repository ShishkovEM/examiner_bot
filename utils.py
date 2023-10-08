from sentence_transformers import SentenceTransformer, util
from queries import GET_QUESTIONS_BY_COMPETENCE

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')


async def generate_test(conn):
    questions = []

    # Выбираем 6 вопросов для ПК-1
    competence_questions = await conn.fetch(GET_QUESTIONS_BY_COMPETENCE, 7, 6)
    questions.extend([q['id'] for q in competence_questions])

    # Выбираем 6 вопросов для ОПК-2
    competence_questions = await conn.fetch(GET_QUESTIONS_BY_COMPETENCE, 6, 6)
    questions.extend([q['id'] for q in competence_questions])

    # Выбираем 4 вопроса для ОПК-1
    competence_questions = await conn.fetch(GET_QUESTIONS_BY_COMPETENCE, 5, 4)
    questions.extend([q['id'] for q in competence_questions])

    # Выбираем 4 вопроса для УК-2
    competence_questions = await conn.fetch(GET_QUESTIONS_BY_COMPETENCE, 1, 4)
    questions.extend([q['id'] for q in competence_questions])

    return questions


async def calculate_similarity(user_answer, correct_answer):
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    correct_embedding = model.encode(correct_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(user_embedding, correct_embedding)

    return similarity


async def evaluate_answer(user_answer, correct_answer):
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    correct_embedding = model.encode(correct_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(user_embedding, correct_embedding)

    return similarity > 0.9, similarity.item()

