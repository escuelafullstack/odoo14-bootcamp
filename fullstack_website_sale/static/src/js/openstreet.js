console.log("Cargando JS...")

let peru = [-10.0, -75.0]
let colombia = [4.13, -73.085]
let ecuador = [-1.362, -78.677]

var map = L.map('map', { center: peru, zoom: 5 });
var osm = new L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

var options = {
    collapsed: false,
    expand: "touch",
    query: "Buscar direccion",
    defaultMarkGeocode: false
};

var theMarker = {};

L.Control.geocoder(options).on('markgeocode', function(e) {
        var bbox = e.geocode.bbox;
        var poly = L.polygon([
            bbox.getSouthEast(),
            bbox.getNorthEast(),
            bbox.getNorthWest(),
            bbox.getSouthWest()
        ]).addTo(map);
        map.fitBounds(poly.getBounds());
    })
    .addTo(map);

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        console.log("Geolocation is not supported by this browser.")
        // x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    setPosition(position.coords.latitude, position.coords.longitude)
}

function setPosition(latitude, longitude){

    $("#partner_latitude").val(latitude);
    $("#partner_longitude").val(longitude);

    if (theMarker != undefined) {
        map.removeLayer(theMarker);
    };
    theMarker = L.marker([latitude, longitude]).addTo(map);
    theMarker.bindPopup("<b>Mi ubicación</b><br/>Latitud: " + latitude + "<br/>Longitud: " + longitude).openPopup();
    map.setView([latitude, longitude], 17);
}

$(document).ready(function() {

    map.on('click', function(e) {
        $("#partner_latitude").val(e.latlng.lat)
        $("#partner_longitude").val(e.latlng.lng)
        setPosition(e.latlng.lat, e.latlng.lng)
    });
    let latitude = $("#partner_latitude").val()
    let longitude = $("#partner_longitude").val()

    if (latitude && longitude){
        setPosition(latitude, longitude)
    }
})
console.log("Cargado JS.")
