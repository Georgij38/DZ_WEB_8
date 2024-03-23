from mongoengine import connect, Document, StringField, BooleanField, DateTimeField

from pymongo.mongo_client import MongoClient

connect(
    db='DZ_8',
    host="mongodb+srv://user:567234@cluster0.qpllrc8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",  # наприклад, 'mongodb+srv://<username>:<password>@your_cluster_url/your_database_name?retryWrites=true&w=majority'
    username='user',
    password='567234',
    authentication_source='admin'  # аутентифікація в адміністративній базі даних
)

uri = "mongodb+srv://user:567234@cluster0.qpllrc8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to contacts!")
except Exception as e:
    print(e)


class Contact(Document):
    full_name = StringField(required=True, unique=True)
    birth_date = DateTimeField()
    email = StringField(required=True, unique=True)
    email_sent = BooleanField(default=False)
    meta = {'collection': 'contacts'}
