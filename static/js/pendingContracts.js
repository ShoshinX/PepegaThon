(function() {
    fetch("http://lvh.me:1337/api/all_contracts")
        .then(function(response) {
            return response.json();
        })
        .then(function(jsonObject) {
            console.log(jsonObject);
            let x = JSON.parse(jsonObject);
            let myJsonArray = x.data;
            console.log(myJsonArray);
            let contentTable = document.getElementById("contentTable");
            let indexArray = ["ContractID", "Source", "Payload", "Amount"];
            for (let i = 0; i < myJsonArray.length; i++) {
                let newRow = document.createElement("tr");
                let json;
                for (let j = 0; j < indexArray.length + 1; j++) {
                    let newElement = document.createElement("td");
                    if (j === indexArray.length) {
                        let newButton = document.createElement("button");
                        newButton.addEventListener("onclick", () => {
                            fetch("http://localhost:1337/verify_contract", {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(json)
                            })
                        });
                        newButton.innerText = "verify";
                        newElement.appendChild(newButton);
                    } else {
                        newElement.innerText = myJsonArray[i][indexArray[j]];
                        if (j === 0) {
                            json["ContractID"] = myJsonArray[i]["ContractID"];
                        } else if (j == 1) {
                            json["User"] = myJsonArray[i]["Source"];
                        } else if (j == 2) {
                            json["Data"] = myJsonArray[i]["Payload"];
                        } else if (j == 3) {
                            json["VerificationBoolean"] = 1;
                        }
                    }
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

function submitButtonStyle() {
    document.getElementsByClassName("stylebutton").style.backgroundColor = "green";
}