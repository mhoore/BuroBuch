$(document).ready(function(){
    var area_elements = document.getElementById("id_map").children;
    var areas = [];
    for (let i=0; i < area_elements.length; i++) {
        var e = area_elements[i];
        areas.push({"key": e.dataset.hkey, 'fillColor': e.dataset.color, 'toolTip': e.dataset.hkey});
    }

    $(document).ready(function(){
        $('#id_img').mapster({
            stroke: true,
            strokeColor: "000000",
            fillOpacity: 0.3,
            strokeOpacity: 0.8,
            strokeWidth: 1,
            singleSelect: true,
            staticState: true,
            mapKey: 'data-hkey',
            showToolTip: true,
            toolTipClose: ["tooltip-click", "area-click"],
            areas: areas
        });
    })
})