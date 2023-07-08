const URL = "http://127.0.0.1:8000/api/status";

async function GetTransactions(URL) {
    let TransactionsList = await fetch(URL);
    return TransactionsList.json();
}

Items = [];

GetTransactions(URL).then(data => Items = data);

while(1) console.log(Items);