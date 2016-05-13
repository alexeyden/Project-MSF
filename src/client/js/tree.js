var to = false;
$('#FindInput').keyup(function () {
    if(to) { clearTimeout(to); }
    to = setTimeout(function () {
      var v = $('#FindInput').val();
      $('#panel_right').jstree(true).search(v);
    }, 250);
});

tree_view = {
    init : function() {
        if($('#panel_right').jstree(true))
            return;

        $('#panel_right').jstree({
            'core' : {
                'themes' : {
                    'name' : 'default-dark',
                    'icons' : true
                }
            },
            'plugins' : [ 'types', 'search' ],
            'types' : {
             'dir' : { 'icon' : 'octicon-file-directory' },
             'file' : { 'icon' : 'octicon-file-code' }
            }
        });

        $('#panel_right').on("changed.jstree", function (e, data) {
            if(data.selected.length > 0) {
                var info = data.instance.get_node(data.selected[0]);
                if(!info.data.is_directory) {
                    $('#edit-dir a').addClass('disabled');
                    $("#run-but a").removeClass("disabled");
                    jQuery("#del-but a").removeClass("disabled");
                    jQuery("#add-but a").addClass("disabled");
                    jQuery("#add-dir-but a").addClass("disabled");

                    tree_view.load(info.data.path);
                }
                else {
                    $('#edit-dir a').removeClass("disabled");
                    jQuery("#add-but a").removeClass("disabled");
                    jQuery("#add-dir-but a").removeClass("disabled");
                    jQuery("#del-but a").removeClass("disabled");
                    jQuery("#run-but a").addClass("disabled");
                }
            }
        });
    },

    selected : function() {
        return $('#panel_right').jstree('get_node', $('#panel_right').jstree('get_selected')[0]).data;
    },

    load : function(path) {
         $.jsonRPC.request('algorithm_fetch', {
            params: [ path ],
            id: server.token,

            success: function(result) {
                src = result.result.source;

                algorithm = result.result;
                algorithm.path = path;
                algorithm.is_new = false;

                $('#algorithm_info').val(algorithm.name)

                load(src);
            },
            error: function(result) {
                alert(JSON.stringify(result));
            }
        });
    },

    update : function() {
       $.jsonRPC.request('path_list', {
            params: ['/', true],
            id: server.token,

            success: function(result) {
                var data = result.result;
                var data_treejs = [];

                var process = function(node) {
                    var result = {
                        id : node.path,
                        text : node.name,
                        type : node.is_directory ? "dir" : "file",
                        data : node,
                        children : []
                    };

                    if(node.children != null) {
                        node.children.forEach(function(item, i, arr) {
                            result.children.push(process(item));
                        });
                    }

                    return result;
                };

                data.forEach(function(item, i, arr) {
                    data_treejs.push(process(item));
                });

                $('#panel_right').jstree(true).settings.core.data = data_treejs;
                $('#panel_right').jstree(true).refresh();
            },
            error: function(result) {
                alert(JSON.stringify(result));
            }
        });
    }
}
