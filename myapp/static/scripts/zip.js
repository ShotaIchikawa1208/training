$(function () {
    console.log('function')
    $('#yubin').change(function () {
        let zip = $(this).val();
        $ajax({
            url: "http://zipcloud.ibsnet.co.jp/api/search",
            type: "GET",
            data: { zipcode: zip },
            datatype: "jsonp"
        })
            .done(function (value) {
                if (value.message == null) {
                    let result = value.results[0]
                    $("ken_code").val(result.prefcode),
                        $("shiku").val(result.address2 + result.address3),
                        $("jyushyo").val(result.address1 + address2 + address3)
                } else {
                    $("yubin").val(value.message);
                    alert('郵便番号が不正です')
                }
            })
            .fail(sunction()[
                alert("郵便番号が不正です")
            ]);
    });
});