async function process()
{
    var orderedlist = document.getElementById("ol");
    var faceImg = document.getElementById("detectImg");

    console.log("running...");

    await fetch("getimage")
    .then(response => response.json())
    .then(response => {

        if(response.error != undefined)
        {
            console.log(response.error);
            return;
        }

        orderedlist.innerHTML = "";

        var image = response.img;
        var faces = response.faces;
        var objects = response.objects;

        console.log(faces.length);

        for(let index=0;index<faces.length;++index)
        {
            let face = faces[index];

            var li = document.createElement("li");

            var link = document.createElement("a");
            link.setAttribute("target","blank_");

            link.href = "/face/" + face;
            link.innerHTML = face;

            li.appendChild(link);
            orderedlist.appendChild(li);
        }

        faceImg.src = image;

    });
}