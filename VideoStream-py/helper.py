import subprocess
import os
import signal
class FF_helper:
    __process_list=[]
    flist=[]
    rtsp_url=''
    account=''
    password=''
    name=''
    ipadress=''
    rtmp_url=''
    __command=['ffmpeg',
    '-r','30',
    '-i',
    'dsds',
    '-vcodec','copy',
    '-acodec','copy',
    '-f','flv',
    ''
    ]
    def start_process(self):
        self.__command[4]=self.rtsp_url
        self.__command[11]='rtmp://127.0.0.1:9100/myapp/'+self.name
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
               # self.kill_child_processes(p)
                p.terminate()
                break

    #@staticmethod
    # def kill_child_processes(parent_pid, sig=signal.SIGILL):
        # try:
        #     p = psutil.Process(parent_pid)
        # except psutil.NoSuchProcess:
        #     return
        # child_pid = p.children(recursive=True)
        # for pid in child_pid:
        #     os.kill(pid.pid, sig)

    def end_processes(self):
        for p in self.__process_list:
            p.kill()
