import pymysql

try:
    connection_bot = pymysql.connect(
        host='lxo.h.filess.io',
        user='bot_opendoneon',
        password='8110ec97c1417dcea4a5842aaa2e79b7119a1bf9',
        port=3307,
        database='bot_opendoneon'
    )
    connection_bansys = pymysql.connect(
        host='bq6.h.filess.io',
        user='bansys_couplemill',
        password='823a3d2cf0cad8436d485dd845a038c44a602761',
        port=3305,
        database='bansys_couplemill'
    )
except Exception as e:
    print("Der Bot konnte sich nicht mit der Datenbank verbinden: " + str(e))

import pymysql

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
        print("Fehler beim Einfügen des Settings:")
        print(e)

def get_setting(setting):
    with connection_bot.cursor() as cursor:
        sql = "SELECT setting, value FROM settings WHERE setting = %s;"
            
        cursor.execute(sql, (setting,))
        result = cursor.fetchone()
            
        if result is None:
            return None
            
        return {"setting": result[0], "value": result[1]}

def addUser(ingamename, uuid):
    with connection_bot.cursor() as cursor:
        sql = f"INSERT INTO mysql_whitelist (UUID, user) VALUES ('{uuid}', '{ingamename.lower()}');"
        cursor.execute(sql)
        connection_bot.commit()

async def name_check(uuid):
    with connection_bot.cursor() as cursor:
        sql_select = "SELECT COUNT(*) FROM mysql_whitelist WHERE UUID = %s;"
        cursor.execute(sql_select, (uuid, ))
        result = cursor.fetchone()
        count = result[0]
        
        if count <= 0:
            return False
        else:
            return True

try:
    with connection_bot.cursor() as cursor:
        sqls = [
            "CREATE TABLE IF NOT EXISTS settings (setting VARCHAR(255) NOT NULL, value VARCHAR(255) NOT NULL);",
            "CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, discord VARCHAR(255) NOT NULL, minecraft VARCHAR(255) NOT NULL);"
        ]
        settings = ["bot-code", "status-channel", "player-channel", "whitelist-channel", "giveaway-channel", "logs-channel", "server-adress"]
        
        for sql in sqls:
            cursor.execute(sql)
        
        for setting in settings:
            insert_setting(setting)
            
        connection_bot.commit()
        
except Exception as e:
    print("Der Bot konnte die Tabellen nicht erstellen! \nError: " + str(e))