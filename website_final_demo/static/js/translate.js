function translateText() {
  let text = document.getElementById("text");

  var formData = new FormData();
  var input = document.getElementById("inputtext").value;
  formData.append("input", input);

  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("outputtext").innerHTML = request.responseText;
    }
  };

  var clickedName = document.getElementById("name").innerHTML;

  if (clickedName == "trump") {
    link = "http://34.82.174.216:5000/obama";
  } else if (clickedName == "obama") {
    link = "http://104.196.253.238:5000/trump";
  } else if (clickedName == "musk") {
    link = "http://34.83.30.177:5000/elon";
  }

  request.open("POST", link)
  //request.open("POST", "http://localhost:5001/");
  request.send(formData);
  return false;
}
