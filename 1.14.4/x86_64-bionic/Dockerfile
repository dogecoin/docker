FROM ubuntu:bionic

# To improve : static hash make dynamic build of versions impossible.
ARG VERSION=1.14.4

ENV USER=dogecoin
ENV DATADIR=/${USER}/.dogecoin

# Root configuration to mimic user
ENV HOME=/${USER}

RUN useradd ${USER} --home-dir ${HOME}

# Dependencies install
RUN apt update && apt install -y \
    man \
    python3 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download Dogecoin Core from github releases for cross-architecture
WORKDIR /tmp

RUN set -ex && ARCHITECTURE=$(dpkg --print-architecture) && \
    if [ "${ARCHITECTURE}" = "amd64" ]; then ARCHITECTURE=x86_64-linux-gnu; fi \
    && if [ "${ARCHITECTURE}" = "arm64" ]; then ARCHITECTURE=aarch64-linux-gnu; fi \
    && if [ "${ARCHITECTURE}" = "armhf" ]; then ARCHITECTURE=arm-linux-gnueabihf; fi \
    && if [ "${ARCHITECTURE}" = "i386" ]; then ARCHITECTURE=i686-pc-linux-gnu; fi \
    && wget https://github.com/dogecoin/dogecoin/releases/download/v${VERSION}/dogecoin-${VERSION}-${ARCHITECTURE}.tar.gz

# Move downloaded binaries and man pages in the container system.
# Setuid on binaries with $USER rights, to prevent
# root right with `docker exec`.
RUN tar -xvf dogecoin-${VERSION}-*.tar.gz --strip-components=1 && \
    cp share/man/man1/*.1 /usr/share/man/man1 && \
    cp bin/dogecoin* /usr/local/bin && \
    chown ${USER}:${USER} /usr/local/bin/dogecoin* && \
    chmod 4555 /usr/local/bin/dogecoin* && \
    rm -rf /tmp/*

COPY docker-entrypoint.py /usr/local/bin/docker-entrypoint
RUN chmod 500 /usr/local/bin/docker-entrypoint

WORKDIR ${HOME}

# P2P network (mainnet, testnet & regnet respectively)
EXPOSE 22556 44556 18444

# RPC interface (mainnet, testnet & regnet respectively)
EXPOSE 22555 44555 18332

VOLUME ["/dogecoin/.dogecoin"]

ENTRYPOINT ["docker-entrypoint"]
