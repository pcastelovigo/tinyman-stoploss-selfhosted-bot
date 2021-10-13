#################################################################################
# TINYMAN SELF-HOSTED STOPLOSS BOT by Pablo Castelo                             #
#################################################################################
# BE CAREFUL: THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND   #
# THE AUTHOR IS NOT RESPONSIBLE FOR ANY CLAIM, LOSS OR INCONVENIENCE CAUSED     #
# DON'T USE THIS SOFTWARE IF YOU DON'T FULLY UNDERSTAND HOW IT WORKS            #
# READ CAREFULLY THE INSTRUCTIONS AND TRY TESTNET FIRST BEFORE USING            #
#################################################################################
# HOW-TO INSTALL AND RUN                                                        #
# 1. USING PYTHON3 AND PIP3 PACKAGE MANAGER:                                    #
# 2. pip3 install git+https://github.com/tinymanorg/tinyman-py-sdk.git          #
# 3. pip3 install py-algorand-sdk                                               #
# 4. RUN THIS PROGRAM INDEFINITELY: python3 tinyman-selfhosted-stoploss-bot.py  #
#################################################################################
# CONFIGURATION                                                                 #
# AMOUNT OF ASA TO SELL INCLUDING DECIMALS                                      #
# EXAMPLE: SELLING 1.000010 ASA = 1000010                                       #
AMOUNT_OF_ASA_TO_SELL_WITH_DECIMALS=100  #BE CAREFUL DECIMALS MATCHING YOUR ASA #
# THRESHOLD PRICE TO SELL THE AMOUNT SPECIFIED ABOVE                            #
# EXAMPLE: IF THE 100 UNITS OF ASA ARE PAID AT 0.005 ALGO EACH IT WILL BE SOLD  #
THRESHOLD_PRICE_TO_SELL_ASA=0.0004                                              #
# YOUR ASA ID                                                                   #
ASSET_ID_TO_STOP_LOSS=26340954  #BE CAREFUL, ASA CHANGES FROM TEST TO MAIN      #
# ALGO ID. CHANGE IT TO CHANGE TO AN ASA/ASA POOL. NOT RECOMMENDED              #
ALGO_ID=0  # TRY IN TESTNET BEFORE USING THIS FEATURE                           #
# YOUR ADDRESS, THE ADDRESS USED TO SELL THE ASA IF THRESHOLD PRICE IS REACHED  #
YOUR_ADDRESS="FFFB1S3FG1SWE8YSG1W8Y3SF4GS65Y4S6V4S3DG16SY4EXAMPLEADDRESS"       #
# YOUR MNEMONIC KEYS. BE VERY CAREFUL!! YOU CAN LOSE YOUR ASSETS AND FUNDS!!    #
YOUR_MNEMONIC="false test not real pass just example test passphrase example test your pass here test filter stoploss try testnet before user use at your risk"
# NEVER SHARE THIS FILE ONCE CONFIGURED!! YOUR CAPITAL IS AT RISK!              #
#################################################################################
# CONTRIBUTE:                                                                   #
# IF THIS SOFTWARE IS USEFUL FOR YOU PLEASE CONTRIBUTE:                         #
# DONATING ALGO TO: 7VDZ7YN3F4TRAGAWUPTMCAVD32OSIN2ZI67CKUVKX32JZXDRBRNLC36LFU  #
# OR BUYING TOKEN: 330109984                                                    #
# https://app.tinyman.org/#/swap?asset_in=0&asset_out=330109984                 #
# THANK YOU VERY MUCH                                                           #
#################################################################################
# TODO                                                                          #
# STOPLOSS ON VARIOUS ASSETS AT A TIME                                          #
#################################################################################

import time
from tinyman.v1.client import TinymanTestnetClient
from algosdk import mnemonic
account = {
    'address': YOUR_ADDRESS,
    'private_key': mnemonic.to_private_key(YOUR_MNEMONIC)
}
i=0
while i <= 10:
    client = TinymanTestnetClient(user_address=account['address'])
    ASA = client.fetch_asset(ASSET_ID_TO_STOP_LOSS)
    ALGO = client.fetch_asset(ALGO_ID)
    pool = client.fetch_pool(ASA, ALGO)
    quote = pool.fetch_fixed_input_swap_quote(ASA(AMOUNT_OF_ASA_TO_SELL_WITH_DECIMALS), slippage=1.00)
    if (quote.price/10000) > THRESHOLD_PRICE_TO_SELL_ASA:
        precio = quote.price/10000
        print(f'ASA PRICE: {precio}')
    if (quote.price/10000) < THRESHOLD_PRICE_TO_SELL_ASA:
        print(quote)
        print(f'Swapping {quote.amount_in} to {quote.amount_out_with_slippage}')
        transaction_group = pool.prepare_swap_transactions_from_quote(quote)
        transaction_group.sign_with_private_key(account['address'], account['private_key'])
        result = client.submit(transaction_group, wait=True)
        excess = pool.fetch_excess_amounts()
        if ALGO in excess:
            amount = excess[ALGO]
        transaction_group = pool.prepare_redeem_transactions(amount)
        transaction_group.sign_with_private_key(account['address'], account['private_key'])
        result = client.submit(transaction_group, wait=True)
        print('STOPLOSS SUCCESSFULLY EXECUTED')
        quit()
    print('ASA price OVER stoploss price')
    print('Tinyman will rest 5 minutes...')
    time.sleep(300)


