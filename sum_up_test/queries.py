import csv
import mysql.connector
import os

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sumup_test"
)

cursor = conn.cursor()

ten_stores_per_transacted_amount = """WITH TotalStoreTransactionAmount AS (
                    SELECT
                        s.id AS store_id,
                        s.name AS store_name,
                        SUM(ts.amount) AS total_transacted_amount
                    FROM
                        STORE s
                    JOIN
                        DEVICE d ON s.id = d.store_id
                    JOIN
                        TRANSACTION_STORE ts ON d.id = ts.device_id
                    GROUP BY
                        s.id, s.name
                )
                SELECT
                s.store_id,
                    s.store_name,
                    s.total_transacted_amount
                    FROM
                        TotalStoreTransactionAmount s
                    ORDER BY s.total_transacted_amount DESC  
                    LIMIT 10;
                """

cursor.execute(ten_stores_per_transacted_amount)

with open("/Users/texiagonzalezcaceres/Desktop/sum_up_test/queries_results/ten_stores_per_transacted_amount.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

ten_products_sold = """ WITH TotalSoldAmountBySku AS (
                                        SELECT
                                            product_name,
                                            product_sku,
                                            SUM(amount) AS total_sold_amount
                                        FROM
                                            TRANSACTION_STORE
                                        GROUP BY
                                            product_name, product_sku
                                    )
                                    SELECT
                                        *
                                    FROM
                                        TotalSoldAmountBySku
                                    ORDER BY
                                        total_sold_amount DESC
                                    LIMIT 10;
                    """ 

cursor.execute(ten_products_sold)

with open("/Users/texiagonzalezcaceres/Desktop/sum_up_test/queries_results/ten_products_sold.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

average_transacted_amount_per_store_typo_country = """ WITH StoreTransactionInfo AS (
                                                        SELECT
                                                            d.store_id,
                                                            s.typology,
                                                            s.country,
                                                            COUNT(ts.id) AS transaction_count,
                                                            SUM(ts.amount) AS total_amount
                                                        FROM
                                                            TRANSACTION_STORE ts
                                                        JOIN
                                                            DEVICE d ON ts.device_id = d.id
                                                        JOIN
                                                            STORE s ON d.store_id = s.id
                                                        GROUP BY
                                                            d.store_id, s.typology, s.country
                                                    )
                                                    SELECT
                                                        store_id,
                                                        typology,
                                                        country,
                                                        total_amount / transaction_count AS average_transacted_amount
                                                    FROM
                                                        StoreTransactionInfo;
                                                """ 

cursor.execute(average_transacted_amount_per_store_typo_country)

with open("/Users/texiagonzalezcaceres/Desktop/sum_up_test/queries_results/average_transacted_amount_per_store_typo_country.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

percentage_transactions_per_device_type = """ SELECT
                                                d.type,
                                                COUNT(t.id) AS transaction_count,
                                                ROUND((COUNT(t.id) * 100.0) / (SELECT COUNT(*) FROM TRANSACTION_STORE), 2) AS percentage_of_transactions
                                            FROM
                                                TRANSACTION_STORE t
                                            JOIN
                                                DEVICE d ON t.device_id = d.id
                                            GROUP BY
                                                d.type;
""" 

cursor.execute(percentage_transactions_per_device_type)

with open("/Users/texiagonzalezcaceres/Desktop/sum_up_test/queries_results/percentage_transactions_per_device_type.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

average_time_for_store_perform_five_first_transactions = """ WITH RankedTransactions AS (
                                                                    SELECT
                                                                        d.store_id,
                                                                        ts.happened_at,
                                                                        ROW_NUMBER() OVER (PARTITION BY d.store_id ORDER BY ts.happened_at) AS transaction_rank
                                                                    FROM
                                                                        TRANSACTION_STORE ts
                                                                    JOIN
                                                                        DEVICE d ON ts.device_id = d.id
                                                                ),
                                                                FiveTransactions AS (
                                                                    SELECT DISTINCT store_id 
                                                                    FROM RankedTransactions
                                                                    WHERE transaction_rank = 5
                                                                ),
                                                                TransactionData AS (
                                                                    SELECT *
                                                                    FROM RankedTransactions r
                                                                    WHERE r.store_id IN (SELECT store_id FROM FiveTransactions)
                                                                ),
                                                                Transaction_one AS (
                                                                    SELECT store_id, happened_at AS happened_at_one
                                                                    FROM TransactionData
                                                                    WHERE transaction_rank = 1
                                                                ),
                                                                Transaction_five AS (
                                                                    SELECT store_id, happened_at AS happened_at_five
                                                                    FROM TransactionData
                                                                    WHERE transaction_rank = 5
                                                                ),
                                                                Transaction_five_one AS (
                                                                    SELECT tf.store_id, tf.happened_at_five, tro.happened_at_one
                                                                    FROM Transaction_five tf
                                                                    JOIN Transaction_one tro ON tf.store_id = tro.store_id
                                                                ),
                                                                DaysDifference AS (
                                                                    SELECT store_id, happened_at_five, happened_at_one, DATEDIFF(happened_at_five, happened_at_one) AS days_difference
                                                                    FROM Transaction_five_one 
                                                                )
                                                                SELECT AVG(days_difference) AS average_time_days
                                                                FROM DaysDifference;
                                                        """ 

cursor.execute(average_time_for_store_perform_five_first_transactions)

with open("/Users/texiagonzalezcaceres/Desktop/sum_up_test/queries_results/average_time_for_store_perform_five_first_transactions.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

conn.commit()
cursor.close()
conn.close()
