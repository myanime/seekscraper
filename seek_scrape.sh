echo "start:" >> ./runcounter
date >> ./runcounter
CURRENT_FILENAME=seek
MYDATE=$(date +"%d_%m_%Y")
MYPATH=/home/ubuntu
COUNTRY=seek
cd $MYPATH/$COUNTRY/static/
date +%d-%m-%Y_%H:%M > date
sleep 5
echo Starting_Scrapy
cd $MYPATH/$COUNTRY/
echo "DELETING STUFF"
mkdir $MYPATH/$COUNTRY/static/output/transfer
mkdir $MYPATH/$COUNTRY/static/output/history
mv $MYPATH/$COUNTRY/static/output/seek.json $MYPATH/$COUNTRY/static/output/history/backup_$MYDATE.json
rm $MYPATH/$COUNTRY/static/output/joblist
rm $MYPATH/$COUNTRY/static/output/seek.json
sleep 5
scrapy crawl joblist -s DNS_TIMEOUT=3 -s DOWNLOAD_TIMEOUT=5 -o $MYPATH/$COUNTRY/static/output/joblist.csv
sleep 5
mv $MYPATH/$COUNTRY/static/output/joblist.csv $MYPATH/$COUNTRY/static/output/joblist2.csv
sed 's/\"//g' $MYPATH/$COUNTRY/static/output/joblist2.csv > $MYPATH/$COUNTRY/static/output/joblist.csv
rm $MYPATH/$COUNTRY/static/output/joblist2.csv
sleep 5
python salarydedupe.py
mv $MYPATH/$COUNTRY/static/output/joblist.csv $MYPATH/$COUNTRY/static/output/joblist
sleep 5
xvfb-run scrapy crawl seek -o $MYPATH/$COUNTRY/static/output/$CURRENT_FILENAME.json
sleep 2
cd $MYPATH/$COUNTRY/static/output
python deduplicate.py
sleep 5
cd $MYPATH/$COUNTRY/static/output/transfer
gzip *.*
mv *.* /$MYPATH/countries/$COUNTRY
#scp -i /home/myanime/.ssh/aws_schlupfi.pem -r $MYPATH/transfer/$COUNTRY/* ubuntu@52.59.254.43:./countries/$COUNTRY
#scp -i $MYPATH/.ssh/aws_schlupfi.pem -r $MYPATH/transfer/$COUNTRY/* ubuntu@52.59.254.43:./countries/$COUNTRY
sleep 10
cd $MYPATH/$COUNTRY/
echo "stop:" >> ./runcounter
date >> ./runcounter
sleep 10
sudo reboot now
