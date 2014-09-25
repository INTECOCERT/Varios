#!/bin/bash

function get_url_cert_data {

	time=$1
	curl=$2

	tmp=`timeout $time openssl s_client -connect $curl:443 < /dev/null 2>/dev/null | \
		openssl x509 -noout -text 2>/dev/null | tee | grep "Signature Algorithm\|Not Before\|Not After" | \
               	sed -e "s/\s\{2,\}/ /g" | sed -e "s/^\s//g"`

	sigAlgo=`echo "$tmp" | grep "Signature Algorithm" | sort | uniq | sed "s/:\s/;/g" | cut -d\; -f2`
	notBefore=`echo "$tmp" | grep "Not Before" | sed "s/:\s/;/g" | cut -d\; -f2`
	notBefore=`date -d "$notBefore" "+%s"`
	notAfter=`echo "$tmp" | grep "Not After" | sed "s/:\s/;/g" | cut -d\; -f2`
	notAfter=`date -d "$notAfter" "+%s"`

}

if [ $# != 2 ]; then
	echo "Usage: $0 <URLs file> <timeout>"
	exit 1
fi

file=$1
timeout=$2

# Read the urls from the input file
echo -e "#URL\tsigAlgo\tnotBefore\tnotAfter"
while read line; do
	
	# Try to connect to the URL
	url=$line

	# Get cert data
	get_url_cert_data $timeout $url
	if [[ $sigAlgo == '' ]]; then
		echo -e "$url\tN/A\tN/A\tN/A"
	else
		echo -e "$url\t$sigAlgo\t$notBefore\t$notAfter"
	fi

done < $file
