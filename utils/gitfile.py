from git import Repo
import os

class Gitclass(object):

    def __init__(self,name,url):
        self.path = os.path.join('/update/git/',name)
        self.is_dir(url)

    #判断是否为git文件
    def is_dir(self,url):
        #如果项目文件不存在的时候创建一个
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        path = os.path.join(self.path,".git")
        if os.path.isdir(path):
            return True
        else:
            Repo.clone_from(url,self.path)
        self.repo = Repo(self.path)