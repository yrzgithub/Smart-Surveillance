function put(event)
{
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onload = (e) => {
        var uploadElement = document.getElementById("upload");
        uploadElement.src = e.target.result;
    }
}

function upload(element)
{
    var name = document.getElementById("name");
    var number = document.getElementById("number");
    var residence = document.getElementById("residence");
    var group = document.getElementById("group");
    var relegion = document.getElementById("relegion");
    var position = document.getElementById("position");
    var illness = document.getElementById("illness");
    var upload = document.getElementById("file");

    var nameN = name.value;

    console.log(nameN);

    if(nameN == "")
    {
        alert("name cannot be empty.");
        return;
    }

    var files = upload.files;

    if(files.length==0)
    {
        alert("No file selected.");
        return;
    }

    console.log(file);

    var form = new FormData();
    form.append("file",files);
    form.append("var",2);

    var http = new XMLHttpRequest();
    http.open("POST","/uploadFace");
    http.setRequestHeader("Content-Type","application/json");
    http.send(form);
}