(function() {
    let contentTable = document.getElementById("contentTable");
    let indexArray = ["ContractID", "Source", "Provider", "Destination", "Payload"];
    let array = [{
        ContractID: "pepega",
        Source: "u",
        Destination: "me",
        Payload: "59"
    }]
    for (let i = 0; i < array.length; i++) {
        let newRow = document.createElement("tr");
        for (let j = 0; j < indexArray.length; j++) {
            let newElement = document.createElement("td");
            newElement.innerText = array[i][indexArray[j]];
            newRow.appendChild(newElement);
        }
        for (let j = 0; j < newRow.childElementCount; j++) {
            newRow.children[j].classList.add("body-item");
            newRow.children[j].classList.add("mbr-fonts-style");
            newRow.children[j].classList.add("display-7");

        }
        contentTable.appendChild(newRow);
    }
    fetch("http://localhost:1337/all_contracts")
        .then(function(response) {
            return response.json();
        })
        .then(function(myJsonArray) {
            let contentTable = document.getElementById("contentTable");
            let indexArray = ["Contract ID", "Source", "Provider", "Destination", "Payload"];
            for (let i = 0; i < myJsonArray.size(); i++) {
                let newRow = document.createElement("tr");
                for (let j = 0; j < indexArray.size(); j++) {
                    let newElement = document.createElement("td");
                    newElement.innerText = myJsonArray[indexArray[j]];
                    newRow.appendChild(newElement);
                }
                for (let j = 0; j < newRow.childElementCount; j++) {
                    newRow.children[j].classList.add("body-item");
                    newRow.children[j].classList.add("mbr-fonts-style");
                    newRow.children[j].classList.add("display-7");

                }
                contentTable.appendChild(newRow);
            }
        })
})();