document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('webcam');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing webcam:', error);
        });
});