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

function upload(event)
{
    event.preventDefault();

    var name = document.getElementById("name");
    var number = document.getElementById("number");
    var residence = document.getElementById("residence");
    var group = document.getElementById("group");
    var relegion = document.getElementById("relegion");
    var position = document.getElementById("position");
    var illness = document.getElementById("illness");
    var upload = document.getElementById("file");

    var nameN = name.value;

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

    console.log(files);

    var form = new FormData();
    form.append("file",files[0]);
    
    form.append("name",name.value);
    form.append("number",number.value);
    form.append("residence",residence.value);
    form.append("group",group.value);
    form.append("religion",relegion.value);
    form.append("religion",relegion.value);
    form.append("illness",illness.value);


    fetch("/uploadFace",{"method":"post","body":form})
    .then(
        (resolve) => {
            alert("File uploaded successfully.");
        },

        (reject) => {
            alert("Something went wrong.");
        }
    );
}