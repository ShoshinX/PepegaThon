import json

def generate_data(contracts, transactions, ledger, active_contracts):
	gen_data = {
	    "contracts": None,
	   	"transactions": None,
	    "ledger": None,
	    "active_contracts": None
	}

	gen_data['contracts'] = contracts
	gen_data['transactions'] = transactions
	gen_data['ledger'] = json.dumps(ledger)
	gen_data['active_contracts'] = json.dumps(active_contracts)

	return json.dumps(gen_data)