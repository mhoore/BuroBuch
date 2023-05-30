$(document).ready(function(){
    add_events();
    room = document.getElementById('id_room').value;
    if (room != "---") {
        reload_objects(room, document.getElementById('id_desk'));
    }
})

function add_events() {
    $("#id_building").change(function () {
        element = document.getElementById('id_department');
        reload_objects(this.value, element);
        removeOptions('id_room');
        removeOptions('id_desk');
    });

    $("#id_department").change(function () {
        element = document.getElementById('id_room');
        reload_objects(this.value, element);
        removeOptions('id_desk');
    });

    $("#id_room").change(function () {
        element = document.getElementById('id_desk');
        reload_objects(this.value, element);
    });
}

function reload_objects(parent_id, element) {
    removeOptions(element.id);
    removeMap();
    $.ajax({
        type: "POST",
        url: '/booking/get_choices/',
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'parent_id': parent_id,
            'element_id': element.id
        },
        success: function (data) {
            console.log(data);
            data_json = JSON.parse(data);
            choices = data_json['choices']
            for (let key in choices) {
                var opt = document.createElement('option');
                opt.value = key;
                opt.innerHTML = choices[key]['name'];
                element.appendChild(opt);
            }
            load_map(element.id, data_json['image_url'], choices);
        }
    });
}

function removeOptions(id) {
    element = document.getElementById(id);
    element.selectedIndex = 0;
    var i, L = element.options.length - 1;
    for(i = L; i > 0; i--) {
        element.remove(i);
    }
}

function removeMap() {
    element = document.getElementById('id_map_div');
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function load_map(choice_element_id, image_url, choices) {
    var img = document.createElement('img');
    img.id = "id_img";
    img.src = image_url;
    img.alt = 'Plan';
    img.useMap = "#plan";
    img.className = 'image_map';
    document.getElementById('id_map_div').appendChild(img);

    var map = document.createElement('map');
    map.name = "plan";

    var mapster_areas = [];
    for (let key in choices) {
        var area = document.createElement('area');
        area.shape = 'poly';
        coords = choices[key]['coords'];
        area.coords = scale_coords(coords, img.width / 100);
        area.href = '#';
        area.id = choices[key]['name'];

        area.onclick = function(e){
            e.preventDefault();
            choice_element = document.getElementById(choice_element_id);
            choice_element.value = key;
            const evt = new Event("change");
            choice_element.dispatchEvent(evt);
        };

        var mapster_area_dict = {}
        mapster_area_dict['key'] = choices[key]['name'];
        mapster_area_dict['fillcolor'] = "000000";
        mapster_areas.push(mapster_area_dict);

        map.appendChild(area);
    }

    document.getElementById('id_map_div').appendChild(map);
    
    $('#id_img').mapster({
        fillOpacity: 0.3,
        fillColor: "45af5f",
        stroke: true,
        strokeColor: "000000",
        strokeOpacity: 0.8,
        strokeWidth: 1,
        singleSelect: true,
        staticState: true,
        mapKey: 'id',
        listKey: 'id',
        showToolTip: true,
        toolTipClose: ["tooltip-click", "area-click"],
        areas: mapster_areas
    });
}

function scale_coords(coords_str, factor) {
    var coords_arr = coords_str.split(',');
    for(i=0; i < coords_arr.length; i++) {
        coords_arr[i] *= factor;
    }
    return coords_arr.toString();
}