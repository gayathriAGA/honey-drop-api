echo "Bringing down existing containers..."
ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "cd /root/home/honey-drop-lms/ && docker compose down"
echo "Uploading new code to server..."
scp -i "C:\Users\Shameer\logistics" -r . root@88.222.245.102:/root/home/honey-drop-lms/honey-drop-backend/
ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "find /root/home/honey-drop-lms/honey-drop-backend/ -type f ! -name 'Dockerfile' ! -name '*.py' ! -name '*.txt' | xargs rm"
echo "Building and bringing up new containers..."
ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "cd /root/home/honey-drop-lms/ && docker compose build"
ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "cd /root/home/honey-drop-lms/ && docker compose up -d"