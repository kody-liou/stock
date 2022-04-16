# Install package:
> pip install -r requirements.txt
> pip freeze > requirements.txt

# Build
> docker-compose build --progress plain

## With no cache
> docker-compose build --no-cache --progress plain

# Execute
> docker-compose up

# Todos
1. Do some technical analysis: MACD, MA, bband, Bollinger Channel
1. Read historical data in cents and perform technical analysis
2. Read instant data followed by technical analysis
3. Place an order automatically