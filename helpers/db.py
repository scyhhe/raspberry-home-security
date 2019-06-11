import sqlite3

try:
    db = sqlite3.connect('/home/pi/raspberry-home-security/passcodes.db')
    print('Connected!', sqlite3.version)
except:
    print('Connection failed.')



def insert_passcode(name, code):
    cursor = db.cursor()
    try:
        cursor.execute(
                '''INSERT INTO passcodes(owner, combination)
                   VALUES(?,?)''', (name, code))
        print('Passcode for {} added'.format(name))
        db.commit()
    except:
        print('Name OR combination already exist.')
        

def check_passcode(code):
    cursor = db.cursor()
    code_parsed = int(code)
    match = cursor.execute('''SELECT COUNT(*) FROM passcodes WHERE combination = ?''',
                           (code_parsed,))

    passcode = match.fetchone()
    if not passcode[0]:
        return False
    return True


if __name__ == '__main__':
    db.execute(
        '''CREATE TABLE IF NOT EXISTS PASSCODES
         (ID INTEGER PRIMARY KEY NOT NULL,
         OWNER  TEXT UNIQUE NOT NULL,
         COMBINATION INTEGER UNIQUE NOT NULL)
        ''')
    print("Table created successfully");

