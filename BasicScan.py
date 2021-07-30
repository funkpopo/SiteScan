import hashlib
import aiohttp
import asyncio
from multiprocessing import Process, Queue, Manager


class Dirscan():
    def __init__(self, target):
        self.target = target
        self.targetmd5 = ''
        self.allqueue = Queue()
        self.urlpath = r'./dictionary/php.txt'  # 字典文件
        self.Ansdomain = Manager().list()
        self.processnum = 8  # 进程数
        self.alldictnum = 0

    def dicturl(self):
        with open(self.urlpath, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                self.allqueue.put(self.target + '/' + i.strip('\n'))
            self.alldictnum = self.allqueue.qsize()

    async def main(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                htmlstr = await res.text()
                md5hash = hashlib.md5(htmlstr.encode("utf8"))
                md5 = md5hash.hexdigest()
                return res.status, md5

    def dirscan(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.main(self.target))
        status, self.targetmd5 = loop.run_until_complete(task)

        while self.allqueue.empty() != True:
            tmp = self.allqueue.get()
            task = loop.create_task(self.main(tmp))
            try:
                print('\r' + str(int(self.alldictnum) - int(self.allqueue.qsize())) + '/' + str(int(self.alldictnum)),
                      end='')
                status, mad5 = loop.run_until_complete(task)
                # print('bad : '+tmp)
                if ((status == 200) and (mad5 != self.targetmd5)):
                    print('OK : ' + tmp)
                    self.Ansdomain.append(tmp)
            except Exception as e:
                print(e)

    def SetProcess(self):
        self.dicturl()
        allprocess = []
        for i in range(0, self.processnum):
            p = Process(target=self.dirscan, args=())
            p.start()
            allprocess.append(p)
        for i in allprocess:
            i.join()
        for i in allprocess:
            i.close()


if __name__ == '__main__':
    obj = Dirscan('https://www.cyberis.fun')
    obj.SetProcess()
