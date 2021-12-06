# PolyWall

## What is this?
PolyWall is a plain-text file stored on the Polygon blockchain.
There are 2^256-1 lines on this wall. Each line is 100 characters long.

## Is it free?
Creation of new lines is always free.
Each modification of a line increases the cost for editing by 0.01 MATIC.

You are free to write whatever you like. The Wall will never be moderated. 
We believe that freedom of speech is one of the unalienable right for every man.
Leave a message. It will be stored on-chain. Forever.

Check out the [website](https://polywall.pw) to try it yourself.


## PolyWall CLI
PolyWall CLI is simply a bunch of functions. It's made mainly for file upload.

### Requirements
- python 3.7


### Setup

1. Install brownie``pip install eth-brownie``
2. Add the account you want to use ``brownie accounts new <NAME>``
3. Set an environment variable ``WEB3_INFURA_PROJECT_ID`` with your Infura key


### Usage

You can upload text files to the PolyWall

1. Put your file into ``cli\files``
2. Run
```
brownie run .\cli\functions.py upload_file 0xWALL <ACCOUNT_NAME> <FILE_NAME> <FROM_LINE> --network polygon-main
```

Other functions are well documented in ``.\cli\main.py``
