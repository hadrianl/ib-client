# ib-client
use vue as fronted and ib_insync as backend to place orders to IB
  
## USAGE
### build from source code
- `git clone https://github.com/hadrianl/ib-client.git`
- `cd ib-client`
- `docker-compose up`
- if build ib-visual-frontend failed, remove '--registry https://registry.npm.taobao.org' from the frontend dockerfile
### pull from docker hub
- copy the `docker-compose.yml` and `ib.env` into `$YourDir`
- set up your own `ib.env`
- `cd $YourDir`
- `docker-compose up`