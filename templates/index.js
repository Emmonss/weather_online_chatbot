function send(){
    // 先获取文本域内的代码值
    var sourcecode = $("#sourcecode").val();
    // var sourcecode = document.getElementById("sourcecode").value;
    // 借助ajax实现功能获取
    var xhr = XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState==4) {
            console.log(xhr.responseText)
        }
    }
    xhr.open(post, '/api/user')
    xhr.send({'code': sourcecode})
}