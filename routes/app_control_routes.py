from flask import Blueprint, jsonify, request
import mysql.connector
from config.databaselink import *
from config.urlink import *
import json
import requests
import hashlib
import time

app_control_bp = Blueprint('app_control', __name__, url_prefix='/app_control')

@app_control_bp.route('/update_credit', methods=['POST'])
def update_credit():
    try:
        phone = request.json.get('phone')
        amount = request.json.get('amount')
        env = request.json.get('env')
        
        # 根据环境选择数据库
        db_name = APPDEV_DB_NAME if env == 'DEV' else APPUAT_DB_NAME
        
        # 连接APPUAT数据库
        appuat_conn = mysql.connector.connect(
            host=APPUAT_DB_HOST,
            port=APPUAT_DB_PORT,
            user=APPUAT_DB_USER,
            password=APPUAT_DB_PASSWORD,
            database=db_name
        )
        
        # 连接APIdev数据库
        apidev_conn = mysql.connector.connect(
            host=API_DEV_DB_HOST,
            port=API_DEV_DB_PORT,
            user=API_DEV_DB_USER,
            password=API_DEV_DB_PASSWORD,
            database=API_DEV_DB_NAME
        )

        # APPUAT更新逻辑
        with appuat_conn.cursor() as cursor:
            cursor.execute("SELECT uid FROM yx_user WHERE username=%s", (phone,))
            result = cursor.fetchone()
            if not result:
                return jsonify({"code": "404", "message": "APP无用户数据"})
            
            cursor.fetchall()
            cursor.execute("""
                UPDATE tb_credit_info 
                SET credit_amt = %s, used_amt = 0 
                WHERE user_id IN (SELECT uid FROM yx_user where username=%s)
            """, (amount, phone))
            appuat_conn.commit()

        # APIDEV更新逻辑
        with apidev_conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM zx_credit_user_info WHERE mobile=%s", (phone,))
            result = cursor.fetchone()
            if not result:
                return jsonify({"code": "404", "message": "API无用户数据"})
            
            cursor.fetchall()
            cursor.execute("""
                UPDATE zx_credit_info 
                SET credit_amt = %s, used_amt = 0 
                WHERE user_id IN (SELECT user_id FROM zx_credit_user_info where mobile=%s)
            """, (amount, phone))
            apidev_conn.commit()

        return jsonify({"code": "200", "message": "更新成功"})

    except Exception as e:
        return jsonify({"code": "500", "message": str(e)})
    finally:
        if 'appuat_conn' in locals():
            appuat_conn.close()
        if 'apidev_conn' in locals():
            apidev_conn.close()

@app_control_bp.route('/delete_login', methods=['POST'])
def delete_login():
    try:
        phone = request.json.get('phone')
        env = request.json.get('env')
        
        # 根据环境选择数据库
        db_name = APPDEV_DB_NAME if env == 'DEV' else APPUAT_DB_NAME
        
        conn = mysql.connector.connect(
            host=APPUAT_DB_HOST,
            port=APPUAT_DB_PORT,
            user=APPUAT_DB_USER,
            password=APPUAT_DB_PASSWORD,
            database=db_name
        )

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM tb_user_login_log 
                WHERE user_id IN (SELECT uid FROM yx_user where username=%s)
            """, (phone,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"code": "404", "message": "APP无用户登录数据"})

            cursor.execute("""
                DELETE FROM tb_user_login_log 
                WHERE user_id IN (SELECT uid FROM yx_user where username=%s)
            """, (phone,))
            conn.commit()

        return jsonify({"code": "200", "message": "删除成功"})

    except Exception as e:
        return jsonify({"code": "500", "message": str(e)})
    finally:
        if 'conn' in locals():
            conn.close()

@app_control_bp.route('/update_ab_label', methods=['POST'])
def update_ab_label():
    try:
        phone = request.json.get('phone')
        env = request.json.get('env')
        ab_label = request.json.get('ab_label')
        
        # 根据环境选择数据库
        db_name = APPDEV_DB_NAME if env == 'DEV' else APPUAT_DB_NAME
        
        conn = mysql.connector.connect(
            host=APPUAT_DB_HOST,
            port=APPUAT_DB_PORT,
            user=APPUAT_DB_USER,
            password=APPUAT_DB_PASSWORD,
            database=db_name
        )

        with conn.cursor() as cursor:
            # 检查用户是否存在
            cursor.execute("SELECT COUNT(*) FROM yx_user WHERE username=%s", (phone,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"code": "404", "message": "用户不存在"})

            # 更新AB面标签
            cursor.execute("UPDATE yx_user SET ab_label=%s WHERE username=%s", (ab_label, phone))
            conn.commit()

        return jsonify({"code": "200", "message": "更新成功"})

    except Exception as e:
        return jsonify({"code": "500", "message": str(e)})
    finally:
        if 'conn' in locals():
            conn.close()

@app_control_bp.route('/report_customer', methods=['POST'])
def report_customer():
    try:
        name = request.json.get('name')
        id_card = request.json.get('idCard')
        phone = request.json.get('phone')
        channel = request.json.get('channel')

        # 构建加密请求数据
        request_data = {
            "data": json.dumps({
                "baseInfo": {
                    "name": name,
                    "idCardNo": id_card,
                    "issueOrg": "安化县公安局",
                    "startDate": "2016-08-08",
                    "endDate": "2026-12-12",
                    "gender": 1,
                    "ethnic": "汉",
                    "front": "https://picture-test.usurong.com/ocrAuthentica/348cd75606214c0fa6201204ecf53bd21710899889106.JPG",
                    "back": "https://picture-test.usurong.com/ocrAuthentica/ae06039d72aa4be18e0f3e68ee4e2cfe1710899873736.JPG",
                    "maritalStatus": "20",
                    "occupation": "0",
                    "income": "2",
                    "educationLevel": "20",
                    "channel": channel
                },
                "contactInfos": [
                    {"phoneType": "1", "phone": phone, "contactType": "1"},
                    {"phoneType": "2", "phone": phone, "contactType": "1"}
                ],
                "faceInfos": [{
                    "url": "https://picture-test.usurong.com/ocrAuthentica/348cd75606214c0fa6201204ecf53bd21710899889106.JPG",
                    "faceChannel": "FACE++",
                    "score": 99.8
                }],
                "domicileAddrInfos": [{
                    "domicileAddr": "湖南省安化县东坪镇建设路萼辉巷16号"
                }],
                "residenceAddrInfos": [{
                    "residenceAddr": "湖南省安化县东坪镇建设路萼辉巷16号",
                    "residenceProvince": "440000",
                    "residenceCity": "440100",
                    "residenceDistrict": "440115"
                }],
                "workUnitInfos": [{
                    "name": "湖南省安化县东坪镇建设路萼辉巷16号",
                    "addr": "湖南省安化县东坪镇建设路萼辉巷16号",
                    "unitIndustry": "H",
                    "unitContact": "15862448561"
                }],
                "contactPersonInfos": [
                    {"name": "阿萨德", "phone": "13855965552", "relation": "40"},
                    {"name": "付费", "phone": "13855965553", "relation": "50"},
                    {"name": "订单", "phone": "13855965554", "relation": "30"}
                ]
            }),
            "partner": "API"
        }

        # 调用加密接口
        encrypt_response = requests.post(
            'http://192.168.1.101:8290/test/encrypt',
            json=request_data
        )
        
        if encrypt_response.status_code != 200:
            return jsonify({"code": "500", "message": "加密接口调用失败"})

        encrypted_data = encrypt_response.json()

        # 调用客户信息上报接口
        report_response = requests.post(
            'http://192.168.1.101:8290/customer/report',
            json=encrypted_data
        )

        if report_response.status_code != 200:
            return jsonify({"code": "500", "message": "客户信息上报失败"})

        report_result = report_response.json()
        
        # 修改断言逻辑：检查返回的code是否为0
        if report_result.get('code') != 0:
            return jsonify({
                "code": "500",
                "message": report_result.get('msg', '上报失败')
            })

        return jsonify({
            "code": "200",
            "message": "上报成功"
        })

    except Exception as e:
        return jsonify({"code": "500", "message": f"操作失败：{str(e)}"}) 

@app_control_bp.route('/apply_credit', methods=['POST'])
def apply_credit():
    try:
        phone = request.json.get('phone')
        name = request.json.get('name')
        id_card = request.json.get('idCard')
        channel = request.json.get('channel')
        env = request.json.get('env')
        
        # 获取环境URL
        base_url = APP_TEST_URL if env == 'APP_TEST' else APP_UAT_URL
        
        # MD5加密
        phone_md5 = hashlib.md5(phone.encode()).hexdigest()
        cid_md5 = hashlib.md5(id_card.encode()).hexdigest()
        
        # 第一次加密请求
        first_encrypt_data = {
            "data": json.dumps({
                "phoneMD5": phone_md5,
                "cidMD5": cid_md5
            }),
            "channelId": channel,
            "pid": "1"
        }
        
        encrypt_response = requests.post(
            f'{base_url}/test/encrypt',
            json=first_encrypt_data
        )
        
        if encrypt_response.status_code != 200:
            return jsonify({"code": "500", "message": "加密接口调用失败"})
            
        # 调用hit接口
        hit_response = requests.post(
            f'{base_url}/v1/hit',
            json=encrypt_response.json()
        )
        
        if hit_response.status_code != 200:
            return jsonify({"code": "500", "message": "hit接口调用失败"})
            
        # 生成applyId
        apply_id = f"test{int(time.time()*1000)}"
        
        # 第二次加密请求
        second_encrypt_data = {
            "data": json.dumps({
                "applyAmount": 10000,
                "applyId": apply_id,
                "basicInfo": {
                    "companyName": "众利有限公司",
                    "degree": 10,
                    "houseAddress": "广州市南沙区富家花园",
                    "houseCity": "广州市",
                    "houseCityId": "440100",
                    "houseDistrict": "南沙区",
                    "houseDistrictId": "440117",
                    "houseProvince": "广东省",
                    "houseProvinceId": "440000",
                    "marriage": 10,
                    "phone": phone
                },
                "contactInfo": [
                    {"name": "陈胜利", "phone": "13660168486", "relation": "60", "sort": 1},
                    {"name": "袁芳", "phone": "13042027868", "relation": "60", "sort": 2}
                ],
                "idInfo": {
                    "address": "湖南省安化县东坪镇建设路萼辉巷16号",
                    "backUrl": "https://picture-test.usurong.com/ocrAuthentica/ae06039d72aa4be18e0f3e68ee4e2cfe1710899873736.JPG",
                    "cid": id_card,
                    "faceScore": "100",
                    "faceUrl": "https://picture-test.usurong.com/ocrAuthentica/348cd75606214c0fa6201204ecf53bd21710899889106.JPG",
                    "frontUrl": "https://picture-test.usurong.com/ocrAuthentica/fa518b1f00144c1598dc9b5d797505fe1710899873920.JPG",
                    "gender": "M",
                    "issuedBy": "安化县公安局",
                    "name": name,
                    "nation": "汉族",
                    "validEndDate": "20260808",
                    "validStartDate": "20160808"
                },
                "supplementInfo": {
                    "income": 1,
                    "occupation": "0"
                },
                "deviceInfo": {
                    "ip": "14.145.141.5",
                    "gps": {
                        "x": "113.859339",
                        "y": "22.569849"
                    }
                }
            }),
            "channelId": channel,
            "pid": "1"
        }
        
        second_encrypt_response = requests.post(
            f'{base_url}/test/encrypt',
            json=second_encrypt_data
        )
        
        if second_encrypt_response.status_code != 200:
            return jsonify({"code": "500", "message": "第二次加密失败"})
            
        # 调用授信接口
        credit_response = requests.post(
            f'{base_url}/v1/apiApplyCredit',
            json=second_encrypt_response.json()
        )
        
        if credit_response.status_code != 200:
            return jsonify({"code": "500", "message": "授信申请失败"})
            
        return jsonify({"code": "200", "message": "授信申请成功"})

    except Exception as e:
        return jsonify({"code": "500", "message": f"操作失败：{str(e)}"}) 

@app_control_bp.route('/skip_face', methods=['POST'])
def skip_face():
    try:
        phone = request.json.get('phone')
        env = request.json.get('env')
        
        # 根据环境选择数据库
        db_name = APPDEV_DB_NAME if env == 'DEV' else APPUAT_DB_NAME
        
        conn = mysql.connector.connect(
            host=APPUAT_DB_HOST,
            port=APPUAT_DB_PORT,
            user=APPUAT_DB_USER,
            password=APPUAT_DB_PASSWORD,
            database=db_name
        )

        with conn.cursor() as cursor:
            # 检查用户是否存在
            cursor.execute("SELECT COUNT(*) FROM tb_loan_user_info WHERE mobile=%s", (phone,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"code": "404", "message": "用户不存在"})

            # 更新用户状态
            cursor.execute("UPDATE tb_loan_user_info SET state='1,2,3,5' WHERE mobile=%s", (phone,))
            conn.commit()

        return jsonify({"code": "200", "message": "更新成功"})

    except Exception as e:
        return jsonify({"code": "500", "message": str(e)})
    finally:
        if 'conn' in locals():
            conn.close() 