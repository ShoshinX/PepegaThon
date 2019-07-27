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
                for (let j = 0; j < indexArray.length; j++) {
                    let newElement = document.createElement("td");
                    newElement.innerText = myJsonArray[i][indexArray[j]];
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