from .database import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # Уникальный id
    email = db.Column(db.String(50), unique=True) # Почта пользователя максимальной длиной 50 символов, должна быть уникальной
    psw = db.Column(db.String(500), nullable=False) # Пароль максимально 500 символов тк он хэшируется, не может быть пустым
    first_name = db.Column(db.String(15))
    second_name = db.Column(db.String(15))
    phoneNum = db.Column(db.String(18), unique=True) # Телефон пользователя максимальной длиной 18 символов, должна быть уникальной
    confirmed = db.Column(db.Boolean, default=False) # Колонка, говорящая, подтвердил ли пользователь свой email

    def __repr__(self):     
        return f"<users {self.id}>"


class Profiles(db.Model):
    __tablename__ = 'profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    description = db.Column(db.Text, nullable=True)
    home_address = db.Column(db.String(200), nullable=True)
    home_latitude = db.Column(db.Float, nullable=True)
    home_longitude = db.Column(db.Float, nullable=True)
 
    def __repr__(self):
        return f"<profiles {self.id}>"


class Trips(db.Model):
    __tablename__ = 'trips'
    trip_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer)
    passengers_ids = db.Column(db.ARRAY(db.Integer))
    max_passengers_amount = db.Column(db.Integer, default=2)

    from_address = db.Column(db.String)    
    from_latitude = db.Column(db.Float, nullable=True)
    from_longitude = db.Column(db.Float, nullable=True)

    to_address = db.Column(db.String)
    to_latitude = db.Column(db.Float, nullable=True)
    to_longitude = db.Column(db.Float, nullable=True)

    trip_date = db.Column(db.Date)
    trip_time = db.Column(db.Time)