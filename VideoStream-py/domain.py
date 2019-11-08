import peewee
import sqlite3
DATABASE = 'Nvr.db3'
database =peewee.SqliteDatabase(DATABASE)
class BaseModel(peewee.Model):
    class Meta:
        database = database
    @staticmethod
    def connect():
        database.connect()
    @staticmethod
    def close():
        database.close()

class Video(BaseModel):
    id=peewee.IntegerField()
    camara_url=peewee.CharField()
    name=peewee.CharField()
    location=peewee.CharField()
    camara_id=peewee.CharField()
    camara_pw=peewee.CharField()
    remark=peewee.TextField()
    stream_url=peewee.CharField()

    

class Camara:
    id=0
    url=""
    name=""
    location=""
    camara_id=""
    camara_pw=""
    memo=""

    def camara2dict(self):
        return {
        'id':self.id,
        'url':self.url,
        'name':self.name,
        'location':self.location,
        'camara_id':self.camara_id,
        'camara_pw':self.camara_pw,
        'memo':self.memo
        }


class Stream:
    url=""
    name=""
    location=""

    def stream2dict(self):
        return {
        'url':self.url,
        'name':self.name,
        'location':self.location,
        }


class Result:    
    data=[]
    message=""
    status=True

    def result2dict(self):
        return {
        'data':self.data,
        'status':self.status,
        'message':self.message
        }

