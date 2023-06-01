$(document).ready(function(){
    add_events();
    room = document.getElementById('id_room');
    if (room.selectedIndex != 0) {
        reload_objects(room.value, document.getElementById('id_desk'));
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
        date = document.getElementById('id_date').value;
        reload_objects(this.value, element, date);
    });

    $("#id_date").change(function () {
        document.getElementById('id_building').selectedIndex = 0;
        removeOptions('id_department');
        removeOptions('id_room');
        removeOptions('id_desk');
        removeMap();
    });
}

function reload_objects(parent_id, element, date='') {
    removeToolTips();
    removeOptions(element.id);
    removeMap();
    $.ajax({
        type: "POST",
        url: '/booking/get_choices/',
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'parent_id': parent_id,
            'element_id': element.id,
            'date': date,
        },
        success: function (data) {
            data_json = JSON.parse(data);
            choices = data_json['choices']
            for (let key in choices) {
                var opt = document.createElement('option');
                opt.value = key;
                opt.innerHTML = choices[key]['name'];
                element.appendChild(opt);
            }
            load_map(element.id, data_json['image_url'], choices, data_json['booked_choices']);
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

function load_map(choice_element_id, image_url, choices, booked_choices) {
    var img = document.createElement('img');
    img.id = "id_img";
    img.src = image_url;
    img.alt = 'Plan';
    img.useMap = "#plan";
    img.className = 'image_map';
    document.getElementById('id_map_div').appendChild(img);

    var map = document.createElement('map');
    map.name = "plan";
    map.id = "id_map";

    var mapster_areas = [];
    for (let key in choices) {
        var id = choices[key]['name'];
        var area = document.createElement('area');
        area.shape = 'poly';
        area.coords = choices[key]['coords'].toString();
        area.href = '#';
        area.id = id;
        area.dataset.hkey = id;

        area.onclick = function(e){
            e.preventDefault();
            choice_element = document.getElementById(choice_element_id);
            choice_element.value = key;
            const evt = new Event("change");
            choice_element.dispatchEvent(evt);
        };

        var d = {};
        d['key'] = id;
        d['fillColor'] = '45af5f';
        d['toolTip'] = id;
        mapster_areas.push(d);

        map.appendChild(area);
    }

    for (let key in booked_choices) {
        var id = booked_choices[key]['name'];
        var area = document.createElement('area');
        area.shape = 'poly';
        area.coords = booked_choices[key]['coords'].toString();
        area.href = '#';
        area.id = id;
        area.dataset.hkey = id;

        var d = {};
        d['key'] = id;
        d['fillColor'] = 'ff0000';
        d['toolTip'] = id;
        mapster_areas.push(d);

        map.appendChild(area);
    }

    document.getElementById('id_map_div').appendChild(map);
    
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
        areas: mapster_areas
    });
}

function removeToolTips() {
    var elements = document.getElementsByClassName('mapster_tooltip');
    for(let i=0; i < elements.length; i++) {
        elements[i].remove();
    }
}