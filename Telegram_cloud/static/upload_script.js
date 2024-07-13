// Allows you to manage the page for sending files
document.addEventListener('DOMContentLoaded', function() {
    // Function to send files + convert file to text
    function handleFileSelect(event) {
        const fileList = event.target.files;
        if (fileList.length > 0) {
          const file = fileList[0];
          const reader = new FileReader();
          reader.onload = function(event) {
            const fileContent = event.target.result;
            const fileName = file.name;

              // Call the function that makes a POST request to the site's upload API
            sendFileToFlask(fileName, fileContent);
          };
          reader.readAsText(file);
        }
    }

    // Function to send the file to the Flask server via the API
    function sendFileToFlask(fileName, fileContent) {
        const data = {
            file_name: fileName,
            file_content: fileContent
        };
        // Create and send request 
        fetch('/upload_file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        // Analysis of responses below
        .then(response => {
            if (!response.ok) {
                throw new Error('Une erreur est survenue');
            }
            return response.json();
        })
        .then(data => {
            // Process server response if necessary
            console.log(data.message);
        })
        .catch(error => {
            console.error(error);
        });
    }

    // Listen for the file change 
    document.getElementById('file-input').addEventListener('change', handleFileSelect);
});