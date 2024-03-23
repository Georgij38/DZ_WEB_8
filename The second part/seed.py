from faker import Faker

from models import Contact

faker = Faker()


def populate_database(num_records):
    for _ in range(num_records):
        full_name = faker.name()
        birth_date = faker.date_of_birth()
        email = faker.email()
        email_sent = False


        contact = Contact(
            full_name=full_name,
            birth_date=birth_date,
            email=email,
            email_sent=email_sent
        )
        contact.save()


if __name__ == '__main__':
    populate_database(100)
