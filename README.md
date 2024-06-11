# sumup_technical_assessment

## General info
This project was created as solution for Technical Assessment - Analytics Engineer (SumUp)

## Technical Test 
The goal of this technical test is to showcase an end to end ELT pipeline from a data source to any data warehouse using Python, SQL and DBT and data models to answer the following questions 

	•	Top 10 stores per transacted amount
	•	Top 10 products sold
	•	Average transacted amount per store typology and country
	•	Percentage of transactions per device type
	•	Average time for a store to perform its 5 first transactions


Deliverables: 
- Please share the source code, data model design, SQLs to answer the above questions via public git repository including a README file explaining your assumptions, design and solution implementation details.

*Usage of pandas libraries and python notebooks are not permitted and for any data manipulations please use SQL

Assumptions:

	•	Each of our customers have one or multiple stores, which are physical locations where their business happens, those stores are classified by different typology. 
	•	We also provide them with different types of devices (1 to 5), those devices are hardware needed to perform any kind of transactions, each of them are tied up to a specific store. 
	•	A transaction is a payment made using the provided devices, currently our devices only handle payments made by card and in euros. Those transactions are made to pay for products sold inside the store, each product has a name and a SKU (stock keeping unit) which is unique.
	•	Everyday, our customer’s customers walk into their favorite stores to buy products and pay for them using the devices that we provide.

We now want to target customers that will use our devices efficiently and benefit the most from our product. That’s why we need to answer the above questions to know which stores, products and devices are the most efficient and also to know how long it takes for a store to adopt our devices.

In order to solve this problem, we have provided the following three datasets in csv format
	•	Stores
	•	Devices
	•	Transactions


* The dataset supplied with this test contains only sample data. Your design and implementation should scale for larger volumes of data (millions to billions records)

## Technologies
* MySql
* Python

## Setup
To run this project, you require to install:
* Python
* MySql 
* Code editor of your preference

## After setup:
* pip install mysql-connector-python

## Solution implementation

This challenge is a ETL development (Extract Transform Load), a specific database conecction is not provided, but instead three xlsx file [device, store, transaction].

* In first step I converted xlsx files to csv just renaming extension file.
* I decide to work with MySql, creating an instance using:
```
brew install mysql
```
* Decide to work just with root user.
* Creation of tables to use [device, store, transaction_store]:
```
CREATE TABLE DEVICE (
  id int NOT NULL,
  type int,
  store_id int,
  PRIMARY KEY (id),
  KEY store_id (store_id)
)
```
```
CREATE TABLE STORE (
  id int NOT NULL,
  name varchar(255),
  address varchar(255),
  city varchar(255),
  country varchar(255),
  created_at datetime,
  typology varchar(255),
  customer_id int,
  PRIMARY KEY (id)
)
```
```
CREATE TABLE TRANSACTION_STORE (
  id int NOT NULL,
  device_id int,
  product_name varchar(255),
  product_sku varchar(255),
  category_name varchar(255),
  amount int,
  status varchar(255),
  card_number varchar(255),
  cvv int,
  created_at datetime,
  happened_at datetime,
  PRIMARY KEY (id),
  KEY device_id (device_id)
)

```
* I created a script to handle format datetime, data default format "%m/%d/%Y %H:%M:%S", this replace the format data and overwrite the file data
```
convert_data.py
```
* To work with data you need data! I filled tables with another script, this is just one of many ways to do it:
```
fill_tables.py
```
* Having the connection, tables formatted data and tables filled, I created the queries necessaries to answer this technical assessment, and decided to deliver results saving it in csv files:
```
queries.py
```
* And just to try to do some things in one step, I created:
```
run_scripts.py
```

## Executing the solution
* For you connection replace for you credentials in any file used:
```
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sumup_test"
)
```
* First way, you can run:
```
#remember use your python version
python3 run_scripts.py
```
* Second way, just run the queries to get the results:
```
#remember use your python version
python3 queries.py
```
* Reminder, modify where you want save your results, modifying queries.py:
```
#replace thw location on the file system, you cant use pwd command in terminal to print your working directory
with open("/Users/anotheruser/Desktop/sum_up_test/queries_results/average_time_for_store_perform_five_first_transactions.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)
```

## Diagrams

![sumup_test_mysql](https://github.com/texgc/sumup_technical_assessment/assets/167104799/15be3645-a03a-4f45-b6bf-5f29455d6667)

  
![sumup_test_mysql_fk](https://github.com/texgc/sumup_technical_assessment/assets/167104799/6970e0d7-bfcb-495e-8f23-e2021b6cde0a)

## Let's talk about results
#### Top 10 products sold
Always work with product_sku because is correct way to access to his unique reference of a product. It's neccesary clarify business rules for this question, if we digg into data we can get that every transction is associated to a status with handle multiples options [cancelled, refused, accepted], depends on what we are looking for we can filter by the status. For this specific case result was taken with all status options [cancelled, refused, accepted], products that transactions was cancelled, refused or accepted.

| product_name   | product_sku   | total_sold_amount |
| -------------- | ------------- | ----------------- |
| sit amet       | 3770009015075 | 1688              |
| ridiculus mus. | 3770009015042 | 1600              |
| est ac         | v3770009015028| 1564              |
| ridiculus mus. | 3770009015233 | 1361              |
| fringilla mi   | 3770009015043 | 1340              |
| dui, nec       | 3770009015074 | 1327              |
| Duis dignissim | 3770009015233 | 1282              |
| lorem semper   | 3770009015004 | 1265              |
| ornare lectus  | 3770009015044 | 1265              |
| diam vel       | 3770009015073 | 1249              |

#### Top 10 stores per transacted amount
Working with id because is correct way to access to get stores names. It's neccesary clarify business rules for this question, if we digg into data we can get that every transction is associated to a status with handle multiples options [cancelled, refused, accepted], depends on what we are looking for we can filter by the status. For this specific case result was taken with all status options [cancelled, refused, accepted], considering all transactions amount that was cancelled, refused or accepted.

| store_id | store_name                          | total_transacted_amount |
| -------- | ----------------------------------- | ----------------------- |
| 97       | Sem Ut Cursus Corp.                 | 26230                   |
| 60       | Eleifend Cras Institute             | 26206                   |
| 3        | Nec Ante Ltd                        | 26047                   |
| 19       | Magnis Dis Inc.                     | 18851                   |
| 51       | Mauris Aliquam PC                   | 18193                   |
| 46       | Integer Mollis Integer Foundation   | 17199                   |
| 8        | In LLP                              | 16434                   |
| 74       | Dolor Nonummy Ac Inc.               | 15644                   |
| 75       | Erat Neque Foundation               | 14835                   |
| 92       | Tempus Mauris Ltd                   | 14755                   |

#### Average transacted amount per store typology and country
Working with id because is correct way to access to get stores names. It's neccesary clarify business rules for this question, if we digg into data we can get that every transction is associated to a status with handle multiples options [cancelled, refused, accepted], depends on what we are looking for we can filter by the status. For this specific case result was taken with all status options [cancelled, refused, accepted], considering all transactions amount that was cancelled, refused or accepted.

| store_id | typology   | country       | average_transacted_amount |
| -------- | ---------- | ------------- | ------------------------- |
| 99       | Beauty     | New Zealand   | 523.2857                  |
| 3        | FoodTruck  | Costa Rica    | 510.7255                  |
| 61       | Service    | Ukraine       | 476.0588                  |
| 51       | Other      | Germany       | 551.3030                  |
| 29       | Restaurant | South Africa  | 502.8571                  |
| 70       | Press      | Belgium       | 538.5500                  |
| 97       | FoodTruck  | France        | 437.1667                  |
| 75       | Hotel      | New Zealand   | 593.4000                  |
| 19       | Press      | Netherlands   | 554.4412                  |
| 27       | Florist    | South Korea   | 567.5500                  |
| 28       | Hotel      | Canada        | 399.3889                  |
| 73       | Beauty     | Ireland       | 521.3600                  |
| 46       | Service    | South Africa  | 554.8065                  |
| 87       | Press      | Belgium       | 467.5000                  |
| 38       | Restaurant | Nigeria       | 522.4375                  |
| 8        | Other      | Indonesia     | 586.9286                  |
| 21       | Press      | Mexico        | 538.6296                  |
| 69       | Beauty     | Netherlands   | 467.7000                  |
| 65       | Beauty     | South Africa  | 455.8710                  |
| 98       | Beauty     | Norway        | 524.6923                  |
| 56       | Press      | Netherlands   | 426.8824                  |
| 30       | Florist    | Austria       | 684.8571                  |
| 77       | FoodTruck  | Ukraine       | 461.3000                  |
| 36       | Other      | Singapore     | 351.6154                  |
| 58       | Service    | Germany       | 397.0000                  |
| 95       | Restaurant | Sweden        | 459.3793                  |
| 57       | Restaurant | Netherlands   | 506.2759                  |
| 76       | Service    | United Kingdom| 523.5333                  |
| 60       | Florist    | Indonesia     | 459.7544                  |
| 78       | Other      | Indonesia     | 479.0000                  |
| 35       | Press      | Indonesia     | 423.5000                  |
| 84       | Restaurant | India         | 490.0588                  |
| 59       | Beauty     | Brazil        | 440.7000                  |
| 34       | FoodTruck  | Austria       | 435.5789                  |
| 74       | Press      | Poland        | 422.8108                  |
| 52       | Beauty     | Italy         | 418.9375                  |
| 92       | Florist    | France        | 526.9643                  |
| 31       | Beauty     | Brazil        | 590.2632                  |
| 24       | FoodTruck  | United Kingdom| 472.7000                  |
| 53       | FoodTruck  | India         | 603.8333                  |
| 44       | Press      | Chile         | 284.7500                  |
| 82       | Florist    | Brazil        | 463.8065                  |
| 17       | Florist    | Singapore     | 494.5000                  |
| 39       | Restaurant | South Korea   | 384.8750                  |
| 79       | FoodTruck  | Australia     | 553.7391                  |
| 45       | Beauty     | Vietnam       | 532.5455                  |
| 49       | Press      | Netherlands   | 481.0000                  |
| 42       | Press      | Brazil        | 461.9583                  |
| 91       | Other      | Germany       | 574.3000                  |
| 25       | Restaurant | Colombia      | 737.0000                  |
| 93       | Service    | Australia     | 363.0000                  |
| 47       | Other      | Peru          | 531.1000                  |
| 26       | Beauty     | Nigeria       | 447.2273                  |
| 62       | Hotel      | United States | 328.5000                  |
| 10       | Other      | India         | 566.8000                  |
| 64       | Press      | Peru          | 444.4583                  |
| 9        | Service    | Belgium       | 476.8095                  |
| 88       | Beauty     | Nigeria       | 459.7143                  |
| 68       | Press      | Peru          | 573.6364                  |
| 7        | Service    | Mexico        | 568.7500                  |
| 12       | Florist    | Australia     | 493.9600                  |
| 55       | Service    | Brazil        | 637.1538                  |
| 86       | Service    | India         | 462.0000                  |
| 1        | Florist    | Belgium       | 595.7000                  |
| 13       | FoodTruck  | France        | 422.0000                  |
| 80       | Hotel      | Netherlands   | 483.0588                  |
| 4        | Hotel      | Nigeria       | 700.4000                  |
| 41       | Other      | Spain         | 343.6250                  |
| 67       | Beauty     | Austria       | 583.1667                  |
| 71       | Press      | United Kingdom| 519.2500                  |
| 50       | Other      | France        | 615.8571                  |
| 37       | Hotel      | China         | 465.2857                  |
| 23       | Hotel      | Italy         | 526.7778                  |
| 63       | Restaurant | Austria       | 550.3636                  |
| 89       | Beauty     | United States | 521.0000                  |
| 85       | Hotel      | Ireland       | 472.4211                  |
| 90       | FoodTruck  | Nigeria       | 339.5714                  |
| 96       | Hotel      | China         | 597.6667                  |
| 5        | Restaurant | Ireland       | 465.7143                  |
| 16       | Hotel      | Costa Rica    | 497.0000                  |
| 72       | Florist    | China         | 527.9333                  |
| 18       | FoodTruck  | South Africa  | 85.0000                   |
| 20       | Service    | Singapore     | 438.0769                  |
| 11       | Florist    | Brazil        | 490.6000                  |
| 6        | FoodTruck  | India         | 557.0000                  |
| 22       | Press      | Netherlands   | 486.2857                  |
| 83       | Hotel      | Belgium       | 450.5000                  |

#### Percentage of transactions per device type
If we digg into data we can get that every transction is associated to a status with handle multiples options [cancelled, refused, accepted], depends on what we are looking for we can filter by the status. For this specific case results are considering all type of transactions, cancelled, refused or accepted.

| type | transaction_count | percentage_of_transactions |
| ---- | ----------------- | -------------------------- |
| 1    | 326               | 21.73                      |
| 3    | 306               | 20.40                      |
| 4    | 350               | 23.33                      |
| 5    | 262               | 17.47                      |
| 2    | 256               | 17.07                      |

#### Average time for a store to perform its 5 first transactions
If we digg into data we can get that every transction is associated to a status with handle multiples options [cancelled, refused, accepted], depends on what we are looking for we can filter by the status. For this specific case results are considering all type of transactions, cancelled, refused or accepted, also just stores with five or more transactions are considerated, stores with less of five transactions were not considerated. Results are reflected on days.

| average_time_days |
| ----------------- |
| 149.5185         |
