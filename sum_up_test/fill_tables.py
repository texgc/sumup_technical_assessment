import csv
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sumup_test"
)

cursor = conn.cursor()

#Fill STORE table
csv_file_path = 'STORE.csv'

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)

    insert_query = """
    INSERT INTO STORE (id,name,address,city,country,created_at,typology,customer_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for row in csv_reader:
        cursor.execute(insert_query, row)

#Fill DEVICE table
csv_file_path = 'DEVICE.csv'

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)

    insert_query = """
    INSERT INTO DEVICE (id,type,store_id)
    VALUES (%s, %s, %s)
    """

    for row in csv_reader:
        cursor.execute(insert_query, row)

#Fill TRANSACTION_STORE table
csv_file_path = 'transaction.csv'

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)

    insert_query = """
    INSERT INTO TRANSACTION_STORE (id,device_id,product_name,product_sku,category_name,amount,status,card_number,cvv,created_at,happened_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for row in csv_reader:
        cursor.execute(insert_query, row)

conn.commit()
cursor.close()
conn.close()