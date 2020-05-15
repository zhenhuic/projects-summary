# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 9:32 AM
# @Author  : sichengli
# @FileName: menu.py
# @Software: PyCharm

class Menu:

    def readerTitle(self, path):

        titleList = []
        file = open(path, 'r', encoding='utf-8')
        line = file.readline()
        while line != "":
            line = line.replace("\n", "")
            titleList.append(line)
            line = file.readline()
        return titleList


    def writerTile(self, path, name):
        titleList = self.readerTitle(path)
        if name not in titleList:
            file = open(path, "a", encoding='utf-8')
            file.write(name + "\n")

    def delete(self, path, name):
        titleList = self.readerTitle(path)
        file = open(path, "w", encoding='utf-8')
        for x in titleList:
            if x != name:
                file.write(x + "\n")


if __name__ == '__main__':
    menu = Menu()
    menu.readerTitle("../menuFile/变频器.txt")

