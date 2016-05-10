var cookies = {};

document.cookie.split('; ').forEach(function(item, i, a) {
    var parts = item.split('=');
    cookies[parts[0]] = parts[1];
});

server = {};

$.jsonRPC.setup({
    endPoint: '/api'
});

$('#user_exit').click(logout);

if('user' in cookies && 'token' in cookies &&
    cookies.user != '' && cookies.token != '')
{
    document.getElementById("main_panel").style.display = "block";
    document.getElementById("auth_panel").style.display = "none";

    server.user = cookies.user;
    server.token = cookies.token;

    $(function() {
        tree_view.init();
        tree_view.update();
        $("#user").html(server.user);
    });
}

$("#auth_button").click(function() {
    $("#auth_button").prop('disabled', true);
    $("#auth_error").css('visibility', 'hidden');

    var login = $('#auth_login').val();
    var password = $('#auth_password').val();

    $.jsonRPC.request('user_authorize', {
        params: [login, password],
        id: 'none',

        success: function(result) {
            server.user = login;
            server.token = result.result;

            document.getElementById("main_panel").style.display = "block";
            document.getElementById("auth_panel").style.display = "none";

            tree_view.init();
            tree_view.update();

            $("#auth_button").prop('disabled', false);

            document.cookie = "user=" + server.user;
            document.cookie = "token=" + server.token;

            $("#user").html(server.user);
        },
        error: function(result) {
            if(result.error.code == 1) {
                $('#auth_error').css("visibility",'visible');
            }
            else {
                alert(JSON.stringify(result));
            }

            $("#auth_button").prop('disabled', false);
        }
    });
});

function logout() {
    server.user = '';
    server.token = '';
    document.cookie = "user=";
    document.cookie = "token=";

    document.getElementById("main_panel").style.display = "none";
    document.getElementById("auth_panel").style.display = "flex";
    $('#auth_password').val("");
}