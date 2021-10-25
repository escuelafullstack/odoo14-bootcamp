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
                 ' <th scope="row">' + item.id + '</th>' +
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