odoo.define('ge10_team03.mileage', ['web.ajax'], function(require){
    "use strict";
    var ajax= require('web.ajax');
    $(document).ready(function () {
        var container= document.getElementById("mileage");
        if(container) {
            container.innerHTML= "";
            ajax.jsonRpc('/get_mileage', 'call', {}).then(function(data){
                container.innerHTML= "";
                container.innerHTML+= "<b><center>Our bikes have travelled " + data + ' miles worldwide!</center></b>';
            });
        }
    });
});
