from quart import Quart,request,json, render_template
from telethon import TelegramClient, utils
import pymssql
# Telethon simply doesnt work with flask. So need to Quartz.
# Reference : https://github.com/LonamiWebs/Telethon/tree/master/telethon_examples#quart_loginpy

SESSION = 'SESSION_NAME'
API_ID = YOUR_API_ID
API_HASH = 'YOUR_API_HASH'

app = Quart(__name__)

@app.route('/info',methods=['GET','POST'])
async def info():
    if not client.is_connected():
        await client.connect()
        
    info = await(client.get_me())
    return str(info)

@app.route('/',methods=['GET','POST'])
async def root():
    response = {'status':'200 OK'}
    return json.jsonify(response)

@app.route('/update_transaction',methods=['GET','POST'])
async def update_db():
    transaction_id = request.args.get('transact_id')
    contact_no = request.args.get('contact_no')
    session_id = request.args.get('session_id')
    conn = pymssql.connect('DBSERVER', 'DBUSER', 'DBPASS', "DBNAME")
    cursor=conn.cursor()
    cursor.execute("UPDATE transactionTable set transactionID='"+ transaction_id +"',contactNumber='" + contact_no + "' WHERE ID=" +session_id)
    conn.commit()
    response = {'result' : "OK",'message': "Database updated"}
    cursor.close()
    conn.close()
    return json.jsonify(response)

@app.route('/send',methods=['GET','POST'])
async def send_message():
    number = request.args.get('number')
    message = request.args.get('message')
    response = {}
    if number and message:
        if not client.is_connected():
            await client.connect()
        try:
            message_object = await(client.send_message(number,message))
            response['message'] = str(message_object)
            response['result'] = "OK"
        except ValueError:
            response['message'] = "Recepient name or number not found "
            response['result'] = "ERROR"
        except:
            response['message'] = "Error sending message"
            response['result'] = "ERROR"
    else:
        response['message'] = "Params missing"
        response['result'] = "ERROR"
    
    return json.jsonify(response)
    
client = TelegramClient(SESSION, API_ID, API_HASH)
client.parse_mode = 'html'  # <- render things nicely
app.run(loop=client.loop,host='0.0.0.0')
