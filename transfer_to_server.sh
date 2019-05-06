PROJECT_DIR='/home/myanime/seekscraper'
AWS_KEY="/home/myanime/.ssh/aws_schlupfi.pem"
cp * /home/myanime/seekscraper/static/output/backup/
scp -i $AWS_KEY -r $PROJECT_DIR/static/output/transfer/* ubuntu@52.59.254.43:./countries/seek
rm $PROJECT_DIR/static/output/transfer/*
