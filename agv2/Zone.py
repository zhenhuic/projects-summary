def readpoints():
    points = {}
    with open('newpoint1.txt') as f:
        for line in f:
            point = line.split(',', -1)[0].strip()
            x = line.split(',', -1)[1].strip()
            y = line.split(',', -1)[2].strip()
            points[point] = [x, y]
    return points

#node是点位 number是几号车

def isZone(node, number):
    points = readpoints()
    if str(node) in points:
        x = (float(points[str(node)][0]) + 130) / 130 * 1920
        y = (163 - float(points[str(node)][1])) / 90 * 1080
        print('点的坐标', x, y)

        #蓝黑2交接处
        if node in [392, 237, 301, 600, 531]:
            if number in [1, 2, 3]:
                return [4]
            else:
                return [3]

        # 红 1 黑1 2 黑2 3 蓝 4 黄 5 紫 6
        if y < (163 - float(points[str(325)][1])) / 90 * 1080:
            return [1]
        elif y <= (163 - float(points[str(200)][1])) / 90 * 1080:
            if x < (float(points[str(599)][0]) + 130) / 130 * 1920:
                return [2]
            if x < (float(points[str(602)][0]) + 130) / 130 * 1920 and y < (163 - float(points[str(392)][1])) / 90 * 1080:
                return [4]
            if x > (float(points[str(606)][0]) + 130) / 130 * 1920 and x <= (float(points[str(931)][0]) + 130) / 130 * 1920 and y < (163 - float(points[str(308)][1])) / 90 * 1080:
                return [3]
            if x > (float(points[str(327)][0]) + 130) / 130 * 1920 and y < (163 - float(points[str(82)][1])) / 90 * 1080:
                return [5]
            if x > (float(points[str(160)][0]) + 130) / 130 * 1920:
                return [4, 5]
            else:
                if number in [1, 2, 3]:
                    return [4]
                else:
                    return [6]
        elif y >= (163 - float(points[str(509)][1])) / 90 * 1080:
            return [6]
        else:
            return []

    else:
        return []


#
# x = isZone(585,1)
# print(x)
#




