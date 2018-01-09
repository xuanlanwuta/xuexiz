import time

def shij(fc):
	def kan_shi():
		a = time.time()
		fc()
		b = time.time()
		print("函数%s运行的时间是%s" % (fc.__name__, str(b-a)))
	return kan_shi

@shij
def ceshi():
	time.sleep(1)
	print("---------")

ceshi()