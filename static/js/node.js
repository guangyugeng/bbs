var nodeTemplate = function(n){
    var n = `
    <div class="node-box">
        <div class="node-item" data-id="${n.id}">
            <div class="node-title">
                <h1>${n.name}</h1>
            </div>
            <div class="node-content">
                ${n.description}
            </div>
            <div class="node-action">
                <button class="node-delete" type="button">删除</button>
            </div>
        </div>
    </div>
    `
    return n
}

var btnOnNewNode = function(e){
    var btn = e.target
    var box = $(btn).closest('.node-input-box')
    var topic_id = $(box).find('.select-topic').first().val()
    var name = $(box).find('.input-node-name').first().val()
    var en_name = $(box).find('.input-node-en_name').first().val()
    var description = $(box).find('.input-node-description').first().val()
    var form = {
        'topic_id': parseInt(topic_id),
        'name': name,
        'en_name': en_name,
        'description': description
    }
    log(form.topic_id)
    var response = function(r){
        if (r.success){
            n = r.data
            $('.node-lists').prepend(nodeTemplate(n))
        }
        else{
            alert(r.message)
        }
    }
    api.nodeAdd(form, response)
}

var btnOnDeleteNode = function(e){
    var btn = e.target
    var item = $(btn).closest('.node-item')
    var box = $(item).closest('.node-box')
    var id = $(item).data('id')
    var form = {
        'id': id
    }
    var response = function(r){
        if (r.success){
            box.remove()
            alert('删除成功')
        }
        else{
            alert(r.message)
        }
    }
    api.nodeDelete(form, response)
}

var bindNodeEvents = function(){
    $('.node-new').on('click', btnOnNewNode)
    $('.node-lists').on('click', '.node-delete', btnOnDeleteNode)
}


$(document).ready(function(){
    bindNodeEvents()

})