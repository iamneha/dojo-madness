##  Dojo-Madness
The website can be accessble by the url http://localhost:8080

### Build:
- Requirements:
	-	`docker`,  `docker-compose`
bash
$ docker-compose build


- **Local** Build Requirements (optional)
	- `python3`, `pip`, `sqlite3`
	- **Local build && run**
		bash
		$ make install && python3 server.py
		

### Run:
bash
$ docker-compose up -d


### Testing:
bash
$ make test
