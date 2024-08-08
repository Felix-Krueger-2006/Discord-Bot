import pymysql
from datetime import datetime

connection_bot = None
connection_bansys = None

def table_check():
    global connection_bot
    global connection_bansys
    
    try:
        connection_bot = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            port=3306,
            database='bot',
            connect_timeout=30 
        )
        connection_bansys = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            port=3306,
            database='bansys',
            connect_timeout=30 
        )
    except Exception as e:
        print("Der Bot konnte sich nicht mit der Datenbank verbinden: " + str(e))
        
    try:
        with connection_bot.cursor() as cursor:
            sqls = [
                "CREATE TABLE IF NOT EXISTS mysql_whitelist (UUID VARCHAR(100) NOT NULL, user VARCHAR(100) NOT NULL);",
                "CREATE TABLE IF NOT EXISTS settings (setting VARCHAR(255) NOT NULL, value VARCHAR(255) NOT NULL);",
                "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, discord VARCHAR(255) NOT NULL, minecraft VARCHAR(255) NOT NULL);",
                "CREATE TABLE IF NOT EXISTS giveaways (id INT AUTO_INCREMENT PRIMARY KEY, author CHAR(255) NOT NULL,title CHAR(255) NOT NULL,description CHAR(255) NOT NULL,image CHAR(255) NOT NULL,winner CHAR(255),start DATE NOT NULL,end DATE NOT NULL,time TIME NOT NULL,begin INTEGER NOT NULL,complete INTEGER NOT NULL, message CHAR(255));"
            ]
            settings = ["bot-code", "status-channel", "player-channel", "whitelist-channel", "giveaway-channel", "logs-channel", "commands-channel", "server-adress"]
            
            for sql in sqls:
                cursor.execute(sql)
            
            for setting in settings:
                insert_setting(setting)
                
            connection_bot.commit()
            
    except Exception as e:
        print("Der Bot konnte die Tabellen nicht erstellen! \nError: " + str(e))
        
        
def insert_setting(setting):
    try:
        with connection_bot.cursor() as cursor:
            sql_select = "SELECT COUNT(*) FROM settings WHERE setting = %s;"
            cursor.execute(sql_select, (setting, ))
            result = cursor.fetchone()
            count = result[0]
            
            if count <= 0:
                sql_insert = "INSERT INTO settings (setting, value) VALUES (%s, %s);"
                cursor.execute(sql_insert, (setting, '0'))
        
        connection_bot.commit()
    
    except Exception as e:
        print("Fehler beim Einfügen der Settings:")
        print(e)

def get_setting(setting):
    with connection_bot.cursor() as cursor:
        sql = "SELECT setting, value FROM settings WHERE setting = %s;"
            
        cursor.execute(sql, (setting,))
        result = cursor.fetchone()
            
        if result is None:
            return None
            
        return {"setting": result[0], "value": result[1]}

def get_discord_id(uuid):
    with connection_bot.cursor() as cursor:
        sql_select = "SELECT discord FROM users WHERE minecraft = %s;"
        cursor.execute(sql_select, (uuid, ))
        try:
            result = cursor.fetchone()
            result = result[0]
            return result
        except:
            return None

def get_minecraft_uuid(id):
    with connection_bot.cursor() as cursor:
        sql_select = "SELECT minecraft FROM users WHERE discord = %s;"
        cursor.execute(sql_select, (id, ))
        try:
            result = cursor.fetchone()
            result = result[0]
            return result
        except:
            return None

async def name_check(uuid):
    with connection_bot.cursor() as cursor:
        sql_select = "SELECT COUNT(*) FROM mysql_whitelist WHERE UUID = %s;"
        cursor.execute(sql_select, (str(uuid), ))
        result = cursor.fetchone()
        count = result[0]
        
        if count <= 0:
            return False
        else:
            return True

async def user_already_in(id):
    with connection_bot.cursor() as cursor:
        sql_select = "SELECT minecraft FROM users WHERE discord = %s;"
        cursor.execute(sql_select, (id, ))
        result = cursor.fetchone()
        minecraft_uuid = result[0] if result is not None else None
        
        if minecraft_uuid != None and await name_check(minecraft_uuid):
            return True
        else:
            return False

async def user_exist(id):
    with connection_bot.cursor() as cursor:
        sql_select = "SELECT COUNT(*) FROM users WHERE discord = %s;"
        cursor.execute(sql_select, (str(id), ))
        result = cursor.fetchone()
        count = result[0]
        
        if count <= 0:
            return False
        else:
            return True

async def delete_user_from_whitelist(uuid):
    with connection_bot.cursor() as cursor:
        sql = f"DELETE FROM mysql_whitelist WHERE UUID = '{uuid}';"
        cursor.execute(sql)
        connection_bot.commit()

async def add_user_to_whitelist(name, uuid):
    with connection_bot.cursor() as cursor:
        sql = f"INSERT INTO mysql_whitelist (UUID, user) VALUES ('{uuid}', '{name}');"
        cursor.execute(sql)
        connection_bot.commit()
        
async def add_user_to_table(discord, minecraft):
    with connection_bot.cursor() as cursor:
        sql = f"INSERT INTO users (id, discord, minecraft) VALUES (0, '{discord}', '{minecraft}');"
        cursor.execute(sql)
        connection_bot.commit()
        
async def replace_user_in_table(uuid, id):
    with connection_bot.cursor() as cursor:
        sql = "UPDATE users SET minecraft = %s WHERE discord = %s;"
        cursor.execute(sql, (str(uuid), str(id), ))
        connection_bot.commit()
        
async def check_if_giveaway_starts():
    day = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    with connection_bot.cursor() as cursor:
        sql = "SELECT * FROM giveaways WHERE start = %s AND time < %s"
        cursor.execute(sql, (day, time, ))
        result = cursor.fetchone()
        
        if result:
            return result
        else:
            return None

async def check_if_giveaway_ends():
    day = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    with connection_bot.cursor() as cursor:
        sql = "SELECT * FROM giveaways WHERE end = %s AND time < %s"
        cursor.execute(sql, (day, time, ))
        result = cursor.fetchone()
        
        if result:
            return result
        else:
            return None

async def set_giveaway_on_active(liste, message):
    id = liste[0]
    with connection_bot.cursor() as cursor:
        sql = "UPDATE giveaways SET begin = %s, message = %s WHERE id = %s;"
        cursor.execute(sql, (1, str(message), id, ))
        connection_bot.commit()
        
async def set_giveaway_on_ends(liste):
    id = liste[0]
    with connection_bot.cursor() as cursor:
        sql = "UPDATE giveaways SET complete = %s WHERE id = %s;"
        cursor.execute(sql, (1, id, ))
        connection_bot.commit()

async def set_giveaway_winner(liste, user):
    id = liste[0]
    winner = str(user.id) + "§" + str(user.name)
    with connection_bot.cursor() as cursor:
        sql = "UPDATE giveaways SET winner = %s WHERE id = %s;"
        cursor.execute(sql, (winner, ))
        connection_bot.commit()
        
async def count_whitelist():
    with connection_bot.cursor() as cursor:
        sql = "SELECT COUNT(*) FROM mysql_whitelist"
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        
        return result