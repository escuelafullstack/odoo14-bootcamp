console.log("Cargando offline.js")


var db = openDatabase('offline_odoo', '1.0', 'My Offline Database', 10 * 1024 * 1024);


db.transaction(function(tx) {
    tx.executeSql('CREATE TABLE IF NOT EXISTS res_partner(id, name, vat, create_date, write_date)', [], getPartners);
});


function getPartners(){
    console.log('getPartners....')
    $.ajax({
        url: "/getPartners",
        type: 'get',
        dataType: 'json',
        success: function(response) {
            db.transaction(function(tx) {
                tx.executeSql('DELETE FROM res_partner ', []);
            });
            jQuery.each(response, function(i, item) {
                $("#table-body").append(
                 '<tr>' +
                 '<td><input type="text" id="id_'+item.id+'" value="' + item.id +'" readonly=""/></td>' +
                 '<td><input type="text" id="name_'+item.id+'" value="' + item.name +'"/></td>' +
                 '<td><input type="text" id="vat_'+item.id+'" value="' + item.vat +'"/></td>' +
                 ' <td>' + item.create_date +'</td>' +
                 ' <td>' + item.write_date +'</td>' +
                 ' <td><button class="btn btn-primary" type="button" onclick="guardarPartner('+item.id+')"><i class="fa fa-save"/> Guardar</button></td>' +
                 ' <td></td>' +
                '</tr>'
                )
                db.transaction(function(tx) {
                    tx.executeSql('INSERT INTO res_partner (id, name, vat, create_date, write_date) VALUES (?, ?, ?, ?, ?)',
                        [item.id, item.name, item.vat, item.create_date, item.write_date]);
                });
            })
        }
    });
}


function guardarPartner(id){
    console.log('Guardando id. ' + id)
    let name = $("#name_" + id).val()
    let vat = $("#vat_" + id).val()
    db.transaction(function(tx) {
        tx.executeSql('UPDATE res_partner set name=?, vat=? where id=?',
            [name, vat, id]);
    });

}


function subirData(){
    db.transaction(function (tx) {
        tx.executeSql('SELECT id, name, vat FROM res_partner', [],
          function callback(tx, results) {
            //console.log(results.rows)
              var len = results.rows.length, i;
              let lista = []
              for (i = 0; i < len; i++) {
                lista.push(results.rows.item(i))
              }
              let data = {
                'csrf_token': $("#csrf_token").val(),
                'data': JSON.stringify(lista)
              }
              console.log(data)
            $.ajax({
              url: '/updatePartners',
              type: 'post',
              dataType: 'json',
              timeout: 10000,
              data: data,
              success: function(data) {
                console.log(data)
                if (data.status){
                    alert('Información actualizada')
                }
              },
              error: function(data) {
                alert("Ocurrió un error")
              }
            });

            },
          function errorCallback(tx, error) {
            alert('Error de conexión: ' + error.message);
          }
          );
    });
}
/*

WebSQL
https://www.arkaitzgarro.com/html5/capitulo-8.html

https://couchdb.apache.org/


*/