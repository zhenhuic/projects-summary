# 配置管理员账号密码
Administor = {"name": "admin", "password": "111"}


# 对账号密码进行校对
def checkAccount(account, password):
    if account == Administor["name"] and password == Administor["password"]:
        return True
    else:
        return False


if __name__ == '__main__':
    pass
