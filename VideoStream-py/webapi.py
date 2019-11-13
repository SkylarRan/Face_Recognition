from domain import Video,Result,Camara,Stream
from helper import FF_helper
from flask import current_app
import socket
import json
import sys
class Camara_Api():

    __fhelper=FF_helper()

    def get(self,camara_id):
        result=Result()
        result.data=[]
        result.status=False
        result.message=""
        try:
            if camara_id<=0:
                result.message="camara doesn't exist"
                return result.result2dict() 
            Video.connect()
            v1=Video.get_or_none(Video.id==camara_id)
            Video.close()
            if not v1:
                result.message="camara doesn't exist"
                return result.result2dict()
            camara=self.video2camara(v1)
            result.data.append(camara.camara2dict())
            result.status=True
            return result.result2dict()
        except:
            current_app.logger.warning("Unexpected error:", sys.exc_info())
            result.message="Unexpected error has happened,please contact website administrator"
            return result.result2dict() 

    def delete(self,data):
        result=Result()
        result.data=[]
        result.status=False
        try:
            if not 'id' in data or int(data['id'])<=0 or not data['id']:
                result.message="Data error,id dosen't exist"
                return result.result2dict()
            Video.connect()
            v=Video.get(id=data['id'])
            Video.delete().where(Video.id==data['id']).execute()
            Video.close()
            self.__fhelper.name=v.name
            pid=0
            for f in self.__fhelper.flist:
                if f['name']==v.name:
                    pid=f['pid']
                    break
            self.__fhelper.end_process(pid)
            result.status=True
            return result.result2dict()
        except:
            current_app.logger.warning("Unexpected error:", sys.exc_info())
            result.message="Unexpected error has happened,please contact website administrator"
            return result.result2dict() 
        return result.result2dict()

    def add(self,data):
        result=Result()
        result.data=[]
        result.status=True
        if not 'url' in data or data['url']=='' or not data['url']:
            result.message="Data error,url dosen't exist"
            return result.result2dict()
        if not 'name' in data or data['name']=='' or not data['name']:
            result.message="Data error,name dosen't exist"
            return result.result2dict()
        if not 'location' in data or data['location']=='' or not data['location']:
            result.message="Data error,location dosen't exist"
            return result.result2dict()
        Video.connect()
        Video.create(camara_url=data['url'],name=data['name'],location=data['location'],camara_id=data['camara_id'],camara_pw=data['camara_pw'],remark=data['memo']
        ,stream_url='http://'+self.__fhelper.ipadress+':9001/live?port=9100&app=myapp&stream='+data['name'],
        rtmp_url='rtmp://'+self.__fhelper.ipadress+':9100/myapp/'+data['name'])
        Video.close()
        stream=Stream()
        stream.id=Video.get(name=data['name']).id
        stream.name=data['name']
        stream.url='http://'+self.__fhelper.ipadress+':9001/live?port=9100&app=myapp&stream='+data['name']
        stream.location=data['location']
        stream.rtmp='rtmp://'+self.__fhelper.ipadress+':9100/myapp/'+data['name']
        self.__fhelper.name=data['name']
        self.__fhelper.rtsp_url=data['url']
        self.__fhelper.start_process()
        result.data.append(stream.stream2dict())
        result.message=''
        result.status=True
        return result.result2dict()

    def edit(self,data):
        result=Result()
        result.data=[]
        result.status=False
        try:
            if not 'id' in data or int(data['id'])<=0 or not data['id']:
                result.message="Data error,url dosen't exist"
                return result.result2dict()
            if not 'url' in data or data['url']=='' or not data['url']:
                result.message="Data error,url dosen't exist"
                return result.result2dict()
            if not 'name' in data or data['name']=='' or not data['name']:
                result.message="Data error,name dosen't exist"
                return result.result2dict()
            if not 'location' in data or data['location']=='' or not data['location']:
                result.message="Data error,location dosen't exist"
                return result.result2dict()
            v1=Video.get(id=data['id'])
            if not v1:
                result.message="camara doesn't exist"
                return result.result2dict()
            if v1.name!=data['name'] :
                self.__fhelper.name=v1.name
                pid=0
                for f in self.__fhelper.flist:
                    if f['name']==v1.name:
                        pid=f['pid']
                        break
                self.__fhelper.end_process(pid)
                self.__fhelper.name=data['name']
                self.__fhelper.rtsp_url=data['url']
                self.__fhelper.start_process()
            v1.name=data['name']
            v1.camara_url=data['url']
            v1.location=data['location']
            v1.camara_id=data['camara_id']
            v1.camara_pw=data['camara_pw']
            v1.remark=data['memo']
            v1.stream_url='http://'+self.__fhelper.ipadress+':9001/live?port=9100&app=myapp&stream='+data['name']
            v1.rtmp_url='rtmp://'+self.__fhelper.ipadress+':9100/myapp/'+data['name']
            v1.save()
            stream=self.video2stream(v1)
            result.data.append(stream.stream2dict())
            result.message=""
            result.status=True
            return result.result2dict()
        except:
            current_app.logger.warning("Unexpected error:", sys.exc_info())
            result.message="Unexpected error has happened,please contact website administrator"
            return result.result2dict()

    def getlist(self):
        result=Result()
        result.data=[]
        result.status=False
        result.message=""
        try:
            Video.connect()
            vlist=Video.select()
            Video.close()
            if not vlist:
                result.message="camara doesn't exist"
                return result.result2dict()
            for v1 in vlist:
                camara=self.video2camara(v1)
                result.data.append(camara.camara2dict())
            result.status=True
            return result.result2dict()
        except:
            current_app.logger.warning("Unexpected error:", sys.exc_info())
            result.message="Unexpected error has happened,please contact website administrator"
            return result.result2dict() 

    def getstreamlist(self):
        result=Result()
        result.data=[]
        result.status=False
        result.message=""
        try:
            Video.connect()
            vlist=Video.select()
            Video.close()
            if not vlist:
                result.message="stream doesn't exist"
                return result.result2dict()
            for v1 in vlist:
                stream=self.video2stream(v1)
                result.data.append(stream.stream2dict())
            result.status=True
            return result.result2dict()
        except:
            current_app.logger.warning("Unexpected error:", sys.exc_info())
            result.message="Unexpected error has happened,please contact website administrator"
            return result.result2dict() 

    def startallstream(self):
        vlist=Video.select()
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(('8.8.8.8',80))
            self.__fhelper.ipadress=s.getsockname()[0]
        finally:
            s.close()
        for v in vlist:
            self.__fhelper.name=v.name
            self.__fhelper.rtsp_url=v.camara_url
            self.__fhelper.start_process()
       
    @staticmethod
    def video2camara(video):
        camara=Camara()
        camara.id=video.id
        camara.location=video.location
        camara.memo=video.remark
        camara.name=video.name
        camara.url=video.camara_url
        return camara
    
    @staticmethod
    def video2stream(video):
        stream=Stream()
        stream.rtmp=video.rtmp_url
        stream.url=video.stream_url
        stream.location=video.location
        stream.name=video.name
        stream.id=video.id
        return stream


   