
$(document).ready(function(){
  $("#show_razmer").click(function(){
    $("#razmer").fadeIn("slow");
  });
});

$(document).ready(function(){
  $("#show_struj").click(function(){
    $("#strujkolom").fadeIn("slow");
  });
});

$(document).ready(function(){
  $("#show_splav").click(function(){
    $("#splav").fadeIn("slow");
  });
});

$(document).ready(function(){
    $("button").click(function(){
        var f_g = $('#form1').find('[id=f_g]').val()
        var f_b = $('#form1').find('[id=f_b]').val()
        var f_t = $('#form1').find('[id=f_t]').val()
        var f_h = $('#form1').find('[id=f_h]').val()
        var d_l = $('#form1').find('[id=d_l]').val()
        var d_r = $('#form1').find('[id=d_r]').val()
        var d_t = $('#form1').find('[id=d_t]').val()
        var c_m = $('#form1').find('[id=c_m]').val()
        var c_s = $('#form1').find('[id=c_s]').val()
        var g_m = $('#form1').find('[id=g_m]').val()
        var g_s = $('#form1').find('[id=g_s]').val()
        $.ajax({

            type: 'POST',
            contentType: 'application/json',
            url: '/get_carbide_plate',
            data: JSON.stringify({
                'parametrs': {
                    'f_g': f_g,
                    'f_b': f_b,
                    'f_t': f_t,
                    'f_h': f_h,
                    'd_l': d_l,
                    'd_r': d_r,
                    'd_t': d_t,
                    'c_m': c_m,
                    'c_s': c_s,
                    'g_m': g_m,
                    'g_s': g_s
                    }
                }),
            success: function(data) {
            console.log(data);

            $('.result').html(data.results.join('</br>'));

            }
        });
   });
});
