import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_correct_choice():
    question = Question(title='q1')
    question.add_choice('a', True)
    choice = question.choices[0]
    assert choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)
    assert len(question.choices) == 3
    assert question.choices[1].text == 'b'
    assert question.choices[1].is_correct

def test_choice_ids_are_sequential():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_choice_by_id(1)
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.set_correct_choices([1, 2])
    assert question.choices[0].is_correct
    assert question.choices[1].is_correct

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', True)
    result = question.correct_selected_choices([1, 2])
    assert result == [1]

def test_correct_selected_choices_exceeds_max():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', True)
    question.add_choice('b', False)
    with pytest.raises(Exception):
        question.correct_selected_choices([1, 2])


@pytest.fixture
def question_with_choices():
    question = Question(title='Capital do Brasil?', points=5, max_selections=1)
    question.add_choice('São Paulo', False)
    question.add_choice('Brasília', True)
    question.add_choice('Rio de Janeiro', False)
    return question

def test_fixture_correct_answer(question_with_choices):
    result = question_with_choices.correct_selected_choices([2])
    assert result == [2]

def test_fixture_wrong_answer(question_with_choices):
    result = question_with_choices.correct_selected_choices([1])
    assert result == []

def test_fixture_remove_and_check(question_with_choices):
    question_with_choices.remove_choice_by_id(3)
    assert len(question_with_choices.choices) == 2
    assert question_with_choices.choices[0].text == 'São Paulo'
    assert question_with_choices.choices[1].text == 'Brasília'