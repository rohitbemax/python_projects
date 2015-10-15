import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

codeList = r.smembers("redis_test_list")
print("Total no of items: " + str(len(codeList)))
itemSum = 0
for item in codeList:
	itemSum = itemSum + int(r.hget(item, "customer_hash"))

print("Total Number of Customers: " + str(itemSum))
