<p align="center">
  <img src="https://static.tumblr.com/ppdj5y9/Ae9mxmxtp/300coin.png" alt="Dogecoin" width="200"/>
</p>

# Docker images for Dogecoin

## Supported tags and respective `Dockerfile` links

- [`1.14.5`,`latest`](#)

## Quick reference

- **Maintained by the [Dogecoin community](https://github.com/dogecoin/docker/)**
- **Docker Hub images:** https://hub.docker.com/r/dogecoin/dogecoin
- **Dogecoin Core repository:** https://github.com/dogecoin/dogecoin
**Issue tracker:** https://github.com/dogecoin/docker/issues
- **Supported architectures:** `amd64`, `arm32v7`, `arm64v8`, `i386`

## What is this coin with a Doge on it ?

Dogecoin is a community-driven cryptocurrency that was inspired by a Shiba Inu meme. The Dogecoin Core software allows anyone to operate a node in the Dogecoin blockchain networks and uses the Scrypt hashing method for Proof of Work. It is adapted from Bitcoin Core and other cryptocurrencies.

To get more information about Dogecoin Core, visit the [source code repository](https://github.com/dogecoin/dogecoin).

## How to use this image

Start your node in a single command, exposing P2P & RPC ports, mapping the data directory:
```bash
docker run -d --name dogecoin-node \
    -v $(pwd)/datadir:/dogecoin/.dogecoin \
    -p 22555:22555 \
    -p 22556:22556 \
    dogecoin/dogecoin:latest
```
It will launch the synchronization of the blockchain, which take hours. That's it, your node is up !

To verify if the container is running and to get logs:
```bash
docker ps
docker logs dogecoin-node
```

Call the JSON-RPC API using the `dogecoin-cli` present inside the container. The help menu will display all existing commands of the API:
```bash
docker exec dogecoin-node dogecoin-cli help
```

## Syntax & Configuration

```bash
# Syntax
docker run  [docker-options] dogecoin/dogecoin [executable] [executable-options]
```

+ `docker-options` : Set environment variables, ports, volumes and other docker settings.  
+ `executable` : Choose between `dogecoind`, `dogecoin-cli`, `dogecoin-tx` or `dogecoin-qt`. Default to `dogecoind`.  
+ `executable-options` : Pass options directly to the executable.

There are three ways to configure the Dogecoin node:

1. by using environment variables,
2. by passing arguments to the executable,
3. by providing a `dogecoin.conf` in a volume.

**To see all available configurations, see the `-help` menu from each executable:**
```bash
docker run dogecoin/dogecoin -help
```

### Configure with executable arguments

`docker run` arguments are passed directly to the executable.
```bash
docker run dogecoin/dogecoin -paytxfee=0.01 -testnet
```

### Configure with environment variables

All options, for each executable, can be defined with environment variables.

```bash
docker run -e PAYTXFEE=0.01 -e TESTNET=1 dogecoin/dogecoin
```
Environment variables represent executable arguments converted into upper case, without leading hyphen (`-`). 
Any hyphens inside an argument name must be converted to underscores (from `-`, to `_`.) 
Note that boolean arguments require the value `1` assigned to the variable.

For example, the `-help-debug` argument becomes `HELP_DEBUG=1` as environment variable.

### Configure with a configuration file

`dogecoin.conf` file can be used to configure your node. This file need to be located in the `datadir` of the node.

Create `dogecoin.conf` with the following content:
```
testnet=1
paytxfee=0.01
```

Put this file in the directory mounted to `/dogecoin/.dogecoin`, in `datadir` for this example :
```bash
docker run -v $(pwd)/datadir:/dogecoin/.dogecoin dogecoin/dogecoin
```

### Docker Compose

Example for `docker-compose.yml` :
```
version: '3.1'

services:
  dogecoin:
    image: dogecoin/dogecoin
    restart: always
    environment:
      PAYTXFEE: 0.01
      MAXCONNECTIONS: 150
    ports:
      - 22555:22555
      - 22556:22556
    volumes:
      - ./datadir:/dogecoin/.dogecoin
```
Then, run `docker compose up`.

## License

Docker repository for Dogecoin Core is released under [MIT license](https://github.com/dogecoin/docker/blob/main/LICENSE).
Feel free to use, modify & distribute for commercial and non-commercial purpose.

Please share your improvements & fixes to improve the tool for everyone :)
