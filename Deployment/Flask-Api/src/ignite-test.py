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

PRODUCT_INSERT_QUERY = '''
insert into product values (? , ?)
'''
INSERT_DATA= []
for i in range(10) :
	INSERT_DATA.append( [str(i),str(i)] )

for row in INSERT_DATA :
	client.sql(PRODUCT_INSERT_QUERY, query_args=row)

PRODECT_SELECT_QUERY = '''
select * from product 
'''
result = client.sql(PRODECT_SELECT_QUERY, include_field_names=True)
returnList = []
for i,row in enumerate(result):
	if i == 0 :
		field_names = row
	else :
		newDict = {}
		for j,f in enumerate(field_names) : 
			newDict[f] = row[j]
		returnList.append(newDict)
SIMILAR_PRODUCTS_QUERY = '''
select product.product_id, product.product_url from similarproducts
JOIN product on similarproducts.similar_product_id = product.product_id
where similarproducts.product_id = ? 
'''
SIMILAR_PRODUCTS_ARGS = ['1']
result = client.sql(SIMILAR_PRODUCTS_QUERY, query_args=SIMILAR_PRODUCTS_ARGS, include_field_names=True)
returnList = []
for i,row in enumerate(result):
	if i == 0 :
		field_names = row
	else :
		newDict = {}
		for j,f in enumerate(field_names) : 
			newDict[f] = row[j]
		returnList.append(newDict)