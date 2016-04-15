
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

  server= {}

  $.jsonRPC.setup({
    endPoint: '/api'
  });

  $.jsonRPC.request('user_authorize', {
    params: ['user1', '123'],
      id: 'none',

    success: function(result) {
        server.token = result.result;
    },
    error: function(result) {
        alert(JSON.stringify(result));
    }
  });

  function save() {
    source = myDiagram.model.toJson();

    alg = {
        input_spec: ['x'],
        output_spec: ['y']
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

  }

