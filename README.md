Must change .env values for port strategy
container name and pairlist 
All configured by default just change the value

NOTE: for updating config.json better always use config-private.json file

clone the repo

```bash
git clone https://github.com/minulislam/freqtrade-strategies.git 


```bash

cp user_data/config.json.example user_data/config.json
cp user_data/config-private.json.example user_data/config-private.json
cp docker-compose.yml.example docker-compose.yml
cp .env.example .env

docker-compose run --rm freqtrade create-userdir --userdir user_data

```

config-private.json format
```json
{
    "bot_name": "Freqtrade - TradingBot",
    "fiat_display_currency": "USD",
    "exchange": {
        "name": "binance",
        "key": "",
        "secret": ""
    },
    "telegram": {
        "enabled": false,
        "token": "",
        "chat_id": ""
    },
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8070,
        "verbosity": "info",
        "jwt_secret_key": "",
        "CORS_origins": [],
        "username": "freqtrader",
        "password": "freqtrader"
    }
}

'''
