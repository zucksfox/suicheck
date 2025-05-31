
# Wallet checker balance




## Cara Install

Buka terminal kamu + Download dulu

```bash
  git clone https://github.com/zucksfox/suicheck.git
```
Buka Folder kamu
```
cd suicheck
```
Masukan address sui kamu di ```wallet.txt```
contoh :
```
0x1xxxxxxxxxxx
0x2xxxxxxxxxxx
0x3xxxxxxxxxxx
```
Run
```
python suicheck.py 
```

## GET API
daftar + create app dulu di https://dashboard.blockvision.org/ lalu copy

contoh API
```
https://sui-testnet.blockvision.org/v1/xxxxxxxxxxxxxxxx
```
Masukan API di code ```suicheck.py```

```
RPC_URL = "TOKEN SUI MU"
```
