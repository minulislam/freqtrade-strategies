```yml

---
version: '3'
services:
  freqtrade1:
    image: minulislam/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    build:
      context: .
      dockerfile: "./docker/Dockerfile.stable"
    restart: unless-stopped
    container_name: BinClucMadSMAv1
    volumes:
      - "./user_data:/freqtrade/user_data"
    ports:
      - "0.0.0.0:${PORT:-8080}:${PORT:-8080}"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade1.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade1.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config-private.json
      --config /freqtrade/user_data/config-telegram.json
      --config /freqtrade/user_data/pairlist/${PAIRLIST:-binance-usdt-static}.json
      --config /freqtrade/user_data/pairlist/blacklist-binance.json
      --strategy BinClucMadSMAv1
    env_file:
      - freqtrade1.env




  freqtrade3:
    image: minulislam/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    build:
      context: .
      dockerfile: "./docker/Dockerfile.stable"
    restart: unless-stopped
    container_name: Obelisk_Ichimoku_Slow_v1_3
    volumes:
      - "./user_data:/freqtrade/user_data"
    ports:
      - "0.0.0.0:${PORT3:-8080}:${PORT:-8080}"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade3.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade3.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config-private.json
      --config /freqtrade/user_data/pairlist/${PAIRLIST3:-binance-usdt-static}.json
      --config /freqtrade/user_data/pairlist/blacklist-binance.json
      --strategy Obelisk_Ichimoku_Slow_v1_3
    # environment:
    #   - FREQTRADE__MAX_OPEN_TRADES=5
    #   - FREQTRADE__AVAILABLE_CAPTITAL=1000
    env_file:
      - freqtrade3.env


  freqtrade4:
    image: minulislam/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    build:
      context: .
      dockerfile: "./docker/Dockerfile.stable"
    restart: unless-stopped
    container_name: Combined_NFIv7_SMA
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/latest/rest-api/ documentation
    # before enabling this.
    ports:
      - "0.0.0.0:${PORT4:-8080}:${PORT:-8080}"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade4.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade4.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config-private.json
      --config /freqtrade/user_data/pairlist/${PAIRLIST4:-binance-usdt-static}.json
      --config /freqtrade/user_data/pairlist/blacklist-binance.json
      --strategy Combined_NFIv7_SMA
    env_file:
      - freqtrade4.env


```

```env
FREQTRADE__MAX_OPEN_TRADES=10
FREQTRADE__AVAILABLE_CAPTITAL=1000



```
