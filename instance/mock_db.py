from flask_sqlalchemy import SQLAlchemy
from Application.models import User

def populate_db(db: SQLAlchemy):
    u = User(
        email='abc@gmail.com',
        name='Soham',
        password='soham@123'
    )
    db.session.add(u)
    db.session.commit()    
