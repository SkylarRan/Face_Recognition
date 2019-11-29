from peewee import MySQLDatabase,CharField,Model

database = MySQLDatabase('face_recognition', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'localhost', 'user': 'root', 'password': 'root'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        pass
        database = database


class Blacklist(BaseModel):
    id = CharField(primary_key=True)
    image = CharField()
    memo = CharField(null=True)
    name = CharField()

    class Meta:
        table_name = 'blacklist'


class Record(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    frame = CharField()
    recognizedAt = CharField()
    camera = CharField()
    cam_id = CharField()
    location = CharField()

    class Meta:
        table_name = 'record'
