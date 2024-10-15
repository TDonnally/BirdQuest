const fileInput = document.getElementById('file-upload');
const fileNameDisplay = document.querySelector('.file-name');
const form = document.querySelector('.upload-image');
const sectionContainer = document.querySelector('.photo-upload');
const searchingText = document.querySelector(".image-placeholder");
const photoGallery = document.querySelector('.photo-gallery');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const currentPath = window.location.pathname;
const pathSegments = currentPath.split('/').filter(segment => segment);



fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        fileNameDisplay.textContent = file.name;
        
        const formData = new FormData();
        formData.append('image', file);
        searchingText.textContent = "Identifying"
        photoGallery.innerHTML = ""

        fetch('/', {  
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  
                'X-CSRFToken': csrftoken      
            },
        })
        .then(response => response.json())  
        .then(data => {
            console.log(data);  
            photoGallery.innerHTML = "";
            sectionContainer.classList.add("active");
            searchingText.textContent = "";
            const sortedData = Object.entries(data).sort(([, a], [, b]) => b - a);

            sortedData.forEach(([bird, confidence]) => {
                const cleanBirdName = bird.replace(/^\d+\./, '').replace(/_/g, ' ');

                const birdDiv = document.createElement('div');
                birdDiv.classList.add('bird-card');

                const birdImage = document.createElement('img');
                const birdImagePath = `/static/images/birds/${bird}/1.jpg`;  
                birdImage.src = birdImagePath;
                birdImage.alt = cleanBirdName;
                birdDiv.appendChild(birdImage);

                const rightSideContainer = document.createElement("div");
                rightSideContainer.classList.add("bird-info");
                const birdTitle = document.createElement('h3');
                birdTitle.textContent = `${cleanBirdName} (${(confidence * 100).toFixed(2)}%)`;
                rightSideContainer.appendChild(birdTitle);
                if (pathSegments.length > 0) {
                    const thatsMyBirdButton = document.createElement('button');
                    thatsMyBirdButton.classList.add("collection-button")
                    thatsMyBirdButton.textContent = "That's My Bird";
                    rightSideContainer.appendChild(thatsMyBirdButton);
                    thatsMyBirdButton.addEventListener('click', function() {
                        const formData = new FormData();
                        formData.append('bird_name', bird);
                        formData.append('image', file); 
                    
                        fetch('/submit_bird', {  
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            searchingText.innerHTML = 
                            `
                            <h2>Bird Added to Collection!</h2>
                            `;
                            sectionContainer.classList.remove("active");
                            photoGallery.innerHTML = '';
                        })
                        .catch(error => console.error('Error:', error));
                    });
                }
                birdDiv.appendChild(rightSideContainer);
                photoGallery.appendChild(birdDiv);
            });
            const noCorrectBirdMessage = document.createElement('h3');
            noCorrectBirdMessage.classList.add("no-bird-message");
            noCorrectBirdMessage.textContent = "Don't see your bird? Try the characteristcs search or enter the species manually."
            photoGallery.append(noCorrectBirdMessage);
        })
        .catch(error => console.error('Error:', error));
    } else {
        fileNameDisplay.textContent = 'No file chosen';
    }
});