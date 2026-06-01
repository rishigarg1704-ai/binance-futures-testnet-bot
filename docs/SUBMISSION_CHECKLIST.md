# Submission Checklist

## Functional
- [ ] MARKET order works on Binance Futures Testnet
- [ ] LIMIT order works on Binance Futures Testnet
- [ ] BUY and SELL both supported
- [ ] CLI usage is clear and discoverable (`--help`)
- [ ] request and response details are printed

## Quality
- [ ] code split into CLI layer and API/client layer
- [ ] input validation runs before API call
- [ ] exception handling for input/API/network failures exists
- [ ] logs include requests, responses, errors
- [ ] logs redact secrets

## Security
- [ ] API credentials loaded from environment
- [ ] `.env` excluded from git
- [ ] no keys/tokens committed

## Evidence
- [ ] log file contains one successful MARKET order
- [ ] log file contains one successful LIMIT order
- [ ] README includes exact commands used

## Reviewer Experience
- [ ] project runs from a clean machine using README steps
- [ ] `requirements.txt` is complete and minimal
- [ ] assumptions and limitations are documented

## Final Gate
- [ ] repo is clean and readable
- [ ] no dead code, placeholder TODO spam, or broken imports
- [ ] output and logs are deterministic enough to review quickly
