# Instaork demo application README

## Getting Started

### Prerequisites

set up the local environment using the requirements.txt file

Fist create a virtual environment using

```
python3 -m myvenv
```

```
source myvenv/bin/activate
```

```
pip3 install -r instawork/requirements.txt
```

apply migrations using

```
python3 manage.py migrate
```

run server at local host 8000 using

```
python3 manage.py runserver
```

Alternatively you can run the setup.sh script that I created, which does all the above mentioned things

```
python3 -m myvenv
source myvenv/bin/activate
chmod a+x setup.sh
./setup.sh
```

## Testing

You can go to sign up page using http://localhost:8000/teams/ or http://localhost:8000/teams/signup and
login using http://localhost:8000/teams/login

## admin user however can make another user admin