(function() {
    document.getElementById("button").addEventListener("click", (event) => {
        let provider = document.getElementById("provider").value;
        let source = document.getElementById("source").value;
        let destination = document.getElementById("destination").value;
        let payload = document.getElementById("payload").value;
        let amount = document.getElementById("amount").value;
        let data = {
            Provider: provider,
            Source: source,
            Destination: destination,
            Payload: payload,
            Amount: amount
        };
        console.log(data);
        fetch('http://localhost:1337/api/make_contract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain',
                },
                body: JSON.stringify(data)
            })
            .then((response) => alert("DEEZNUTS"));

    });
})();