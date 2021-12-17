"""
    Store outputs of `-help` menus of all Dogecoin Core executable.
    Lists of raw options used to hook `entrypoint.get_help` function.
"""

dogecoin_cli = [
        '  -conf=<file>',
        '  -datadir=<dir>',
        '  -testnet',
        '  -regtest',
        '  -named',
        '  -rpcconnect=<ip>',
        '  -rpcport=<port>',
        '  -rpcwait',
        '  -rpcuser=<user>',
        '  -rpcpassword=<pw>',
        '  -rpcclienttimeout=<n>',
        '  -stdin'
        ]

dogecoin_tx = [
        '  -create',
        '  -json',
        '  -txid',
        '  -testnet',
        '  -regtest'
        ]

dogecoind = [
        '  -version',
        '  -alerts',
        '  -alertnotify=<cmd>',
        '  -blocknotify=<cmd>',
        '  -blocksonly',
        '  -assumevalid=<hex>',
        '  -conf=<file>',
        '  -daemon',
        '  -datadir=<dir>',
        '  -dbcache=<n>',
        '  -feefilter',
        '  -loadblock=<file>',
        '  -maxorphantx=<n>',
        '  -maxmempool=<n>',
        '  -mempoolexpiry=<n>',
        '  -blockreconstructionextratxn=<n>',
        '  -par=<n>',
        '  -pid=<file>',
        '  -prune=<n>',
        '  -reindex-chainstate',
        '  -reindex',
        '  -sysperms',
        '  -txindex',
        '  -addnode=<ip>',
        '  -banscore=<n>',
        '  -bantime=<n>',
        '  -bind=<addr>',
        '  -connect=<ip>',
        '  -discover',
        '  -dns',
        '  -dnsseed',
        '  -externalip=<ip>',
        '  -forcednsseed',
        '  -listen',
        '  -listenonion',
        '  -maxconnections=<n>',
        '  -maxreceivebuffer=<n>',
        '  -maxsendbuffer=<n>',
        '  -maxtimeadjustment',
        '  -onion=<ip:port>',
        '  -onlynet=<net>',
        '  -permitbaremultisig',
        '  -peerbloomfilters',
        '  -port=<port>',
        '  -proxy=<ip:port>',
        '  -proxyrandomize',
        '  -rpcserialversion',
        '  -seednode=<ip>',
        '  -timeout=<n>',
        '  -torcontrol=<ip>:<port>',
        '  -torpassword=<pass>',
        '  -upnp',
        '  -whitebind=<addr>',
        '  -whitelist=<IP address or network>',
        '  -whitelistrelay',
        '  -whitelistforcerelay',
        '  -maxuploadtarget=<n>',
        '  -disablewallet',
        '  -keypool=<n>',
        '  -fallbackfee=<amt>',
        '  -mintxfee=<amt>',
        '  -paytxfee=<amt>',
        '  -rescan',
        '  -salvagewallet',
        '  -sendfreetransactions',
        '  -spendzeroconfchange',
        '  -txconfirmtarget=<n>',
        '  -usehd',
        '  -walletrbf',
        '  -upgradewallet',
        '  -wallet=<file>',
        '  -walletbroadcast',
        '  -walletnotify=<cmd>',
        '  -zapwallettxes=<mode>',
        '  -dblogsize=<n>',
        '  -flushwallet',
        '  -privdb',
        '  -walletrejectlongchains',
        '  -zmqpubhashblock=<address>',
        '  -zmqpubhashtx=<address>',
        '  -zmqpubrawblock=<address>',
        '  -zmqpubrawtx=<address>',
        '  -uacomment=<cmt>',
        '  -checkblocks=<n>',
        '  -checklevel=<n>',
        '  -checkblockindex',
        '  -checkmempool=<n>',
        '  -checkpoints',
        '  -disablesafemode',
        '  -testsafemode',
        '  -dropmessagestest=<n>',
        '  -fuzzmessagestest=<n>',
        '  -stopafterblockimport',
        '  -limitancestorcount=<n>',
        '  -limitancestorsize=<n>',
        '  -limitdescendantcount=<n>',
        '  -limitdescendantsize=<n>',
        '  -bip9params=deployment:start:end',
        '  -debug=<category>',
        '  -nodebug',
        '  -help-debug',
        '  -logips',
        '  -logtimestamps',
        '  -logtimemicros',
        '  -mocktime=<n>',
        '  -limitfreerelay=<n>',
        '  -relaypriority',
        '  -maxsigcachesize=<n>',
        '  -maxtipage=<n>',
        '  -minrelaytxfee=<amt>',
        '  -maxtxfee=<amt>',
        '  -printtoconsole',
        '  -printpriority',
        '  -shrinkdebugfile',
        '  -testnet',
        '  -regtest',
        '  -acceptnonstdtxn',
        '  -incrementalrelayfee=<amt>',
        '  -dustrelayfee=<amt>',
        '  -dustlimit=<amt>',
        '  -bytespersigop',
        '  -datacarrier',
        '  -datacarriersize',
        '  -mempoolreplacement',
        '  -blockmaxweight=<n>',
        '  -blockmaxsize=<n>',
        '  -blockprioritysize=<n>',
        '  -blockmintxfee=<amt>',
        '  -blockversion=<n>',
        '  -server',
        '  -rest',
        '  -rpcbind=<addr>',
        '  -rpccookiefile=<loc>',
        '  -rpcuser=<user>',
        '  -rpcpassword=<pw>',
        '  -rpcauth=<userpw>',
        '  -rpcport=<port>',
        '  -rpcallowip=<ip>',
        '  -rpcthreads=<n>',
        '  -rpcworkqueue=<n>',
        '  -rpcservertimeout=<n>'
        ]
