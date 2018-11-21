# Search the Web

A quick project to fetch and parse xml, json and csv files.


### Installing

This project contains a dockerfile, which will build all that is needed to run.

Assuming you have docker installed and are in the source directory,
everything will be setup using pyenv and pipenv.

Here we build and tag the image so that its nicely named.
The build will also take care of setting up django and a small sqlite migration.
```
docker build . -t code_test:latest
```

All that is left is to run the image and to specify a directory that you would
like the output to be written to on your host system.

Here the host folder (~/tmp) is mapped with the docker containers /tmp folder to
produce ~/tmp/all_products.csv
```
docker run -v ~/tmp:/tmp -t code_test:latest
```


## Author

* **Derrick Heiberg**
