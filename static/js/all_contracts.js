(function() {
    fetch("http://lvh.me:1337/api/all_contracts/")
        .then(function(response) {
            return response.json();
        })
        .then(function(myJsonArray) {
            let contentTable = document.getElementById("contentTable");
            let indexArray = ["Contract ID", "Source", "Provider", "Destination", "Payload"];
            for (let i = 0; i < myJsonArray.length; i++) {
                let newRow = document.createElement("tr");
                for (let j = 0; j < indexArray.length + 1; j++) {
                    let newElement = document.createElement("td");
                    if (j === indexArray.length) {
                        let newButton = document.createElement("button");
                        newButton.innerText = "verify";
                        newElement.appendChild(newButton);
                    } else {
                        newElement.innerText = myJsonArray[i][indexArray[j]];
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