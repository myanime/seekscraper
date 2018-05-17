echo "start:" >> ./runcounter
date >> ./runcounter
CURRENT_FILENAME=seek
MYDATE=$(date +"%d_%m_%Y")
MYPATH=/home/myanime
COUNTRY=seekscraper
cd $MYPATH/$COUNTRY/static/
date +%d-%m-%Y_%H:%M > date
sleep 5
echo Starting_Scrapy
cd $MYPATH/$COUNTRY/
echo "DELETING STUFF"
mkdir $MYPATH/$COUNTRY/static/output/transfer
mkdir $MYPATH/$COUNTRY/static/output/history
mv $MYPATH/$COUNTRY/static/output/seek.json $MYPATH/$COUNTRY/static/output/history/backup_$MYDATE.json
rm $MYPATH/$COUNTRY/static/output/seek.json
sleep 5
scrapy crawl seek -o $MYPATH/$COUNTRY/static/output/$CURRENT_FILENAME.json
sleep 2
cd $MYPATH/$COUNTRY/static/output
python deduplicate.py
sleep 5
cd $MYPATH/$COUNTRY/static/output/transfer
gzip *.*
scp -i /home/media/.ssh/aws_schlupfi.pem -r $MYPATH/$COUNTRY/static/output/transfer/* ubuntu@52.59.254.43:./countries/seek
rm $MYPATH/$COUNTRY/static/output/transfer/*