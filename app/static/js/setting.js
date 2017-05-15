var inputChange = function(e){
    var input = e.target
    var td = input.closest('td')
    var p_message = $(td).find('.message').first()
    console.log(p_message)
    p_message.remove()
}

var fileChange = function(e){
    var input = e.target
    $('#selected-img').cropper('replace', URL.createObjectURL(input.files[0]))
}


var bindEvents = function(){
    $('input').on('input', inputChange)
    $('.file-input').on('change', fileChange)
}

var initCrop = function(){
    log("setting")
    img_x = $('#data-img-x')
    img_y = $('#data-img-y')
    img_nw = $('#data-img-nw')
    img_nh = $('#data-img-nh')
    $('#selected-img').cropper({
        dragMode: 'move',
        aspectRatio: 1/1,
        viewMode: 1,
        preview: '.img-preview',
        minContainerWidth: 200,
        minContainerHeight: 200,
        cropBoxMovable: false,
        cropBoxResizable: false,
        toggleDragModeOnDblclick: false,
        crop: function(e) {
        // Output the result data for cropping image.
        img_x.val(Math.round(e.x))
        img_y.val(Math.round(e.y))
        img_nw.val(Math.round(e.width))
        img_nh.val(Math.round(e.height))
      }
    });
}

var __main = function(){
    bindEvents()
    initCrop()
}

$(document).ready(__main)
