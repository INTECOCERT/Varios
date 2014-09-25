#!/usr/bin/env python

import sys
import re
import OpenSSL
import ssl
# SSLv2 is not available if OpenSSL is compiled with OPENSSL_NO_SSL2_flag
from ssl import PROTOCOL_SSLv3, PROTOCOL_SSLv23, PROTOCOL_TLSv1
import urllib2
import signal
import dateutil.parser
import calendar

class TimeoutException(Exception):
	"Indicates that the function has taken too long."
	
def handle_timeout(*args):
	raise TimeoutException(*args)

def usage():
	print "%s <seed file> [<time out>]" % sys.argv[0]

def check_url(url):

	# regex based in http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
	regex = re.compile(
        	r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
	        r'localhost|' #localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?' # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	found = regex.search(url)

	if found != None:
		return True

	return False

def get_cert(url, to):

	try:

		# Try connecting with PROTOCOL_SSLv3 
		signal.alarm(to)
		cert = ssl.get_server_certificate((url, 443), PROTOCOL_TLSv1)
		signal.alarm(0) # Cancel timeout
		return cert

	except TimeoutException as e:

		# A timeout means that SSL is not at all supported, so we do not
		# even try to connect using other versions of SSL
		raise(e)

	except:

		try: 
			# Try connecting with PROTOCOL_SSLv23
			signal.alarm(to)
			cert = ssl.get_server_certificate((url, 443), ssl_version=PROTOCOL_SSLv3)
			signal.alarm(0) # Cancel timeout
			return cert

		except TimeoutException as e:
			raise(e)

		except:

			try: 

				# Try connecting with PROTOCOL_TLSv1
				signal.alarm(to)
				cert = ssl.get_server_certificate((url, 443), ssl_version=PROTOCOL_SSLv23)
				signal.alarm(0) # Cancel timeout
				return cert

			except TimeoutException as e:
				raise(e)

			except Exception as e:
				raise(e)

	return None


def pring_cert_data(url, cert = None):

	# Get the algorithms of the certificate
	if cert : 
		x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
		algo = x509.get_signature_algorithm()
		notBefore = calendar.timegm(dateutil.parser.parse(x509.get_notBefore()).utctimetuple())
		notAfter = calendar.timegm(dateutil.parser.parse(x509.get_notAfter()).utctimetuple())
		print "%s %s %s %s" % (url, algo, notBefore, notAfter)


def main(argv):

	if len(argv) < 1:
		usage()
		sys.exit(1)

	# Sole argument is the file with the URL seeds
	seed = argv[0]

	if len(argv) == 2:
		to = int(argv[1])
	else:
		to = 1

	# Store each line in the file in the urls array
	with open(seed) as f:
		urls = f.readlines()

	# Prepare timeout function
	signal.signal(signal.SIGALRM, handle_timeout)

	# Go through all the urls and, if SSL, try to establish a connection
	print "#URL\tsigAlgo\tnotBefore\tnotAfter"
	for url in urls:

		# Try https://www.url.dom
		if check_url(url[:-1]):

			try:
				cert = get_cert(url[:-1], to)
				pring_cert_data(url[:-1], cert)

			except TimeoutException:
				print "%s CONN_TIMEOUT" % url[:-1]

			except:
				print "%s SSL_ERROR" % url[:-1]

		else:
			print "%s NOT VALID" % url[:-1]
			
		sys.stdout.flush()


if __name__ == "__main__":
	main(sys.argv[1:])
