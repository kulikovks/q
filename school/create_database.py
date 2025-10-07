from faker import Faker

from models.database import create_db, Session
from models.lesson import Lesson
from models.student import Student
from models.group import Group

# для создания чистой таблицы (без ложных данных)
# передаем False
def create_database(load_fake_data: bool = True):
    create_db()
    if load_fake_data:
        _load_fake_data(Session())
        
    
def _load_fake_data(session: Session):
    lessons_names = ['Математика','Программирование',
                    'Философия','Линал','Матан',
                    'Статистика','Физкультура']
    group1 = Group(group_name='1-МДА-7')
    group2 = Group(group_name='1-МДА-9')
    group3 = Group(group_name='2-ФЛХ-5')
    group4 = Group(group_name='3-ВМК')
    session.add(group1)
    session.add(group2)
    session.add(group3)
    session.add(group4)
    for key, it in enumerate(lessons_names):
        lesson = Lesson(lesson_title=it)
        lesson.groups.append(group1)
        if key % 2 == 0:
            lesson.groups.append(group2)
        if key % 2 == 0 and key % 3 == 1:
            lesson.groups.append(group3)
        if key % 3 == 0 and key % 2 == 1:
            lesson.groups.append(group4)
        session.add(lesson)
        
    faker = Faker('ru_RU')
    group_list = [group1, group2, group3, group4]
    session.commit()
    
    for _ in range(500):
        full_name = faker.name_nonbinary().split(' ')
        age = faker.random.randint(16, 25)
        address = faker.address()
        group = faker.random.choice(group_list)
        student = Student(full_name, age, address, group.id)
        session.add(student)
        
    session.commit()
    session.close()