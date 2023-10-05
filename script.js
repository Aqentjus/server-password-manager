document.addEventListener("DOMContentLoaded", function () {
    const addPasswordForm = document.getElementById("addPasswordForm");
    const getPasswordForm = document.getElementById("getPasswordForm");
    const resultDiv = document.getElementById("result");

    addPasswordForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const service = document.getElementById("service").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        
        const data = {
            "service": service,
            "username": username,
            "password": password
        };

        // Send data to the server
        sendRequest("/add", JSON.stringify(data));
    });

    getPasswordForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const serviceToFind = document.getElementById("serviceToFind").value;
        
        // Send service name to the server
        sendRequest("/get", serviceToFind);
    });

    function sendRequest(endpoint, requestData) {
        const xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    resultDiv.innerHTML = xhr.responseText;
                } else {
                    resultDiv.innerHTML = "Error: " + xhr.statusText;
                }
            }
        };

        xhr.open("POST", endpoint, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(requestData);
    }
});
