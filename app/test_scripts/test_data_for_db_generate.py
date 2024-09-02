from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import random
import string

# Импортируем класс User
from app.models import Recipient, Donor, Base


abc = string.ascii_lowercase

def generate_base_user_data():
    first_names = ["Иван", "Петр", "Сергей", "Александр", "Дмитрий", "Николай", "Михаил", "Владимир", "Андрей",
                   "Алексей"]
    first_name = random.choice(first_names)
    phone = f"+7{random.randint(100000000, 999999999)}"
    profile_picture = ':)'

    return {
        'first_name': first_name,
        'phone': phone,
        'profile_picture': profile_picture
    }

def generate_recipient_user_data():

    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Попов", "Лебедев", "Кузьмин", "Соколов", "Родионов", "Павлов"]
    patronymics = ['Иванович', 'Петрович', 'Сергеевич', 'Алексеевич', 'Дмитриевич']
    addresses = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
    emails = ['user1@example.com', 'user2@example.com', 'user3@example.com', 'user4@example.com', 'user5@example.com']
    genders = ['мужской', 'женский']


    last_name = random.choice(last_names)
    patronymic = random.choice(patronymics)
    address = random.choice(addresses)
    email = random.choice(abc) + random.choice(emails)
    gender = random.choice(genders)
    birth_date = date.today() - timedelta(days=random.randint(365*18, 365*65))

    return {
        'last_name': last_name,
        'patronymic': patronymic,
        'address': address,
        'email': email,
        'gender': gender,
        'birth_date': birth_date
    }

def generate_users(n):
    k = 0
    while k < n:
        try:
            data = generate_base_user_data()
            if random.random() < 0.5:
                data1 = generate_recipient_user_data()
                user = Recipient(**data, **data1)
            else:
                user = Donor(**data)
            user.set_pin_code('1234')
            session.add(user)
            k += 1
        except Exception as ex:
            print(ex)
            continue
        else:
            print('ok', k)







if __name__ == '__main__':
    engine = create_engine('postgresql://gleb:postgres@localhost:5432/servatorium_test_db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    generate_users(30)

    session.commit()
    session.close()
