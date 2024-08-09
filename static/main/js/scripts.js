function showLoader() {
  document.querySelector('.loading-overlay').style.display = 'flex';
}

function hideLoader() {
  document.querySelector('.loading-overlay').style.display = 'none';
}

function findNearestLocation() {
  showLoader();
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;

      fetch('/api/provide_nearest_location/', {
        method: 'POST',
        headers: {
          'Content-Type': 'appplication/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ latitude: latitude, longitude: longitude})
      })
      .then(response => response.json())
      .then(data => {
        hideLoader();
        if (data.error) {
          console.error(data.error);
          document.querySelector('.result').innerText = data.error;
        } else {
          const resultHTML = `
            <p class="evac_description"><strong>施設名:</strong> ${data.facility_name}</p>
            <p class="evac_description"><strong>住所:</strong> ${data.address}</p>
            <p class="evac_description"><strong>距離:</strong> ${data.distance} km</p>
            <a href=${data.google_maps_url} target="_blank"><button class="google_map_button">グーグルマップを開く</button></a>
          `;
          document.querySelector('.result').innerHTML = resultHTML;
        }
      })
      .catch(error => {
        hideLoader();
        console.error('Error:', error);
        document.getElementById('result').innerText = 'エラーが発生しました。';
      });
    }, error => {
      hideLoader();
      console.error('Geolocation error:', error);
      document.getElementById('result').innerText = '位置情報の取得に失敗しました。';
    });
  } else {
    hideLoader();
    console.error('Geolocation is not supported by this browser.');
    document.getElementById('result').innerText = '位置情報がサポートされていません。';
  }
}

function getCsrfToken() {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name.trim() === 'csrftoken') {
          return value;
      }
  }
  return '';
}

document.addEventListener('DOMContentLoaded', function() {
  const button = document.querySelector('.nearest-button');
  button.addEventListener('click', function() {
    findNearestLocation();
  })
})