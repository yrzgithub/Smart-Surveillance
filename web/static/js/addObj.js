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

    console.log("clicked..");

    var name = document.getElementById("name");
    var color = document.getElementById("color");
    var type = document.getElementById("type");
    var power = document.getElementById("power");
    var accuracy = document.getElementById("accuracy");
    var range = document.getElementById("range");
    var portability = document.getElementById("portability");

    var file = document.getElementById("file");
    var image = document.getElementById("upload");

    var nameN = name.value;

    if(nameN == "")
    {
        alert("name cannot be empty.");
        return;
    }

    var files = file.files;

    if(files.length==0)
    {
        alert("No file selected.");
        return;
    }

    var spinner = document.getElementById("spinner");
    var button = document.getElementById("button");
    var uploadbtn = document.getElementById("uploadbtn");

    spinner.className = "fa fa-spinner fa-spin spinner";
    button.innerHTML = "Uploading";

    uploadbtn.style.opacity = ".5";
    uploadbtn.disabled = true;

    var form = new FormData();
    form.append("file",files[0]);

    form.append("name",name.value);
    form.append("color",color.value);
    form.append("type",type.value);
    form.append("power",power.value);
    form.append("accuracy",accuracy.value);
    form.append("range",range.value);
    form.append("portability",portability.value);


    fetch("/uploadObj",{"method":"post","body":form})
    .then(response => response.json())
    .then(response => {

        alert("Data Saved");
        
    })
    .finally(()=> {
        spinner.classList.remove("fa");
        spinner.classList.remove("fa-spinner");
        spinner.classList.remove("fa-spin");
        spinner.classList.remove("spinner");

        button.innerHTML = "Upload";

        uploadbtn.style.opacity = "1";
        uploadbtn.disabled = false;
    });
}