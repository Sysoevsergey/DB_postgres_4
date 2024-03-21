import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:admin@localhost:5432/DBHomework_4'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name="Пушкин Александр Сергеевич")
publisher1_book1 = Book(title="Евгений Онегин", id_publisher=1)
publisher1_book2 = Book(title="Сказка о царе Салтане", id_publisher=1)
publisher1_book3 = Book(title="Руслан и Людмила", id_publisher=1)

publisher2 = Publisher(name="Булгаков Михаил Афанасьевич")
publisher2_book1 = Book(title="Белая гвардия", id_publisher=2)
publisher2_book2 = Book(title="Идиот", id_publisher=2)
publisher2_book3 = Book(title="Братья Карамазовы", id_publisher=2)

publisher3 = Publisher(name="Толстой Лев Николаевич")
publisher3_book1 = Book(title="Война и мир", id_publisher=3)
publisher3_book2 = Book(title="Отцы и дети", id_publisher=3)
publisher3_book3 = Book(title="Анна Каренина", id_publisher=3)

shop1 = Shop(name="Буквоед")
shop2 = Shop(name="Лабиринт")
shop3 = Shop(name="Книжный дом")

sale1 = Sale(price=590, date_sale="2022-01-01", id_stock=1, count=1)
sale2 = Sale(price=700, date_sale="2022-02-01", id_stock=2, count=1)
sale3 = Sale(price=600, date_sale="2022-05-01", id_stock=3, count=1)
sale4 = Sale(price=1200, date_sale="2022-07-01", id_stock=4, count=1)
sale5 = Sale(price=800, date_sale="2022-10-01", id_stock=5, count=1)

stock1 = Stock(id_book=1, id_shop=1, count=1)
stock2 = Stock(id_book=4, id_shop=2, count=1)
stock3 = Stock(id_book=7, id_shop=1, count=1)
stock4 = Stock(id_book=3, id_shop=2, count=1)
stock5 = Stock(id_book=8, id_shop=3, count=1)

session.add_all([publisher1, publisher2, publisher3])
session.add_all([publisher1_book1, publisher1_book2, publisher1_book3,
                publisher2_book1, publisher2_book2, publisher2_book3,
                publisher3_book1, publisher3_book2, publisher3_book3]
                )
session.add_all([shop1, shop2, shop3])
session.add_all([sale1, sale2, sale3, sale4, sale5])
session.add_all([stock1, stock2, stock3, stock4, stock5])

session.commit()

publisher_input = input("Введите имя или id издателя:")

try:
    publisher_id = int(publisher_input)
    publisher = (Session().query(Publisher).filter(Publisher.id == publisher_id).first())
except ValueError:
    publisher = (Session().query(Publisher).filter(Publisher.name.like(f'%{publisher_input}%')).first())

if publisher is not None:
    sales = (
        Session()
        .query(Sale)
        .join(Stock)
        .join(Stock.shop)
        .join(Book)
        .join(Publisher)
        .filter(Publisher.id == publisher.id)
        .order_by(Sale.date_sale)
        .all()
    )

else:
    print("Издатель не найден")

for sale in sales:
    print(f'{sale.stock.book.title:^25}|{sale.stock.shop.name:^10}|{sale.price:^10}|{sale.date_sale}')

session.close()
