/* Global Variables */
var layers,
    featureOverlay,
    wmsLayer,
    wms_url,
    map,
    info,
    displayFeatureInfo,
    view,
    current_layer,
    res_name,
    coordinate,
    map_events;





/*this function creates the base map on the home page*/
function init_map(){


    /*basemap for the map*/
    var base_layer = new ol.layer.Tile({
        source: new ol.source.BingMaps({
            key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
            imagerySet: 'AerialWithLabels'
        })
    });

    /*initial view for the map. You can change the view by changing the lat,long or zoom */
    var view = new ol.View({
        center: ol.proj.transform([-71.4, 18.8], 'EPSG:4326', 'EPSG:3857'),
        minZoom: 2,
        maxZoom: 18,
        zoom:8.3
    });


    /*getting the specific parts that will be used by the popup*/
    var container = document.getElementById('popup');
    var content = document.getElementById('popup-content');
    var closer = document.getElementById('popup-closer');

    /*information for popup*/
    var overlay = new ol.Overlay({
        element: container,
        autoPan: true,
        autoPanAnimation: {
          duration: 250
        }
    });

    /*closes popup on click*/
    closer.onclick = function() {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
    };

    /*identifies which layers will show in the map*/
    layers = [base_layer];

    /*creates the map with the specified views, layers, and popups from above*/
    map = new ol.Map({
        target: 'map',
        view: view,
        layers:layers,
        overlays: [overlay],
    });

    /*searched for the reservoir layer on the geoserver and grabs it. This will need to be changed when installed on a different computer*/
    var wmsLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://tethys-staging.byu.edu:8181/geoserver/wms',
            params: {'LAYERS': 'dominican_republic-national-drainage_line'},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'
        })
    });
    map.addLayer(wmsLayer);


    /*these events occur when the mouse moves*/
    map.on('pointermove', function(evt) {

        var pixel = map.getEventPixel(evt.originalEvent);
        var hit = map.forEachLayerAtPixel(pixel, function(layer) {
            if (layer != layers[0] && layer != layers[1] && layer != layers[2] && layer != layers[3]){
                current_layer = layer;
                return true;}
        });

        /*when the cursor hits a shapefile, it turns into a pointer hand*/
        map.getTargetElement().style.cursor = hit ? 'pointer' : '';

        /*when the cursor is a pointer, the following code if ran*/
        if (map.getTargetElement().style.cursor == "pointer") {
            /*getting the necessary information to pull information from the point in the shapefile*/

        }

    });


    /*when the element is clocked, the "goToUrl" function is used, see first function*/
    map.on("singleclick",function(evt) {

            var view = map.getView();
            var viewProjection = view.getProjection();
            var viewResolution = view.getResolution();
            var wms_url = wmsLayer.getSource().getGetFeatureInfoUrl(evt.coordinate, viewResolution, viewProjection, {'INFO_FORMAT': 'text/javascript', }); //Get the wms url for the clicked point
            /*if the point really is the shapfile then the code will get the information and pull out the NAME*/
            if (wms_url) {
                var parser = new ol.format.GeoJSON();
                $.ajax({
                  url: wms_url,
                  dataType: 'jsonp',
                  jsonpCallback: 'parseResponse'
                }).then(function(response) {
                   comid = response['features'][0]['properties']['COMID'];
                   $.ajax({
                        url: '/apps/uswins/forecastpercent/',
                        type: 'GET',
                        data: {'comid' : comid},
                        contentType: 'application/json',
                        error: function (status) {

                        }, success: function (response) {
                                console.log(response['dates'][0])
                                console.log(response['two'])
                                console.log(response['ten'])
                                console.log(response['twenty'])

                                var tabl = document.getElementById("table");
                                tabl.innerHTML= response['dates']
                                var rows = response;

                                for (i = 0; i < rows.length; i++) {
                                  columns = rows[i];
                                  console.log(i)
//                                  tabl.append(
//                                    '<tr>' +
//                                        <td>' + columns[0] + '</td>' +
//                                        '<td>' + columns[1'<td>' + i + '</td>' +
//                                        '] + '</td>' +
//                                        '<td>' + columns[2] + '</td>' +
//                                        '<td>' + columns[3] + '</td>' +
//                                        '<td>' + columns[4] + '</td>' +
//                                        '<td>' + columns[5] + '</td>' +
//                                        '<td>' + columns[6] + '</td>' +
//                                        '<td>' + columns[7] + '</td>' +
//                                        '<td>' + columns[8] + '</td>' +
//                                        '<td>' + columns[9] + '</td>' +
//                                        '<td>' + columns[10] + '</td>' +
//                                        '<td>' + columns[11] + '</td>' +
//                                        '<td>' + columns[12] + '</td>' +
//                                        '<td>' + columns[13] + '</td>' +
//                                        '<td>' + columns[14] + '</td>' +
//                                        '<td>' + columns[15] + '</td>' +
//                                    '</tr>'
//                                  );
                                }

                        }
                   })


                });


            }

    });



}

function append(){
    var dam = $("#dam").val();
    var level = $("#levelinput").val();
    var date = $("#dateinput").val();

    $.ajax({
        url: '/apps/reservoir-management/append-res-info/',
        type: 'GET',
        data: {'dam' : dam, 'level' : level, 'date' : date},
        contentType: 'application/json',
        error: function (status) {

        }, success: function (response) {

        }
    })
}

function test(){
    alert("work")
}

$('#sampleModal').on('show.bs.modal', function () {
    var dam = $("#dam").val();
    var level = $("#levelinput").val();
    var date = $("#dateinput").val();
    levelstr = "Nivel del Embalse = " + level
    datestr = "Dia = " + date;
    document.getElementsByClassName("modal-body")[0].innerHTML = "Embalse = " + dam;
    $( ".modal-body" ).append("<br>");
    $( ".modal-body" ).append("<br>");
    $( ".modal-body" ).append(levelstr);
    $( ".modal-body" ).append("<br>");
    $( ".modal-body" ).append("<br>");
    $( ".modal-body" ).append(datestr);
    warning = '<i class="material-icons" style="font-size:48px;color:red">warning</i>'
    if (level == "") {
        $( ".modal-body" ).append("<br>");
        $( ".modal-body" ).append(warning);
        $( ".modal-body" ).append("<br>");
        $( ".modal-body" ).append('<i style="font-size:25px;color:red">Se necesita un nivel para el embalse</i>')
    }
})

function addvarstomessage(){
    document.getElementsByClassName("modal-body")[0].innerHTML = "Paragraph changed!";
}


/*thse function occur automatically when the page is loaded*/
$(function(){
//    $('#app-content-wrapper').removeClass('show-nav');
//    $('#app-actions').remove();
    $(".toggle-nav").removeClass('toggle-nav');
    init_map();
});


