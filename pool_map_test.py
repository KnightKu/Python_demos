#from multiprocessing.dummy import Pool as ThreadPool 
from multiprocessing import Pool
import time

print time.time()
def test(url):
	print url
 
urls = [
        'http://www.python.org', 
        'http://www.python.org/about/',
        'http://www.python.org/about/',
        'http://www.python.org/about/',
        # etc.. 
        ]
 
# Make the Pool of workers
pool = Pool(6)
# Open the urls in their own threads
# and return the results
results = pool.map(test, urls)
print results
#close the pool and wait for the work to finish 
pool.close() 
pool.join()
print time.time()
