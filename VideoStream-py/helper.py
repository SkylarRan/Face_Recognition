import subprocess
class FF_helper:
    __process_list=[]
    flist=[]
    rtsp_url=''
    account=''
    password=''
    name=''
    __command=['ffmpeg',
    '-i',
    'dsds',
    '-vcodec','libx264',
    '-acodec','aac',
    '-f','flv',
    'rtmp://127.0.0.1:9100/myapp/'
    ]
    def start_process(self):
        self.__command[2]=self.rtsp_url
        self.__command[9]= 'rtmp://127.0.0.1:9100/myapp/'+self.name
        strmsg=''
        for str in self.__command:
                strmsg+=str+' '
        print(strmsg)
        child = subprocess.Popen(self.__command)
        self.__process_list.append(child)
        self.flist.append({'pid':child.pid,'name':self.name})
    def end_process(self,pid):
        for p in self.__process_list:
            if p.pid==pid:
                p.terminate()
                break
    def end_processes(self):
        for p in self.__process_list:
            p.kill()
