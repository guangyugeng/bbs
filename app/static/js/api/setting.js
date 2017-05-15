api.uploadAvatar = function(data, callback){
    var url = '/api/user/upload/avatar'
    api.post(url, data, callback)
}