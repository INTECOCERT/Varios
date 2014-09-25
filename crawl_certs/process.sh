#!/bin/bash

if [ $# != 1 ] && [ $# != 2 ]; then
	echo "Usage $0 <input file> [pie]"
	exit 1
fi

input=$1

if [ $# == 2 ]; then
	plot=$2
else
	plot="0"
fi

awk -v plot=$plot '

	BEGIN {
		ts_20160101 = mktime("2016 01 01 00 00 00");
		ts_20170101 = mktime("2017 01 01 00 00 00");
	}

	!/^#/ {

		algo[$2]++;

		# If successful connection
		if ($2 != "CONN_TIMEOUT" && $2 != "SSL_ERROR" && $2 != "N/A") {

			success++

			if (toupper($2) ~/SHA1/) {
				sha1total++;
			}

			# expiration > ts_20160101 && algo == SHA1
			if (toupper($2) ~ /SHA1/ && $4 > ts_20160101) {
				after2016++;
			}

			# expiration > ts_20170101 && algo == SHA1
			if (toupper($2) ~ /SHA1/ && $4 > ts_20170101) {
				after2017++;
			}

		}

		total++;
	}

	END {

		# Print summary of algos

		if (plot == "pie") {

			for (x in algo) {
				if (x != "CONN_TIMEOUT" && x != "SSL_ERROR" && x != "N/A") {
					printf("%s ", x);
				}
			}
			printf("\n");

			for ( x in algo) {
				if (x != "CONN_TIMEOUT" && x != "SSL_ERROR" && x != "N/A") {
					printf("%.2f ", algo[x]/success);
				}
			}
			printf("\n");

			printf("01/01/2016 01/01/2017 2017+\n");
			printf("%.2f %.2f %.2f\n", after2016/sha1total, after2017/sha1total, (sha1total-after2016-after2017)/sha1total);

		} else {

			printf("\n####################################################\n");
			printf("# Total connections tried: %d                     #\n", total);
			printf("# Number of successful connections: %d (%.2f%)   #\n", success, success/total*100);
			printf("# Certs with sha1 expiring > 20160101: %d (%.2f%) #\n", after2016, after2016/sha1total*100);
			printf("# Certs with sha1 expiring > 20170101: %d (%.2f%)  #\n", after2017, after2017/sha1total*100);
			printf("####################################################\n");

			for (x in algo) {
				if (x != "CONN_TIMEOUT" && x != "SSL_ERROR" && x != "N/A") {
					printf("%s %s %.2f%\n", x, algo[x], (algo[x]/success)*100);
				}
			}
			printf("\n");
		}

	}
' $input
