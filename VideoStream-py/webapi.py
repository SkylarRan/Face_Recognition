import json
import socket
import sys
import uuid

from flask import current_app

from domain import Camera, Result, Stream, Video
from helper import FF_helper


class Camera_Api():

    __fhelper=FF_helper()

    def get(self,camera_id):
        result=Result()
        result.data=[]
        result.status=False
        result.message=""
        try:
            if camera_id=='':
                result.message="camera doesn't exist"
                return result.result2dict() 
            Video.connect()
            v1=Video.get_or_none(Video.id==camera_id)
            Video.close()
            if not v1:
                result.message="camera doesn't exist"
                return result.result2dict()
            camera=self.video2camera(v1)
            result.data.append(camera.camera2dict())
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
            if not 'id' in data or not data['id']:
                result.message="Data error,id dosen't exist"
                return result.result2dict()
            Video.connect()
            v=Video.get(id=data['id'])
            Video.delete().where(Video.id==data['id']).execute()
            Video.close()
            self.__fhelper.name=v.id
            pid=0
            for f in self.__fhelper.flist:
                if f['name']==v.id:
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
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        Video.connect()
        Video.create(id=suid,camera_url=data['url'],name=data['name'],location=data['location'],camera_id=data['camera_id'],camera_pw=data['camera_pw'],remark=data['memo']
        ,stream_url='http://'+self.__fhelper.ipadress+':9001/live?port=9100&app=myapp&stream='+suid,
        rtmp_url='rtmp://'+self.__fhelper.ipadress+':9100/myapp/'+suid)
        Video.close()
        stream=Stream()
        stream.id=suid
        stream.name=data['name']
        stream.url='http://'+self.__fhelper.ipadress+':9001/live?port=9100&app=myapp&stream='+suid
        stream.location=data['location']
        stream.rtmp='rtmp://'+self.__fhelper.ipadress+':9100/myapp/'+suid
        self.__fhelper.name=suid
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
            if not 'id' in data  or not data['id']:
                result.message="Data error,id dosen't exist"
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
                result.message="camera doesn't exist"
                return result.result2dict()
            if v1.camera_url!=data['url']:
                self.__fhelper.name=v1.id
                pid=0
                for f in self.__fhelper.flist:
                    if f['name']==v1.id:
                        pid=f['pid']
                        break
                self.__fhelper.end_process(pid)
                self.__fhelper.name=v1.id
                self.__fhelper.rtsp_url=data['url']
                self.__fhelper.start_process()
            v1.name=data['name']
            v1.camera_url=data['url']
            v1.location=data['location']
            v1.camera_id=data['camera_id']
            v1.camera_pw=data['camera_pw']
            v1.remark=data['memo']
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
                result.message="camera doesn't exist"
                return result.result2dict()
            for v1 in vlist:
                camera=self.video2camera(v1)
                result.data.append(camera.camera2dict())
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
            self.__fhelper.name=v.id
            self.__fhelper.rtsp_url=v.camera_url
            self.__fhelper.start_process()
       
    @staticmethod
    def video2camera(video):
        camera=Camera()
        camera.id=video.id
        camera.location=video.location
        camera.memo=video.remark
        camera.name=video.name
        camera.url=video.camera_url
        return camera
    
    @staticmethod
    def video2stream(video):
        stream=Stream()
        stream.rtmp=video.rtmp_url
        stream.url=video.stream_url
        stream.location=video.location
        stream.name=video.name
        stream.id=video.id
        return stream
