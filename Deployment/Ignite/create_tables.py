from pyignite import Client

client = Client()
client.connect('127.0.0.1', 10800)
PRODUCT_CREATE_TABLE = '''
create table product(
	product_id VARCHAR PRIMARY KEY,
	product_url VARCHAR
)
'''
client.sql(PRODUCT_CREATE_TABLE)
SIMILARPRODUCTS_CREATE_TABLE = '''
create table similarproducts(
	product_id VARCHAR ,
	similar_product_id VARCHAR ,
	similariy_score DOUBLE ,
	PRIMARY KEY (product_id, similar_product_id)
) WITH "affinityKey=similar_product_id"
'''
client.sql(SIMILARPRODUCTS_CREATE_TABLE)

PRODUCT_INSERT_QUERY = '''
insert into product values (? , ?)
'''
SIMILARPRODUCTS_INSERT_QUERY = '''
insert into similarproducts values (? , ?, ?)
'''

# Code for inserting dummy data
INSERT_PRODUCT_DATA= []
for i in range(10000) :
	INSERT_PRODUCT_DATA.append( [str(i),str(i)] )

for row in INSERT_PRODUCT_DATA :
	client.sql(PRODUCT_INSERT_QUERY, query_args=row)


INSERT_SIMILARPRODUCT_DATA= []
for i in range (0, 10000, 3) :
	for j in range(i, 10000, 7) :
		if(i+j < 10000) :
			INSERT_SIMILARPRODUCT_DATA.append([str(i), str(j), ( i*j / 10000 )])
		else :
			break


for row in INSERT_SIMILARPRODUCT_DATA :
	client.sql(SIMILARPRODUCTS_INSERT_QUERY,  query_args=row)