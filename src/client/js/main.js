init();

function load(src) {
    myDiagram.model = go.Model.fromJson(src);
    myDiagram.model.linkFromPortIdProperty = "fromPort";
    myDiagram.model.linkToPortIdProperty = "toPort";
    myPalette.layoutDiagram(true);

    $('#panel_message').css("display", "none");
    $('#panel_flowchart').css("display", "block");
}

function create() {
    var template = '    { "class": "go.GraphLinksModel",       ' +
    '      "linkFromPortIdProperty": "fromPort",' +
    '      "linkToPortIdProperty": "toPort",    ' +
    '      "nodeDataArray": [                   ' +
    ' {"category":"Start", "text":"Начало", "key":-1, "loc":"-27.76666259765625 -339"}, ' +
    ' {"category":"End", "text":"Конец", "key":-4, "loc":"-0.76666259765625 97"} ' +
    '     ],                                    ' +
    '      "linkDataArray": [                   ' +
    '    ]}                                     ';

    load(template);
}

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
    /*
    $.magnificPopup.open({
        items: {
            type: 'inline',
            src: "#popup-start"
        }
    });
    $(document).on('click', '.popup-modal-cancel', function (e) {
        e.preventDefault();
        $.magnificPopup.close();
    });
    */

   show_msg_ok({
    title: "Press ok",
    text: "<b>Please</b> press ok!",
    onOk: function() {
        console.log("fine!");
    }
   });

    /*
    var x = parseFloat(document.getElementById('InputArg').value);

    $.jsonRPC.request('algorithm_exec', {
        params: ['/user1/Alg', {x:x}],
        id: server.token,

        success: function(result) {
            alert("Результат: " + JSON.stringify(result.result.y));
        }
    });
    */
}

function show_msg_ok(params) {
    $.magnificPopup.open({
        items: {
            type: 'inline',
            src: "#popup-msg-ok"
        }
    });

    $("#popup-msg-ok-title").html(params.title);
    $("#popup-msg-ok-text").html(params.text);

    $(document).off('click', '.popup-modal-ok');
    $(document).on('click', '.popup-modal-ok', function (e) {
        e.preventDefault();
        $.magnificPopup.close();

        params.onOk();
    });
}