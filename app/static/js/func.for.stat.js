function openModal(photoUrl) {
  var modal = document.getElementById("modal");
  var enlargedPhoto = document.getElementById("enlarged-photo");

  enlargedPhoto.src = photoUrl;
  modal.style.display = "block";
}

function closeModal() {
  var modal = document.getElementById("modal");
  modal.style.display = "none";
}

window.onclick = function(event) {
  var modal = document.getElementById("modal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
}