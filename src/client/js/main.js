
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

  $.jsonRPC.setup({
  endPoint: '/api'
  });

  server= {}
  function save() {
    document.getElementById("mySavedModel").value = myDiagram.model.toJson();
    myDiagram.isModified = false;
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
  }

