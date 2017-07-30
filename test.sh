CURRENT_FILENAME=seek
MYDATE=$(date +"%d_%m_%Y")
MYPATH=/home/media
COUNTRY=seek
cd $MYPATH/$COUNTRY/static/
date +%d-%m-%Y_%H:%M > date
echo Starting_Scrapy
cd $MYPATH/$COUNTRY/
echo "DELETING STUFF"
mkdir $MYPATH/$COUNTRY/static/output/transfer
mkdir $MYPATH/$COUNTRY/static/output/history
sleep 5
export DISPLAY=:1
scrapy crawl seek -o $MYPATH/$COUNTRY/test.json
sleep 2
