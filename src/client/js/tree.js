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
                },
                "multiple" : false,
                "check_callback" : function(op, node, parent, pos, more) {
                    if(op == 'move_node') {
                        if(parent.id == '#')
                            return false;

                        if(!parent.data.is_directory)
                            return false;

                        var parts_node = node.data.path.split('/');
                        var parts_parent = parent.data.path.split('/');

                        if(parts_node.length < 2 || parts_parent.length < 2 || parts_node[1] != parts_parent[1])
                            return false;

                        return true;
                    }
                    else return true;
                }
            },
            'plugins' : [ 'types', 'search', 'dnd' ],
            'types' : {
             'dir' : { 'icon' : 'octicon-file-directory' },
             'file' : { 'icon' : 'octicon-file-code' }
            },
            "dnd": {
                "copy" : false,
                "is_draggable": function(nodes, ev) {
                    for(var i = 0; i < nodes.length; i++) {
                        if(nodes[i].data.path.split('/').length < 3)
                            return false;
                    }
                    return true;
                }
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

        $("#panel_right").on("move_node.jstree", function(e, data) {
            console.log(e, data)
            $.jsonRPC.request('path_move', {
                        params: [
                            data.new_instance.get_node(data.node).data.path,
                            data.new_instance.get_node(data.parent).data.path + '/' +
                                data.new_instance.get_node(data.node).data.name
                        ],
                        id: server.token,

                        success: function(result) {
                            tree_view.update()
                        },
                        error: function(result) {
                            if(result.error.code == 2) {
                                show_msg_ok_id({
                                    title : "Ошибка",
                                    text : "Невозможно переместить в эту папку!",
                                    onOk : function() {}
                                });
                                tree_view.update();
                            } else {
                                alert(JSON.stringify(result.error))
                            }
                        }
                });
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
