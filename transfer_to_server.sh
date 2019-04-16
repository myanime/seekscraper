PROJECT_DIR='/Users/ryan/repos/seekscraper'
AWS_KEY="/Users/ryan/.ssh/aws_schlupfi.pem"
cp * /home/myanime/seekscraper/static/output/backup/
scp -i $AWS_KEY -r $PROJECT_DIR/static/output/transfer/* ubuntu@52.59.254.43:./countries/seek
rm $PROJECT_DIR/static/output/transfer/*