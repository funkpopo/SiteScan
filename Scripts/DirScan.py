import hashlib
import aiohttp
import asyncio
import datetime
import os
from multiprocessing import Process, Queue, Manager


class Dirscan:
    def __init__(self, target):
        self.target = target
        self.targetmd5 = ''
        self.allqueue = Queue()
        # 字典文件
        # self.urlpath = r'../dictionary/asp.txt'
        # self.urlpath = r'../dictionary/aspx.txt'
        # self.urlpath = r'../dictionary/dir.txt'
        # self.urlpath = r'../dictionary/fck.txt'
        # self.urlpath = r'../dictionary/jsp.txt'
        # self.urlpath = r'../dictionary/mdb.txt'
        # self.urlpath = r'../dictionary/php.txt'
        # self.urlpath = r'../dictionary/shell.txt'
        # self.urlpath = r'../dictionary/top.txt'
        # self.urlpath = r'../dictionary/fingerprints.txt'
        # self.urlpath = r'../dictionary/differ-kinds.txt'
        # self.urlpath = r'../dictionary/critical.txt'
        # self.urlpath = r'../dictionary/backups.txt'
        self.urlpath = r'../dictionary/php.txt'
        self.Ansdomain = Manager().list()
        # 进程数
        self.processnum = 8
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

        while not self.allqueue.empty():
            tmp = self.allqueue.get()
            task = loop.create_task(self.main(tmp))
            try:
                print('\r' + str(int(self.alldictnum) - int(self.allqueue.qsize())) + '/' + str(int(self.alldictnum)),
                      end='')
                status, mad5 = loop.run_until_complete(task)
                # print('bad : '+tmp)
                if (status == 200) and (mad5 != self.targetmd5):
                    print(' OK : ' + tmp)
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
    # 需输入完整域名
    print("Input the domain name: ")
    target = input()
    obj = Dirscan(target)
    obj.SetProcess()
