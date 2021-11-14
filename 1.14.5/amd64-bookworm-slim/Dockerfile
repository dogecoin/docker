FROM debian:bookworm-slim AS verify

WORKDIR /verify

# Release specification
ARG RLS_VERSION=1.14.5
ARG RLS_ARCH=x86_64
ARG RLS_OS=linux
ARG RLS_LIB=gnu

ENV RLS_FILE_NAME=dogecoin-${RLS_VERSION}-${RLS_ARCH}-${RLS_OS}-${RLS_LIB}.tar.gz

ENV SIG_PATH=${RLS_VERSION}-${RLS_OS}
ENV DESCRIPTOR_PATH=contrib/gitian-descriptors/gitian-${RLS_OS}.yml
ENV PUBKEY_PATH=contrib/gitian-keys

ENV REPO_GITIAN_BUILDER=https://github.com/devrandom/gitian-builder.git
ENV REPO_GITIAN_SIGS=https://github.com/dogecoin/gitian.sigs.git
ENV REPO_DOGECOIN_CORE=https://github.com/dogecoin/dogecoin.git


# install system requirements
RUN apt update && apt install -y \
    wget \
    git \
    ruby \
    gpg \
    && rm -rf /var/lib/apt/lists/*

# fetch tools and setup signers
RUN git clone ${REPO_GITIAN_BUILDER} gitian && \
    git clone ${REPO_GITIAN_SIGS} sigs && \
    git clone -b v${RLS_VERSION} ${REPO_DOGECOIN_CORE} dogecoin && \
    find dogecoin/${PUBKEY_PATH} -name "*.pgp" |xargs -n 1 gpg --import

# download release binary and verify against random signer
RUN wget https://github.com/dogecoin/dogecoin/releases/download/v${RLS_VERSION}/${RLS_FILE_NAME} && \
    gitian/bin/gverify --no-markup -d sigs -r ${SIG_PATH} \
      dogecoin/${DESCRIPTOR_PATH} | grep OK | \
      shuf -n 1 | sed s/:.*// > random_signer.txt && \
    grep ${RLS_FILE_NAME} sigs/${SIG_PATH}/$(cat random_signer.txt)/*assert | shasum -c && \
    mv ${RLS_FILE_NAME} dogecoin.tar.gz

FROM debian:bookworm-slim AS final

ENV USER=dogecoin
ENV DATADIR=/${USER}/.dogecoin

# Root configuration to mimic user
ENV HOME=/${USER}

RUN useradd ${USER} --home-dir ${HOME}

# Dependencies install
RUN apt update && apt install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Copy the downloaded binary from the verify stage
COPY --from=verify /verify/dogecoin.tar.gz ./

# Move downloaded binaries and man pages in the container system.
# Setuid on binaries with $USER rights, to limit root usage.
RUN tar -xvf dogecoin.tar.gz --strip-components=1 && \
    cp share/man/man1/*.1 /usr/share/man/man1 && \
    cp bin/dogecoin* /usr/local/bin && \
    chown ${USER}:${USER} /usr/local/bin/dogecoin* && \
    chmod 4555 /usr/local/bin/dogecoin* && \
    rm -rf *

COPY docker-entrypoint.py /usr/local/bin/docker-entrypoint

WORKDIR ${HOME}

# P2P network (mainnet, testnet & regnet respectively)
EXPOSE 22556 44556 18444

# RPC interface (mainnet, testnet & regnet respectively)
EXPOSE 22555 44555 18332

VOLUME ["/dogecoin/.dogecoin"]

ENTRYPOINT ["docker-entrypoint"]
