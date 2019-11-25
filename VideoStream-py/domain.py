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
    id=peewee.CharField()
    camera_url=peewee.CharField()
    name=peewee.CharField()
    location=peewee.CharField()
    camera_id=peewee.CharField()
    camera_pw=peewee.CharField()
    remark=peewee.TextField()
    stream_url=peewee.CharField()
    rtmp_url=peewee.CharField()
    

class Camera:
    id=0
    url=""
    name=""
    location=""
    camera_id=""
    camera_pw=""
    memo=""

    def camera2dict(self):
        return {
        'id':self.id,
        'url':self.url,
        'name':self.name,
        'location':self.location,
        'camera_id':self.camera_id,
        'camera_pw':self.camera_pw,
        'memo':self.memo
        }


class Stream:
    id=0
    url=''
    name=''
    location=''
    rtmp=''
    def stream2dict(self):
        return {
        'id':self.id,
        'url':self.url,
        'name':self.name,
        'location':self.location,
        'rtmp':self.rtmp
        }


class Result:    
    data=[]
    message=''
    status=True

    def result2dict(self):
        return {
        'data':self.data,
        'status':self.status,
        'message':self.message
        }

