from flask import Blueprint, request, render_template
import redis
from config.redislink import *

redis_bp = Blueprint('redis', __name__, url_prefix='/delredis')

@redis_bp.route('/delete', methods=['POST'])
def delete_key():
    r = None
    try:
        db_index = int(request.form['db_index'])
        key = request.form['key']

        r = redis.StrictRedis(
            host=redisAPPUAT_host, 
            port=redisAPPUAT_port, 
            password=redisAPPUAT_password, 
            db=db_index, 
            decode_responses=True
        )

        if r.delete(key):
            message = f"Key '{key}' deleted successfully from database index {db_index}."
        else:
            message = f"Key '{key}' does not exist in database index {db_index}."

        return render_template('delredis.html', message=message)
    finally:
        if r:
            r.close() 