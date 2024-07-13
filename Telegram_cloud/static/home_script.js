// Function to retrieve the name of files saved in the json register
function retrieve_files_names() {
    return fetch('static/data/reg.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('Fichier json manquant/ne fonctionnant pas');
        }
        return response.json();
      })
      .then(data => { // data contains json reg formatted for js
        const fileNames = [];
        data.forEach(fileObj => { // loop to browse the data array
          const fileName = Object.keys(fileObj)[0]; // retrieve file name 
          fileNames.push(fileName);
        });
        updateFileTable(fileNames);
      })
      .catch(error => {
        console.error('Erreur: ', error);
        return []; // return an empty list on error
      });
  }


  // Function to start downloading a file
  function downloadFile(fileName) {
    const link = document.createElement('a');
    console.log(link);
    link.href = `/download/${fileName}`; // call flask
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Function for creating the table displayed on the main page
  function updateFileTable(fileNames) {
    const tbody = document.querySelector('#fileTable tbody');
    tbody.innerHTML = ''; // Empty current content

    fileNames.forEach(fileName => { // below the container style 
      const row = document.createElement('tr');
      const cell = document.createElement('td');
      const fileContainer = document.createElement('div'); 
      const fileIcon = document.createElement('img');
      const fileText = document.createElement('span');
      const downloadButton = document.createElement('button');

      // System for displaying an icon according to file type (extension)
      const file_extension = fileName.substr(-4);
      if (file_extension === '.pdf') {
        fileIcon.src = 'https://cdn4.iconfinder.com/data/icons/file-extension-names-vol-8/512/24-256.png'; // icon PDF
      } else if (['.png', '.jpeg', '.gif', '.jpg'].includes(file_extension)) {
        fileIcon.src = 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/image-256.png'; // icon image
      } else if (['docx', '.doc', '.odt', '.txt'].includes(file_extension)) {
        fileIcon.src = 'https://cdn1.iconfinder.com/data/icons/hawcons/32/699342-icon-69-document-text-256.png'; // icon document texte
      } else if (['pptx', '.odp'].includes(file_extension)) {
        fileIcon.src = 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/file-powerpoint-256.png'; // icon PowerPoint ou diaporama
      } else if (file_extension === 'json') {
        fileIcon.src = 'https://cdn3.iconfinder.com/data/icons/type-file-working-office-online-set-the-surname-us/53/json-type-512.png'; // icon JSON
      } else if (file_extension === '.csv') {
        fileIcon.src = 'https://cdn0.iconfinder.com/data/icons/common-file-extensions-audio-documents/24/ext_csv-256.png'; // icon CSV
      } else if (['.zip', '.rar'].includes(file_extension)) {
        fileIcon.src = 'https://cdn1.iconfinder.com/data/icons/hawcons/32/698835-icon-109-document-zip-256.png'; // icon ZIP
      } else if (['.dll', '.exe', '.cmd', '.bat', '.bash'].includes(file_extension)) {
        fileIcon.src = 'https://cdn1.iconfinder.com/data/icons/flat-business-icons/128/gear-256.png'; // icon exe
      } else {
        fileIcon.src = 'https://img.icons8.com/material-outlined/24/000000/file.png'; // icon for all other files types
      }
      // Use the icon chosen above
      fileIcon.alt = 'file_icon'; 
      fileIcon.className = 'file-icon';

      // Display file name in table line
      fileText.textContent = fileName;
      fileText.className = 'file-name';

      // Download button
      downloadButton.textContent = 'Download';
      downloadButton.className = 'download-button';
      downloadButton.onclick = () => {
        downloadFile(fileName);
      };

      // Container style (css)
      fileContainer.style.display = 'flex';
      fileContainer.style.alignItems = 'center';
      fileContainer.style.justifyContent = 'space-between';

      const infoContainer = document.createElement('div');
      infoContainer.style.display = 'flex';
      infoContainer.style.alignItems = 'center';

      infoContainer.appendChild(fileIcon);
      infoContainer.appendChild(fileText);

      fileContainer.appendChild(infoContainer);
      fileContainer.appendChild(downloadButton);

      // Add container to cell
      cell.appendChild(fileContainer);
      row.appendChild(cell);
      tbody.appendChild(row);
    });
  }

  // to initialize the array with file names
  // by calling the retrive_files_names() function
  // knowing that it calls all the others afterwards
  retrieve_files_names();


