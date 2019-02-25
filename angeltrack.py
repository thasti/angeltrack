#!/usr/bin/python
import requests
import json
import argparse

api_url_rx = "http://127.0.0.1:8091/sdrangel/deviceset/0/channel/0/settings"
api_url_tx = "http://127.0.0.1:8091/sdrangel/deviceset/1/channel/0/settings"

parser = argparse.ArgumentParser(description="RX/TX control for sdrangel")
arg_group = parser.add_mutually_exclusive_group(required=True)
arg_group.add_argument('--rx', action='store_true')
arg_group.add_argument('--tx', action='store_true')
parser.add_argument('--txoffs', type=float, default=0, help='Specify offset added to RX frequency. TX = RX + TXOFFS')
args = parser.parse_args()

# query demodulator properties
rx_config_req = requests.get(api_url_rx)
rx_config = rx_config_req.json()

# query modulator properties
tx_config_req = requests.get(api_url_tx)
tx_config = tx_config_req.json()

if args.tx:
    tx_config['SSBModSettings']['inputFrequencyOffset'] = rx_config['SSBDemodSettings']['inputFrequencyOffset'] + args.txoffs
    rx_config['SSBDemodSettings']['audioMute'] = 1
    tx_config['SSBModSettings']['audioMute'] = 0

if args.rx:
    rx_config['SSBDemodSettings']['audioMute'] = 0
    tx_config['SSBModSettings']['audioMute'] = 1

requests.patch(api_url_rx, data=json.dumps(rx_config))
requests.patch(api_url_tx, data=json.dumps(tx_config))
