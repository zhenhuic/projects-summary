# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# inOut: utils.py
# time: 2019/12/23 14:32
from Database.connectAndClose import *
from inOut.menu import Menu


class Utils:

    def selectSingleTimeSpendBYName(self, name):
        """
        查询今日的报警消耗时常
        """
        conn, cursor = ConnectAndClose().database_connect()
        sql = "select BQ, BZ from s7300warning where BZ != '' and TO_DAYS(NOW()) - TO_DAYS(SJ) = 0 and BQ = '" + str(
            name) + "'order by SJ asc;"
        cursor.execute(sql)
        selectAll = cursor.fetchall()
        listE = []
        for each in selectAll:
            listE.append(int(each[1].split('分钟')[0]))
        cost = 0
        if len(listE) != 0:
            temp = listE[0]
            front = 0
            rear = 0
            for eachE in listE[1:]:
                if eachE >= temp:
                    temp = eachE
                    rear += 1
                else:
                    cost += (rear - front) * 5
                    front = rear + 1
                    rear = front
                    temp = eachE
            if rear != front:
                cost += (rear - front) * 5
        return cost

    def selectSingleFrequencyAndTimeCostByName(self, name):
        """
        第几天 + 查询近七天的报警次数 + 每天的报警时长总和
        """
        conn, cursor = ConnectAndClose().database_connect()
        sql = "select BZ , TO_DAYS(NOW()) - TO_DAYS(SJ) from s7300warning where BZ != '' and TO_DAYS(NOW()) - TO_DAYS(SJ) between 0 and 6 and BQ='" + str(
            name) + "' ORDER BY TO_DAYS(NOW()) - TO_DAYS(SJ) DESC"
        cursor.execute(sql)
        # 结果：（时间， 距离天数）
        selectAll = cursor.fetchall()
        listAll = []
        for each in selectAll:
            listAll.append([int(each[1]), int(each[0].split('分钟')[0])])

        resultList = []
        for i in range(0, 7):
            count = 0
            cost = 0
            listE = []
            for each in listAll:
                if each[0] == i:
                    listE.append(each[1])
            if len(listE) != 0:
                front = 0
                rear = 1
                temp = listE[0]
                for eachE in listE[1:]:
                    if eachE >= temp:
                        temp = eachE
                        rear += 1
                    else:
                        cost += (rear - front) * 5
                        front = rear + 1
                        rear = front
                        count += 1
                        temp = eachE
                if front != rear:
                    cost += (rear - front) * 5
                    count += 1
            resultList.insert(0, [i, count, cost])
        return resultList

    def selectMultipleFrequencyOfToday(self, name):
        conn, cursor = ConnectAndClose().database_connect()
        menu = Menu()
        filePath = "menuFile/" + str(name) + ".txt"  # ../menuFile/OP30.txt
        # filePath = "menuFile/" + str(name) + ".txt"  # ../menuFile/OP30.txt
        searchList = menu.readerTitle(filePath)
        name = ""
        for x in searchList:
            name += '\'' + x + '\''
            name += ","
        name = name[:-1]
        sql = "select BQ, COUNT(*) from s7300warning where BJ='报警' and TO_DAYS(NOW()) - TO_DAYS(SJ) = 0 and BQ in (" + str(name) + ") GROUP BY BQ ORDER BY BQ ASC"
        cursor.execute(sql)
        selectAll = cursor.fetchall()
        resultList = []
        for each in selectAll:
            resultList.append([each[0], each[1]])
        return resultList

    def selectMultipleFrequencyOfWeek(self, name):
        conn, cursor = ConnectAndClose().database_connect()
        menu = Menu()
        filePath = "menuFile/" + str(name) + ".txt"  # ../menuFile/OP30.txt
        # filePath = "menuFile/" + str(name) + ".txt"  # ../menuFile/OP30.txt
        searchList = menu.readerTitle(filePath)
        name = ""
        for x in searchList:
            name += '\'' + x + '\''
            name += ","
        name = name[:-1]
        sql = "select BQ, a.d , count(*) FROM(select BQ, TO_DAYS(NOW()) - TO_DAYS(SJ) as d from s7300warning WHERE BJ='报警' and  TO_DAYS(NOW()) - TO_DAYS(SJ) between 0 and 7 and BQ in (" + str(name) + ")ORDER BY BQ ASC, TO_DAYS(NOW()) - TO_DAYS(SJ) ASC) as a GROUP BY BQ, a.d ORDER BY BQ ASC, d ASC;"
        cursor.execute(sql)
        selectAll = cursor.fetchall()
        # d = {name:[1， 12， 12， 12，12，0，0]}
        resultDict = {}
        name = []
        for each in selectAll:
            if each[0] not in name:
                name.append(each[0])
        for eachName in name:
            listOne = []
            for i in range(0, 7):
                count = 0
                for each in selectAll:
                    if eachName == each[0]:
                        if each[1] == 6 - i:
                            count = each[2]
                listOne.append(count)
            resultDict[eachName] = listOne
        return resultDict


if __name__ == '__main__':
    utils = Utils()
    utils.selectSingleFrequencyAndTimeCostByName('OP30厚度检测气缸伸出未到位')
