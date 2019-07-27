(function() {
    fetch("http://lvh.me:1337/api/all_transactions")
        .then(function(response) {
            return response.json();
        })
        .then(function(responseJson) {
            let myJsonArray = responseJson["data"];
            console.log(responseJson);
            let contentTable = document.getElementById("contentTable");
            let indexArray = ["index", "source", "provider", "destination", "payload"];
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