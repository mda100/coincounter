# coincounter


## Start Containers
docker-compose up --build

## Services
- Client: http://localhost:3000 
- Rest API: http://localhost:8000
- Polling Service: synchronize database based on cron job
- Worker Service: address transactions added to database asynchronously 
- Database: http://localhost:5432
- Redis: http://localhost:6379


## Rest Endpoints
- `GET /api/addresses/` - List all addresses
- `POST /api/addresses/` - Create new address
    {address: str}
- `DELETE /api/addresses/{address}/` - Delete address
- `GET /api/addresses/{address}/transactions/` - Get address transactions

## TODO and Limitations
- paginate addresses query
- queue 500 errors from external api to retry
- improve logging and error handling
- calculate a time added for transactions and sort by latest
- determine buy or sell for transaction
- transaction query is currently limited to 50 due to rate limiting and memory limits, can fetch total with batch requests
- final balance of address may be out of sync with transactions as transactions are added asynchronously
- keep track of last block height to update only recent transactions
- keep track of last time transactions were added to database for an address and show on frontend
- could add users, then cache user data
- improve UI
- add loading on frontend as external api adds latency
- manage secrets (currently randomly generated for local deployments)
- adding addresses waits for external api - doesn't add in frontend until resolved
