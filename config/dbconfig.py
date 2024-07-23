import mysql.connector


def test_connect_to_database():
    try:
        # 创建数据库连接
        connection = mysql.connector.connect(
            host="rm-bp1eh9qv3b2p5vu98mo.mysql.rds.aliyuncs.com",
            port=3306,
            user="myadmin",
            password="Wszw1990@",
            database="ifs"
        )

        # 如果连接成功，打印消息
        if connection.is_connected():
            print("ZLSK数据库连接成功")
            return connection
        else:
            print("连接失败，尽管连接对象已创建，但可能无法与数据库通信。")
            return None
    except mysql.connector.Error as err:
        # 如果连接失败，抛出异常
        print(f"连接失败: {err}")
        raise

    # 调用方法并传入数据库连接信息

