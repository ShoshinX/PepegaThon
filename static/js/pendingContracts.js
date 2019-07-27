(function() {
    fetch("http://lvh.me:1337/api/all_contracts")
        .then(function(response) {
            return response.json();
        })
        .then(function(jsonObject) {
            console.log(jsonObject);
            let myJsonArray = JSON.parse(jsonObject).data;
            console.log(myJsonArray);
            let contentTable = document.getElementById("contentTable");
            let indexArray = ["index", "source", "payload", "amount"];
            for (let i = 0; i < myJsonArray.length; i++) {
                let newRow = document.createElement("tr");
                let json = {};
                for (let j = 0; j < indexArray.length + 1; j++) {
                    let newElement = document.createElement("td");
                    if (j === indexArray.length) {
                        let newButton = document.createElement("button");
                        newButton.id = "button-" + i;
                        newButton.style.backgroundColor = "red";
                        newButton.addEventListener("click", () => {
                            console.log("works");
                            fetch("http://localhost:1337/api/verify_contract", {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(json)
                            }).then(
                                (response) => { if (response.ok === true) document.getElementById("button-" + i).style.backgroundColor = "green"; }
                            );
                        });
                        newButton.innerText = "verify";
                        newElement.appendChild(newButton);
                    } else {
                        newElement.innerText = myJsonArray[i][indexArray[j]];
                        if (j === 0) {
                            json["ContractID"] = myJsonArray[i]["index"];
                        } else if (j == 1) {
                            json["User"] = myJsonArray[i]["source"];
                        } else if (j == 2) {
                            json["Data"] = myJsonArray[i]["payload"];
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
    console.log("Am i called?");
    document.getElementsByClassName("stylebutton").style.backgroundColor = "green";
}