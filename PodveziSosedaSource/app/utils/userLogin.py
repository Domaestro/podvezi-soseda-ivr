class UserLogin:
    def fromDB(self, user_id, Users):
        self.__user = Users.query.filter(Users.id == user_id).first()
        return self
 
    def create(self, user):
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.__user.id)

    def verifyExt(self, filename):
        legal = ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG", "bmp", "BMP"]
        ext = filename.rsplit('.', 1)[1]
        if ext in legal: 
            return True
        return False