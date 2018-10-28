dirname ${BASH_SOURCE[0]}

for i in {0..9}; do
	openssl genrsa 2048 > private$i.pem;
	dd if=/dev/urandom of=data$i.enc bs=256 count=1
done

PADS=(-oaep -ssl -pkcs)

PAD=${PADS[$RANDOM % ${#PADS[@]} ]}
echo "PAD: $PAD"
echo "Some message" | openssl rsautl -inkey private$[ $RANDOM % 10 ].pem $PAD -encrypt > data$[ $RANDOM % 10 ].enc

../combobreaker.py -v -c -z openssl rsautl -inkey [ private*.pem ] -decrypt -in [ data*.enc ] [ -ssl -pkcs -oaep ]
