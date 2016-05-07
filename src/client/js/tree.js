var to = false;
$('#FindInput').keyup(function () {
    if(to) { clearTimeout(to); }
    to = setTimeout(function () {
      var v = $('#FindInput').val();
      $('#panel_right').jstree(true).search(v);
    }, 250);
});

tree_view = {
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

                $('#panel_right').jstree({
                    'core' : {
                        'data' : data_treejs,
                        'themes' : {
                            'name' : 'default-dark',
                            'icons' : true
                        }
                    },
                    'plugins' : [ 'types', 'search', "contextmenu" ],
                    'types' : {
                     'dir' : { 'icon' : 'octicon-file-directory' },
                     'file' : { 'icon' : 'octicon-file-code' }
                    }
                });
                $('#panel_right').on("changed.jstree", function (e, data) {
                    console.log(data.selected);
                });
            },
            error: function(result) {
                alert(JSON.stringify(result));
            }
        });
    }
}
