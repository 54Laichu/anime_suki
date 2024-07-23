document.addEventListener("DOMContentLoaded", () => {
  document.querySelector('#uploadButton').addEventListener('click', async function(event) {
    event.preventDefault();

    const textInput = document.querySelector('#text').value;
    const fileInput = document.querySelector('#img').files[0];

    if (!textInput || !fileInput) {
      alert("請輸入文字並選擇圖片");
      return;
    }

    const formData = new FormData();
    formData.append('note', textInput);
    formData.append('img', fileInput);

    try {
      const response = await fetch('/api/v1/image', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        const resultDiv = document.querySelector('#result');

        const img = document.createElement('img');
        img.src = result.url;
        img.alt = 'Uploaded Image';

        const text = document.createElement('p');
        text.textContent = result.note;

        resultDiv.innerHTML = '';
        resultDiv.appendChild(img);
        resultDiv.appendChild(text);
      } else {
        console.error('Upload failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  const imgContainer = document.querySelector('#img-container');

  fetch('/api/v1/images')
    .then(response => {
      if (!response.ok) {
        throw new Error('SQL 連線問題');
      }
      return response.json();
    })
    .then(images => {
      let uploadedImages = images["message"];
      if (uploadedImages.length != 0) {
        uploadedImages.forEach(img => {
          let cardImg = document.createElement('div');
          cardImg.className = "card-img";
          let imgElement = document.createElement('img');
          imgElement.src = img.url;
          imgElement.alt = 'Uploaded Image';
          cardImg.appendChild(imgElement);

          let cardText = document.createElement('p');
          cardText.className = "card-txt";
          cardText.textContent = img.note;

          let card = document.createElement('div');
          card.className = "card";
          card.appendChild(cardImg);
          card.appendChild(cardText);

          imgContainer.appendChild(card);
        });
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
