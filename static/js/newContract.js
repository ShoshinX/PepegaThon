(function() {
    document.addEventListener("change", (event) => {
        let provider = document.getElementById("provider").nodeValue;
        let source = document.getElementById("source").nodeValue;
        let destination = document.getElementById("destination").nodeValue;
        let payload = document.getElementById("payload").nodeValue;
        let amount = document.getElementById("amount").nodeValue;
        data = {
            Provider: provider,
            Source: source,
            Destination: destination,
            Payload: payload,
            Amount: amount
        };
        fetch("http://localhost:1337/api/make_contract", {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                mode: 'cors', // no-cors, cors, *same-origin
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                headers: {
                    'Content-Type': 'application/json',
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                redirect: 'follow', // manual, *follow, error
                referrer: 'no-referrer', // no-referrer, *client
                body: JSON.stringify(data), // body data type must match "Content-Type" header
            })
            .then(response => alert("contract made"));
    });
})();