# write your code here
from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

Base = declarative_base()

Flashcards = Table('Flashcards', Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('question', String(256)),
                   Column('answer', String(256)),
                   Column('box', Integer))

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

current_id = 1
current_session = 1


class Flashcard:
    def __init__(self, id, answer, question, box):
        self.id = id
        self.answer = answer
        self.question = question
        self.box = box


mapper(Flashcard, Flashcards)


def add_flashcards():
    global current_id

    def menu():
        print('1. Add a new flashcard')
        print('2. Exit')

    while True:
        try:
            menu()
            str_added_option = input()
            option = int(str_added_option)
            if option == 2:
                break
            elif option == 1:
                while True:
                    question = input('Question:').strip()
                    if question:
                        break

                while True:
                    answer = input('Answer:').strip()
                    if answer:
                        break

                flashcard = Flashcard(current_id, answer, question, 1)
                current_id += 1
                session.add(flashcard)
                session.commit()
            else:
                print(f'{option} is not an option')
        except ValueError:
            print(f'{str_added_option} is not an option')


def get_flashcards():
    global current_session
    the_result_list = session.query(Flashcard).filter(Flashcard.box <= current_session).all()
    result = [Flashcard(res.id, res.answer, res.question, res.box) for res in the_result_list]

    current_session += 1
    if current_session > 3:
        current_session = 1

    return result


def delete_flashcard(flashcard_id):
    d = Flashcards.delete().where(Flashcards.c.id == flashcard_id)
    session.execute(d)
    session.commit()


def update_flashcard(the_flashcard):
    d = Flashcards.update(). \
        values(answer=the_flashcard.answer, question=the_flashcard.question,
               box=the_flashcard.box). \
        where(Flashcards.c.id == the_flashcard.id)
    session.execute(d)
    session.commit()


def practice_flashcards():
    flashcards = get_flashcards()

    if not flashcards:
        print('There is no flashcard to practice!')
    else:
        for the_flashcard in flashcards:
            print(f'Question: {the_flashcard.question}')
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')
            option = input()

            if option == 'y':
                print(f'Answer: {the_flashcard.answer}')
                print('press "y" if your answer is correct:')
                print('press "n" if your answer is wrong:')
                choice = input()
                if choice.strip().lower() == 'y':
                    the_flashcard.box = the_flashcard.box + 1
                    if the_flashcard.box > 2:
                        delete_flashcard(the_flashcard.id)
                    else:
                        update_flashcard(the_flashcard)
                elif choice.strip().lower() == 'n':
                    the_flashcard.box = 1
                    update_flashcard(the_flashcard)
                else:
                    print(f'{choice} is not an option')
            elif option == 'n':
                continue
            elif option == 'u':
                print('press "d" to delete the flashcard:')
                print('press "e" to edit the flashcard:')
                new_option = input()
                if new_option == 'd':
                    delete_flashcard(the_flashcard.id)
                elif new_option == 'e':
                    print(f'current question: {the_flashcard.question}')
                    the_flashcard.question = input('please write a new question:')

                    print(f'current answer: {the_flashcard.answer}')
                    the_flashcard.answer = input('please write a new answer:')

                    update_flashcard(the_flashcard)
            else:
                print(f'{option} is not an option')


def reset_flashcards():
    # quando for iniciar a execução deste programa, deve-se colocar
    # todos os boxes como igual a 1, para os flashcards que estejam
    # no banco de dados.
    pass


if __name__ == '__main__':
    reset_flashcards()

    while True:
        try:
            print('1. Add flashcards')
            print('2. Practice flashcards')
            print('3. Exit')
            str_option = input()
            main_option = int(str_option)

            if main_option == 3:
                print('Bye!')
                break
            elif main_option == 2:
                practice_flashcards()
            elif main_option == 1:
                add_flashcards()
            else:
                print(f'{main_option} is not an option')
        except ValueError:
            print(f'{str_option} is not an option')
