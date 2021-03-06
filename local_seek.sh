echo "start:" >> ./runcounter
date >> ./runcounter
#PROJECT_DIR='/Users/ryan/repos/seekscraper'
#AWS_KEY="/Users/ryan/.ssh/aws_schlupfi.pem"
PROJECT_DIR='/home/myanime/seekscraper'
AWS_KEY="/home/myanime/.ssh/aws_schlupfi.pem"
MYDATE=$(date +"%d_%m_%Y")

cd $PROJECT_DIR/static/
date +%d-%m-%Y_%H:%M > date
sleep 5

echo Starting_Scrapy
cd $PROJECT_DIR/
echo "DELETING STUFF"
#mv /home/myanime/seekscraper/job_ids.txt /home/myanime/seekscraper/job_ids$MYDATE.txt
#touch /home/myanime/seekscraper/job_ids.txt
mkdir $PROJECT_DIR/static/output/transfer
mkdir $PROJECT_DIR/static/output/history
mv $PROJECT_DIR/static/output/seek.json $PROJECT_DIR/static/output/history/backup_$MYDATE.json
rm $PROJECT_DIR/static/output/seek.json
sleep 5
scrapy crawl seek -o $PROJECT_DIR/static/output/seek.json
sleep 2
cd $PROJECT_DIR/static/output
python deduplicate.py
sleep 5
cd $PROJECT_DIR/static/output/transfer
gzip /home/myanime/seekscraper/static/output/transfer/*.*
cp * $PROJECT_DIR/static/output/backup/
scp -i $AWS_KEY -r $PROJECT_DIR/static/output/transfer/* ubuntu@52.59.254.43:./countries/seek
rm $PROJECT_DIR/static/output/transfer/*
