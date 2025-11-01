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