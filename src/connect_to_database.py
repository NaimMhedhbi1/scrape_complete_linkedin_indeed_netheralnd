import pyodbc 
conn = pyodbc.connect('Driver=SQL Server'
                      'Server=DESKTOP-QIQG2OF\SQLEXPRESS'
                      'Database=tests'
                      'Trusted_Connection=yes')

cursor = conn.cursor()


#server name : DESKTOP-QIQG2OF\SQLEXPRESS
