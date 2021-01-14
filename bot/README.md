# labelling-bot

## Setup

```sh
# Install dependencies
yarn install or npm install

# Run the bot
yarn start or npm start
```

## Docker

```sh
# 1. Build container
docker build -t labelling-bot .

# 2. Start container
docker run -e APP_ID=<app-id> -e PRIVATE_KEY=<pem-value> labelling-bot
```

## Contributing

If you have suggestions for how `labelling-bot` could be improved, or want to report a bug, open an issue!
We'd love all and any contributions.
