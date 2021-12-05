import json
from sqlalchemy.ext.declarative import DeclarativeMeta
import datetime

class AlchemyEncoder(json.JSONEncoder):
    '''
    Для преобразования объекта таблицы в json формат
    Основа взята с https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    '''

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, datetime.date):
                        json.dumps(data.strftime(r"%d.%m.%Y"))
                        fields[field] = data.strftime(r"%d.%m.%Y")

                    elif isinstance(data, datetime.time):
                        json.dumps(data.strftime(r"%H:%M"))
                        fields[field] = data.strftime(r"%H:%M")

                    else:
                        json.dumps(data)
                        fields[field] = data
                    
                except TypeError:
                    fields[field] = None
            
            return fields

        return json.JSONEncoder.default(self, obj)