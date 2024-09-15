document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;

    fetch('/api/user/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = data.message;
    });
});

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    fetch('/api/user/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        const messageElement = document.getElementById('message');
        messageElement.innerHTML = ''; // Clear previous messages

        if (data.token) {
            localStorage.setItem('token', data.token);
            
            // Create token display and copy button
            const tokenDisplay = document.createElement('div');
            const tokenText = document.createElement('p');
            tokenText.innerText = `Token: ${data.token.substring(0, 10)}...`; // Show only first 5 characters
            
            const copyButton = document.createElement('button');
            copyButton.innerText = 'Copy Token';
            copyButton.onclick = function() {
                navigator.clipboard.writeText(data.token).then(() => {
                    alert('Token copied to clipboard');
                });
            };

            tokenDisplay.appendChild(tokenText);
            tokenDisplay.appendChild(copyButton);
            messageElement.appendChild(tokenDisplay);

            document.getElementById('upload').style.display = 'block';
        } else {
            messageElement.innerText = data.message;
        }
    });
});

document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const file = document.getElementById('fileInput').files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/user/upload_screenshot', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = data.message;
    });
});
