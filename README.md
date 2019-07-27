# PepegaThon
- Project ARAB - Aid Resouce Allocation Blockchain

# Goals
1) Public Ledger detailing all aid allocation from source to end user
2) Online Webapp viewer which can search through the entire blockchain
3) Private and Public key wallet
4) Tokens
5) Smart Contracts

# Random Notes
Organisation (aid provider) -> Contract (Source, Destination, Payload, Amount, Provider)

If Contract not fulfilled -> Both Source and Destination lose integrity tokens

Contract Fulfilled -> Transaction Made

- Make Contract (Source, Destination, Payload, Amount, Provider)
- Verify Contract (ContractID, ContractID+ValidationBoolean signed with key)
- Get Pending Contracts
- Get All Transactions 


Each Block 10 Transactions or Contracts