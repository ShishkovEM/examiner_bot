# Получение юзера по имени
GET_USER_BY_NAME = """
SELECT * FROM users WHERE name = $1;
"""

# Получение юзера по имени
GET_USER_BY_TG_ID = """
SELECT * FROM users WHERE tg_id = $1;
"""

# Получение юзера по имени
GET_QUESTIONS_COUNT = """
SELECT COUNT(*) FROM questions;
"""

# Добавление нового юзера
INSERT_NEW_USER = """
INSERT INTO users (name, learning_group, role, tg_username, tg_id) VALUES ($1, '8М-НФ22', 1, $2, $3) RETURNING id;
"""

# Добавление нового юзера
UPDATE_USER = """
UPDATE users SET name = $1, tg_username = $2 WHERE tg_id = $3 RETURNING id;
"""

# Выбор вопросов по компетенциям
GET_QUESTIONS_BY_COMPETENCE = """
SELECT * FROM questions WHERE competence_id = $1 ORDER BY RANDOM() LIMIT $2;
"""

# Показать дисциплину по номеру вопроса
GET_DISCIPLINE_BY_QUESTION = """
SELECT name FROM disciplines WHERE id = (SELECT discipline_id FROM questions WHERE id = $1);
"""

# Показать компетенцию по номеру вопроса
GET_COMPETENCE_BY_QUESTION = """
SELECT name FROM competences WHERE id = (SELECT competence_id FROM questions WHERE id = $1);
"""

# Показать текст вопроса
GET_QUESTION_VAL_BY_ID = """
SELECT val FROM questions WHERE id = $1;
"""

# Показать эталонный ответ
GET_RIGHT_ANSWER_BY_ID = """
SELECT answer FROM questions WHERE id = $1;
"""

# Вставка попытки в базу данных
INSERT_ATTEMPT = """
INSERT INTO attempts (
    user_id, 
    question_1, question_2, question_3, question_4, question_5, 
    question_6, question_7, question_8, question_9, question_10, 
    question_11, question_12, question_13, question_14, question_15,
    question_16, question_17, question_18, question_19, question_20
) VALUES (
    $1, $2, $3,
    $4, $5, $6, $7, $8, 
    $9, $10, $11, $12, $13,
    $14, $15, $16, $17, $18,
    $19, $20, $21
) RETURNING id;
"""

# Вставка ответа 1
INSERT_ANSWER_1 = """
UPDATE attempts SET answer_1 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_2= """
UPDATE attempts SET answer_2 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_3 = """
UPDATE attempts SET answer_3 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_4 = """
UPDATE attempts SET answer_4 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_5 = """
UPDATE attempts SET answer_5 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_6 = """
UPDATE attempts SET answer_6 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_7 = """
UPDATE attempts SET answer_7 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_8 = """
UPDATE attempts SET answer_8 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_9 = """
UPDATE attempts SET answer_9 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_10 = """
UPDATE attempts SET answer_10 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_11 = """
UPDATE attempts SET answer_11 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_12 = """
UPDATE attempts SET answer_12 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_13 = """
UPDATE attempts SET answer_13 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_14 = """
UPDATE attempts SET answer_14 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_15 = """
UPDATE attempts SET answer_15 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_16 = """
UPDATE attempts SET answer_16 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_17 = """
UPDATE attempts SET answer_17 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_18 = """
UPDATE attempts SET answer_18 = $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_19 = """
UPDATE attempts SET answer_19=  $1 WHERE id = $2 RETURNING id;
"""
INSERT_ANSWER_20 = """
UPDATE attempts SET answer_20 = $1 WHERE id = $2 RETURNING id;
"""

# Вставка результата 1
INSERT_RESULT_1 = """
INSERT INTO results (attempt_id, result_1) VALUES ($1, $2) RETURNING id;
"""
INSERT_RESULT_2 = """
UPDATE results SET result_2 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_3 = """
UPDATE results SET result_3 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_4 = """
UPDATE results SET result_4 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_5 = """
UPDATE results SET result_5 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_6 = """
UPDATE results SET result_6 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_7 = """
UPDATE results SET result_7 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_8 = """
UPDATE results SET result_8 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_9 = """
UPDATE results SET result_9 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_10 = """
UPDATE results SET result_10 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_11 = """
UPDATE results SET result_11 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_12 = """
UPDATE results SET result_12 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_13 = """
UPDATE results SET result_13 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_14 = """
UPDATE results SET result_14 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_15 = """
UPDATE results SET result_15 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_16 = """
UPDATE results SET result_16 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_17 = """
UPDATE results SET result_17 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_18 = """
UPDATE results SET result_18 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_19 = """
UPDATE results SET result_19 = $2 WHERE attempt_id = $1 RETURNING id;
"""
INSERT_RESULT_20 = """
UPDATE results SET result_20 = $2 WHERE attempt_id = $1 RETURNING id;
"""

COUNT_RIGHT_ANSWERS = """
SELECT
    (CASE WHEN result_1 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_2 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_3 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_4 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_5 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_6 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_7 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_8 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_9 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_10 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_11 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_12 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_13 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_14 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_15 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_16 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_17 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_18 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_19 > 0.7 THEN 1 ELSE 0 END) +
    (CASE WHEN result_20 > 0.7 THEN 1 ELSE 0 END) AS total
FROM results
WHERE attempt_id = $1;
"""

INSERT_TOTAL = """
UPDATE results SET total = $2 WHERE attempt_id = $1 RETURNING total;
"""

SET_END_TIME = """
UPDATE attempts SET end_time = NOW() WHERE id = $1;
"""

CALCULATE_ATTEMPT_TIME = """
SELECT
    end_time - start_time
FROM attempts
WHERE id = $1;
"""