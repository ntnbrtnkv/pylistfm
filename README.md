# PyListFm

Create local playlist from remote music tops

It requires python 3 version. To install all libraries type in terminal (python should be installed):

```bash
$ pip install -r requirements.txt
```

For using:
1. Initialize config:
```$bash
$ python -m pylistfm --init
```
2. Configure it
3. Create playlist
```$bash
$ python -m pylistfm -a "Artist"
``` 

For testing type:

```$bash
$ python -m unittest discover ./test
```