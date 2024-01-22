document.addEventListener('DOMContentLoaded', function () {
    var email = document.getElementById('e-mail');

    email.addEventListener('change', function (event) {

        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/mail_check', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = xhr.responseText;
                if (response == 'OK') {
                    console.log('OK')
                    document.getElementById('result_mail').innerHTML = '登録可能メールアドレス';
                } else {
                    console.log('NO')
                    document.getElementById('result_mail').innerHTML = '登録不可メールアドレス';
                    document.getElementById('e-mail').value = '';
                }


            }
        };

        xhr.send('e-mail=' + email.value)

    })
})



// 郵便番号入力で住所表示
document.addEventListener('DOMContentLoaded', function () {
    var yubin = document.getElementById('yubin')

    yubin.addEventListener('change', function (event) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/search_address', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response['yubin'] == 'None') {
                    alert('入力された郵便番号はありません');
                    document.getElementById('yubin').value = '';
                    document.getElementById('ken_code').value = '';
                    document.getElementById('shiku').value = '';
                    document.getElementById('jyushyo').value = '';
                } else {
                    console.log(response['yubin'])
                    document.getElementById('ken_code').value = response['ken_code']
                    document.getElementById('shiku').value = response['shiku']
                    var jyushyo = response['ken'] + response['shiku'] + response['mati']
                    document.getElementById('jyushyo').value = jyushyo
                }
            }
        }
        xhr.send('yubin=' + yubin.value)
    })
})