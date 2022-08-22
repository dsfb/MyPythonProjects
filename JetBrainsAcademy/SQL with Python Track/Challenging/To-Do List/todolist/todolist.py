import datetime
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Date, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, Sequence('task_seq'), primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return "{}. {}".format(self.id, self.task)


class Program(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(bind=self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.task_list = None

    def show_today_tasks(self):
        print()
        today = datetime.today()
        print('Today {} {}:'.format(today.day,
                                    today.strftime('%b')))
        self.task_list = self.session. \
            query(Task).filter(Task.deadline ==
                               today.date()).all()
        if not self.task_list:
            print('Nothing to do!')
        else:
            for task in self.task_list:
                print(task)

    def show_week_tasks(self):
        today = datetime.today()
        for i in range(7):
            day = today + timedelta(days=i)
            print()
            print("{} {} {}:".format(day.strftime('%A'),
                                     day.day,
                                     day.strftime('%b')))
            self.task_list = self.session. \
                query(Task).filter(Task.deadline ==
                                   day.date()).all()

            if not self.task_list:
                print('Nothing to do!')
            else:
                for task in self.task_list:
                    print(task)

    def show_missed_tasks(self):
        print()
        today = datetime.today()
        self.task_list = self.session. \
            query(Task).filter(Task.deadline <
                               today.date()). \
            all()
        if not self.task_list:
            print('All tasks have been completed!')
        else:
            print('Missed tasks:')
            for task in self.task_list:
                day = task.deadline
                print('{}. {} {}'.format(task,
                                         day.day,
                                         day.strftime('%b')))

    def delete_task(self):
        print()
        self.task_list = self.session. \
            query(Task).order_by(Task.deadline). \
            all()
        if not self.task_list:
            print('Nothing to delete')
        else:
            print('Choose the number of the task you want to delete:')
            for task in self.task_list:
                day = task.deadline
                print('{}. {} {}'.format(task,
                                         day.day,
                                         day.strftime('%b')))
            choice = int(input())
            self.session.query(Task).filter(Task.id == choice). \
                delete()
            self.session.commit()
            print('The task has been deleted!')

    def show_all_tasks(self):
        print()
        self.task_list = self.session. \
            query(Task).order_by(Task.deadline). \
            all()
        print('All tasks:')
        if not self.task_list:
            print('Nothing to do!')
        else:
            for task in self.task_list:
                day = task.deadline
                print('{}. {} {}'.format(task,
                                         day.day,
                                         day.strftime('%b')))

    def add_task(self):
        print()
        print('Enter a task')
        todo = input()
        print('Enter a deadline')
        deadline = input()
        deadline = datetime.strptime(deadline,
                                     "%Y-%m-%d")
        new_task = Task(task=todo,
                        deadline=deadline)
        self.session.add(new_task)
        self.session.commit()
        print('The task has been added!')

    def process(self):
        while True:
            print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add a task
6) Delete a task
0) Exit''')

            choice = int(input())

            if choice == 1:
                self.show_today_tasks()
            elif choice == 2:
                self.show_week_tasks()
            elif choice == 3:
                self.show_all_tasks()
            elif choice == 4:
                self.show_missed_tasks()
            elif choice == 5:
                self.add_task()
            elif choice == 6:
                self.delete_task()
            elif choice == 0:
                break

            print()

        print('Bye!')
        print()
        print('Bye!')


p = Program()
p.process()
