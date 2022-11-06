class UserLogin:
    '''Класс с методами для получение информации о статусе авторизации пользователя'''
    def fromDB(self, user_id, Users):
        '''Извлечение пользователя из бд'''
        self.__user = Users.query.filter(Users.id == user_id).first()
        return self
 
    def create(self, user):
        '''Создание пользователя (для его обнаружения приложением)'''
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        '''Получение id пользователя'''
        return str(self.__user.id)

    def verifyExt(self, filename):
        '''Доступные для загрузки виды изображений'''
        legal = ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG", "bmp", "BMP"]
        ext = filename.rsplit('.', 1)[1]
        if ext in legal: 
            return True
        return False