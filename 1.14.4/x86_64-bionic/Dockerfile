FROM ubuntu:bionic AS verify

WORKDIR /verify

# Specify release variables
ARG RLS_VERSION=1.14.4
ARG RLS_OS=linux
ARG RLS_LIB=gnu
ARG RLS_ARCH=

# Automatically detect architecture
RUN set -ex && ARCHITECTURE=$(dpkg --print-architecture) \
    && if [ "${ARCHITECTURE}" = "amd64" ]; then RLS_ARCH=x86_64 ; fi \
    && if [ "${ARCHITECTURE}" = "arm64" ]; then RLS_ARCH=aarch64; fi \
    && if [ "${ARCHITECTURE}" = "armhf" ]; then RLS_ARCH=arm && RLS_LIB=gnueabihf; fi \
    && if [ "${ARCHITECTURE}" = "i386" ]; then RLS_ARCH=i686-pc; fi \
    && if [ "${RLS_ARCH}" = "" ]; then echo "Could not determine architecture" >&2; exit 1; fi \
    && RLS_FILE_NAME=dogecoin-${RLS_VERSION}-${RLS_ARCH}-${RLS_OS}-${RLS_LIB}.tar.gz \
    && echo -n ${RLS_FILE_NAME} > .filename

ARG SIG_PATH=${RLS_VERSION}-${RLS_OS}
ARG DESCRIPTOR_PATH=dogecoin/contrib/gitian-descriptors/gitian-${RLS_OS}.yml

ARG RLS_LOCATION=https://github.com/dogecoin/dogecoin/releases/download/v${RLS_VERSION}
ARG REPO_GITIAN_BUILDER=https://github.com/devrandom/gitian-builder.git
ARG REPO_GITIAN_SIGS=https://github.com/dogecoin/gitian.sigs.git
ARG REPO_DOGECOIN_CORE=https://github.com/dogecoin/dogecoin.git

# Pinned known sha256sums
RUN    echo 72ee42424835cdfb4111b284c98f78919b7a9ede6f8d509b2abe31f7b3eb1f09 dogecoin-1.14.4-aarch64-linux-gnu.tar.gz > SHASUMS \
    && echo d023b7a6dfc5d92b1635f0fa03e14c9fc787a3eae94fba0cc3aca53b62a8e9ac dogecoin-1.14.4-arm-linux-gnueabihf.tar.gz >> SHASUMS \
    && echo 6e93f5edccf528b44112f2088be3ac8f4f44151a757754da09c8c53cdd725815 dogecoin-1.14.4-i686-pc-linux-gnu.tar.gz >> SHASUMS \
    && echo 6266235abe4bcbd41ea57bdf42f11ef89aa69f0386e8c8846d5228af69e7fa13 dogecoin-1.14.4-x86_64-linux-gnu.tar.gz >> SHASUMS

# install system requirements
RUN apt update && apt install -y \
    wget \
    git \
    ruby \
    gpg \
    && rm -rf /var/lib/apt/lists/*

# fetch tools and setup signers
RUN git clone --depth 1 ${REPO_GITIAN_BUILDER} gitian \
    && git clone --depth 1 ${REPO_GITIAN_SIGS} sigs \
    && git clone --depth 1 -b v${RLS_VERSION} ${REPO_DOGECOIN_CORE} dogecoin \
    && find dogecoin/contrib/gitian-keys -name "*.pgp" |xargs -n 1 gpg --import

# download release binary and verify against random OK signer and pinned shasums
RUN RLS_FILE_NAME=$(cat .filename) \
    && wget ${RLS_LOCATION}/${RLS_FILE_NAME} \
    && gitian/bin/gverify --no-markup -d sigs -r ${SIG_PATH} ${DESCRIPTOR_PATH} \
       | grep OK | shuf -n 1 | sed s/:.*// > random_signer.txt \
    && grep ${RLS_FILE_NAME} sigs/${SIG_PATH}/$(cat random_signer.txt)/*assert | sha256sum -c \
    && grep ${RLS_FILE_NAME} SHASUMS | sha256sum -c \
    && mv ${RLS_FILE_NAME} dogecoin.tar.gz

FROM ubuntu:bionic AS final

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
RUN tar -xvf dogecoin.tar.gz --strip-components=1 \
    && cp share/man/man1/*.1 /usr/share/man/man1 \
    && cp bin/dogecoin* /usr/local/bin \
    && chown ${USER}:${USER} /usr/local/bin/dogecoin* \
    && chmod 4555 /usr/local/bin/dogecoin* \
    && rm -rf *

COPY docker-entrypoint.py /usr/local/bin/docker-entrypoint
RUN chmod 500 /usr/local/bin/docker-entrypoint

WORKDIR ${HOME}

# P2P network (mainnet, testnet & regnet respectively)
EXPOSE 22556 44556 18444

# RPC interface (mainnet, testnet & regnet respectively)
EXPOSE 22555 44555 18332

VOLUME ["/dogecoin/.dogecoin"]

ENTRYPOINT ["docker-entrypoint"]
