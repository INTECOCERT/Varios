Repositorio para pequeñas pruebas de concepto, programas y scripts varios.

Contenidos actuales:

*crawl_certs/*
* crawl_certs.py: Pequeño script en Python para recuperar los certificados digitales presentados por los sitios web especificados en el fichero recibido como parámetro, y devolver los valores de sigAlgo, notBefore y notAfter.
* crawl_certs.sh: Pequeño script en Bash, con la misma funcionalidad que el script crawl_certs.py.
* process.sh:	Pequeño script en Bash + AWK para procesar los datos producidos por los scripts anteriores.

*stego/*
* imgrand.py: Script en python para aleatorizar el porcentaje indicado de pixeles de la imagen recibida como parametro. Ejecutar sin parámetros para obtener un menú de ayuda.
* imgchi2.py: Script para aplicar un estegoanálisis Chi cuadrado sobre la imagen recibida como parámetro. Ejecutar sin parámetros para obtener un menú de ayuda.
