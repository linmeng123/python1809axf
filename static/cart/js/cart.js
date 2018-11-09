$(function () {
    $('.cart').width(innerWidth)


    total()


    //单个计算
    $('.cart .confirm-wrapper').click(function () {
        var cartid = $(this).attr('cartid')
        var $that = $(this)
        $.get('/changecartstatus/',{'cartid':cartid},function (response) {
             console.log(response)
            if (response.status == 1){
                var isselect = response.isselect
                $that.attr('isselect', isselect)
                $that.children().remove()
                if (isselect){
                    $that.append('<span class="glyphicon glyphicon-ok"></span>')
                } else {
                    $that.append('<span class="no"></span>')
                }

                total()
            }

        })

    })
    $('.cart .all').click(function () {
        var isselect = $(this).attr('isselect')
        isselect = (isselect == 'false')? true : false
        $(this).attr('isselect',isselect)
        if (isselect){
            $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
        }else {
            $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')

        }

        $.get('/changeallselect/',{'isselect':isselect},function (response) {

            if (response.status == 1){
                $('.confirm-wrapper').each(function () {
                    $(this).attr('isselect', isselect)
                    if (isselect){
                        $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                    } else {
                        $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
                    }
                })
                total()
            }
        })

    })

    function total() {
        var sum = 0

        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if ($confirm.find('.glyphicon-ok').length){
                var price = $content.find('.price').attr('price')
                var num = $content.find('.num').attr('number')
                sum +=price*num
            }
        })
        $('.bill .total b').html(parseInt(sum))
    }

     $('.bill-right').click(function () {
         $.get('/generateorder/',function (response) {
             if (response.status ==1){
                 window.open('/orderinfo/'+response.identifier + '/',target='_self')
             }
         })
     })

















})