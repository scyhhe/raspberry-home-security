rm -f pep.zip
mkdir -p pep_backup
mv alarm.py pep_backup 2>/dev/null
mv restarter.py pep_backup 2>/dev/null
mv alarmfunctionsr.py pep_backup 2>/dev/null
mv dht22.py pep_backup 2>/dev/null
mv dallas.py pep_backup 2>/dev/null
mv rfsensor.py pep_backup 2>/dev/null
mv globals.py pep_backup 2>/dev/null
mv webcam.py pep_backup 2>/dev/null

mv lcd_hd44780.py pep_backup 2>/dev/null
mv lcd_nokia.py pep_backup 2>/dev/null
mv lcdtest.py pep_backup 2>/dev/null
mv publish.py pep_backup 2>/dev/null
mv subscribe.py pep_backup 2>/dev/null

wget www.privateeyepi.com/downloads/pep.zip
unzip -o pep.zip
chmod 700 alarm.py
chmod 700 dallas.py
chmod 700 globals.py
chmod 700 alarmfunctionsr.py
chmod 700 dht22.py
chmod 700 restarter.py
chmod 700 pep_backup
chmod 700 webcam.py

chmod 700 lcd_hd44780.py
chmod 700 lcd_nokia.py
chmod 700 lcdtest.py
chmod 700 publish.py
chmod 700 subscribe.py

sudo apt-get install python-serial
