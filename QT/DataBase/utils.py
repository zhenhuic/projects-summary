# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: utils.py
# time: 2019/12/23 14:32
from DataBase.connectAndClose import *


class Utils:

    def selectSingleFrequencyAndTimeCostByName(self, name):
        """
        第几天 + 查询近七天的报警次数 + 每天的报警时长总和
        """
         # """
        # 查询近七天的报警次数
        # """
        # conn, cursor = ConnectAndClose().database_connect()
        # sql = "select a.d,count(*) from (select TO_DAYS(NOW()) - TO_DAYS(SJ) as d from s7300warning where BQ = '"+str(name)+"' and BJ='报警' and TO_DAYS(NOW()) - TO_DAYS(SJ) < 7) as a group by a.d order by a.d ASC"
        # cursor.execute(sql)
        # frequencyList = []
        # for i in range(1, 8):
        #     for each in cursor.fetchall():
        #         if each[0] == i:
        #             frequencyList.append(each[1])
        #         else:
        #             frequencyList.append(0)
        # ConnectAndClose().database_close(conn, cursor)
        conn, cursor = ConnectAndClose().database_connect()
        sql = "select BZ , TO_DAYS(NOW()) - TO_DAYS(SJ) from s7300warning where BZ != '' and TO_DAYS(NOW()) - TO_DAYS(SJ) < 7 and BQ='" + str(name) + "' ORDER BY TO_DAYS(NOW()) - TO_DAYS(SJ) ASC"
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
                for eachE in listE:
                    if listE.index(eachE) - 1 < 0:
                        front = 0
                    else:
                        front = listE[listE.index(eachE) - 1]
                    if listE.index(eachE) + 1 > len(listE) - 1:
                        behind = 0
                    else:
                        behind = listE[listE.index(eachE) + 1]
                    if eachE >= front and eachE >= behind:
                        count += 1
                        cost += eachE
            resultList.append([i, count, cost])
        return resultList

    def selectSingleTimeSpendBYName(self, name):
        """
        查询今日的报警消耗时常
        """
        conn, cursor = ConnectAndClose().database_connect()
        sql = "select BQ, BZ from s7300warning where BZ != '' and TO_DAYS(NOW()) - TO_DAYS(SJ) = 0 and BQ = '" + str(name) + "'order by SJ asc;"
        cursor.execute(sql)
        selectAll = cursor.fetchall()
        listAll = []
        cost = 0
        for each in selectAll:
            listAll.append(int(each[1].split('分钟')[0]))
        for eachE in listAll:
            if listAll.index(eachE) - 1 < 0:
                front = 0
            else:
                front = listAll[listAll.index(eachE) - 1]
            if listAll.index(eachE) + 1 > len(listAll) - 1:
                behind = 0
            else:
                behind = listAll[listAll.index(eachE) + 1]
            if eachE >= front and eachE >= behind:
                cost += eachE
        return cost

    def selectMultipleFrequencyOfToday(self):
        conn, cursor = ConnectAndClose().database_connect()
        sql = "select BQ, COUNT(*) from s7300warning where BJ='报警' and TO_DAYS(NOW()) - TO_DAYS(SJ) < 7 GROUP BY BQ ORDER BY BQ ASC"
        cursor.execute(sql)
        selectAll = cursor.fetchall()
        resultList = []
        for each in selectAll:
            resultList.append([each[0], each[1]])
        return resultList

    def selectMultipleFrequencyOfWeek(self):
        conn, cursor = ConnectAndClose().database_connect()
        sql = "select BQ, a.d , count(*) FROM(select BQ, TO_DAYS(NOW()) - TO_DAYS(SJ) as d from s7300warning WHERE BJ='报警' and  TO_DAYS(NOW()) - TO_DAYS(SJ)< 7 ORDER BY BQ ASC, TO_DAYS(NOW()) - TO_DAYS(SJ) ASC) as a GROUP BY BQ, a.d ORDER BY BQ ASC, d ASC;"
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
            for i in range(0, 6):
                count = 0
                for each in selectAll:
                    if eachName == each[0]:
                        if each[1] == i:
                            count = each[2]
                listOne.append(count)
            resultDict[eachName] = listOne
        return resultDict








    # def draw_line_BendingMachine(self):
    #     x = [1, 2, 3]
    #     y = [1, 2, 2]
    #     F = MyFigure(width=4.7, height=3.7, dpi=100)
    #     F.axes.plot(x, y)
    #     F.axes.scatter(x, y)
    #     F.axes.set_xlabel('时刻')
    #     F.axes.set_ylabel('效率')
    #     F.axes.set_title('折弯机效率图')
    #     F.axes.set_xticks(x, minor=True)
    #     graphicscene = QtWidgets.QGraphicsScene()
    #     graphicscene.addWidget(F)
    #     self.graphicsView_6.setScene(graphicscene)
    #     self.graphicsView_6.show()
    #     plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

if __name__ == '__main__':
    utils = Utils()
    # utils.selectSingleFrequencyAndTimeCostByName("2号变频器故障反馈")
    # utils.selectSingleTimeSpendBYName("1号变频器故障反馈")
    # utils.selectMultipleFrequencyOfToday()
    utils.selectMultipleFrequencyOfWeek()
        # select
        # count(*)
        # from s7300warning where
        # BJ = '报警' and TO_DAYS(NOW()) - TO_DAYS(SJ) = 0 and BQ =  # {name}
