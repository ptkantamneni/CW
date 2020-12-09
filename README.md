# CW - Hackathon


To run the backend:

``` 
  mkdir venv
  cd venv
  python3 -m venv .
  cd ..
  source venv/bin/activate 
  pip3 install -r requirements.txt
  python3 api.py
```

Once the initial venv is setup as detailed above, you may run only:

```
  pip3 install -r requirements.txt
```

as necessary to get updated libraries as the team adds them in.


The python postgres library for versions python 3.3+ (we are using 3.9) is: https://github.com/tlocke/pg8000


export FLASK_APP=api.py
