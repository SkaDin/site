$(document).ready(function() {
    $(".image-thumbnail").click(function() {
        var imageUrl = $(this).attr("src");
        // Открываем модальное окно с увеличенным изображением
        openModal(imageUrl);
    });
});

function openModal(imageUrl) {
    // Создаем модальное окно, которое будет отображать увеличенное изображение
    var modalHtml = '<div id="myModal" class="modal">' +
                    '<span class="close">&times;</span>' +
                    '<img class="modal-content" src="' + imageUrl + '">' +
                    '</div>';

    $("body").append(modalHtml);

    // Закрываем модальное окно при нажатии на крестик или область вокруг изображения
    $(".close, .modal").click(function() {
        closeModal();
    });
}

function closeModal() {
    $("#myModal").remove();
}