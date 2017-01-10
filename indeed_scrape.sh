CURRENT_FILENAME=new_jobs
MYDATE=$(date +"%d_%m_%Y")
MYPATH=/home/ubuntu
COUNTRY=seek
cd $MYPATH/$COUNTRY/static/
date >> ./runcounter
date +%d-%m-%Y_%H:%M > date
sleep 5
echo Starting_Scrapy
cd $MYPATH/$COUNTRY/
scrapy crawl seek_1 -o $MYPATH/$COUNTRY/static/output/1$CURRENT_FILENAME.json
sleep 15
scrapy crawl seek_2 -o $MYPATH/$COUNTRY/static/output/2$CURRENT_FILENAME.json
sleep 15
scrapy crawl seek_3 -o $MYPATH/$COUNTRY/static/output/3$CURRENT_FILENAME.json
sleep 10
cd $MYPATH/$COUNTRY/static/output
sudo python deduplicate.py
sleep 5
cd $MYPATH/$COUNTRY/static/output/transfer
sudo gzip *.*
sudo mv *.* /$MYPATH/transfer/$COUNTRY
scp -i $MYPATH/.ssh/aws_schlupfi.pem -r $MYPATH/transfer/$COUNTRY/* ubuntu@54.93.163.4:./countries/$COUNTRY
