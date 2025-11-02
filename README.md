# honey-drop-api
API for Honey Drop

## Notes

- Command to create an admin user <br>
`python manage.py createsuperuser --name Admin --username admin@honeydrop.com --role admin --email admin@honeydrop.com`

- Command to capture migration<br>
`python manage.py makemigrations`

- Command to migrate <br>
`python manage.py migrate`

- Command to login to server
- `ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102`

- Command to copy files to server (D:\PWork\AquaFlow\honey-drop-api\app)
- `scp -i "C:\Users\Shameer\logistics" -r . root@88.222.245.102:/root/home/honey-drop-lms/honey-drop-backend/`

- Command to clear residue files
- `ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "find /root/home/honey-drop-lms/honey-drop-backend/ -type f ! -name 'Dockerfile' ! -name '*.py' ! -name '*.txt' | xargs rm"`


- Command to clear residue files & build app
- `ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "cd /root/home/honey-drop-lms/ && docker compose build"`

- Command to ShutDown app
- `ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "cd /root/home/honey-drop-lms/ && docker compose down"`
- 
- Command to Deploy app
- `ssh -i "C:\Users\Shameer\logistics" root@88.222.245.102 -t "cd /root/home/honey-drop-lms/ && docker compose up -d"`