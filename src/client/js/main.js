init();

function save() {
source = myDiagram.model.toJson();

alg = {
    input_spec: ['x'],
    output_spec: ['y'],
    source: source
}

$.jsonRPC.request('algorithm_update', {
        params: ['/user1/Alg', alg],
        id: server.token,

        success: function(result) {
            alert(JSON.stringify(result.result));
        }
});
}

function exec() {
var x = parseFloat(document.getElementById('InputArg').value);

$.jsonRPC.request('algorithm_exec', {
    params: ['/user1/Alg', {x:x}],
    id: server.token,

    success: function(result) {
        alert("Результат: " + JSON.stringify(result.result.y));
    }
});
}

function toggle_menu() {
  var item = document.getElementById("panel_menu");

  if(item.classList.contains('hide_menu')) {
    item.classList.remove('hide_menu');
    item.classList.add('show_menu');
  }
  else {
    item.classList.remove('show_menu');
    item.classList.add('hide_menu');
  }
}