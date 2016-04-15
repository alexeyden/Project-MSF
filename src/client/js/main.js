
  $(function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
    $( "#find" ).autocomplete({
      source: availableTags
    });
  });

  init();

  server= {}

  $.jsonRPC.setup({
    endPoint: '/api'
  });

  $.jsonRPC.request('user_authorize', {
    params: ['user1', '123'],
      id: 'none',

    success: function(result) {
        server.token = result.result;

         $.jsonRPC.request('algorithm_fetch', {
            params: ['/user1/Alg'],
            id: server.token,

            success: function(result) {
                src = result.result.source;
                myDiagram.model = go.Model.fromJson(src);
            },
            error: function(result) {
                alert(JSON.stringify(result));
            }
        });
    },
    error: function(result) {
        alert(JSON.stringify(result));
    }
  });

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
                alert(JSON.stringify(result));
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

