# -*- coding:utf-8 -*-

class Dict(dict):
    def __repr__(self):
        str=u""
        for name,num in self.items():
            str=str+u"%sx%d "%( name , num)
        return str.encode("utf-8")
