(function() {
    document.getElementById("form").addEventListener("submit", (event) => {
        event.preventDefault();
        let provider = document.getElementById("provider").value;
        let source = document.getElementById("source").value;
        let destination = document.getElementById("destination").value;
        let payload = document.getElementById("payload").value;
        let amount = document.getElementById("amount").value;
        let data = {
            provider: provider,
            source: source,
            destination: destination,
            payload: payload,
            amount: amount,
            signedContract: "Despacito"
        };
        console.log(data)
        fetch('http://localhost:1337/api/make_contract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then((response) => alert("Contract Made"));
    });
})();
