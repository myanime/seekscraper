#LOCALVERSION
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
sleep 2
scrapy crawl seek_2 -o $MYPATH/$COUNTRY/static/output/2$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_3 -o $MYPATH/$COUNTRY/static/output/3$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_4 -o $MYPATH/$COUNTRY/static/output/4$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_5 -o $MYPATH/$COUNTRY/static/output/5$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_6 -o $MYPATH/$COUNTRY/static/output/6$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_7 -o $MYPATH/$COUNTRY/static/output/7$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_8 -o $MYPATH/$COUNTRY/static/output/8$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_9 -o $MYPATH/$COUNTRY/static/output/9$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_10 -o $MYPATH/$COUNTRY/static/output/10$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_11 -o $MYPATH/$COUNTRY/static/output/11$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_12 -o $MYPATH/$COUNTRY/static/output/12$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_13 -o $MYPATH/$COUNTRY/static/output/13$CURRENT_FILENAME.json
sleep 2
scrapy crawl seek_14 -o $MYPATH/$COUNTRY/static/output/14$CURRENT_FILENAME.json
sleep 2

cd $MYPATH/$COUNTRY/static/output
sudo python deduplicate.py
sleep 5
cd $MYPATH/$COUNTRY/static/output/transfer
sudo gzip *.*
sudo mv *.* /$MYPATH/transfer/$COUNTRY
scp -i $MYPATH/.ssh/aws_schlupfi.pem -r $MYPATH/transfer/$COUNTRY/* ubuntu@54.93.163.4:./countries/$COUNTRY
