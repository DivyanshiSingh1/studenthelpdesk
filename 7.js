
 
 function generateResume() { 
  var photo = document.getElementById("photo").innerHTML;
  var name = document.getElementById("name").innerHTML;
  var sign = document.getElementById("sign").innerHTML;
  var roll = document.getElementById("roll").innerHTML;
  var dob = document.getElementById("dob").innerHTML;
  var prog = document.getElementById("prog").innerHTML;
  var branch = document.getElementById("branch").innerHTML;
  var batch = document.getElementById("batch").innerHTML;
  var preaddress = document.getElementById("preaddress").innerHTML;
  var mob = document.getElementById("mob").innerHTML;
  var pmob = document.getElementById("pmob").innerHTML;
  var bg = document.getElementById("bg").innerHTML;
  var allergic = document.getElementById("allergic").innerHTML;
  var cgpa = document.getElementById("cgpa").innerHTML;
  var skills = document.getElementById("skills").innerHTML;
  
  document.querySelector("#exportContent").innerHTML="<img src="+photo+".jpg>"+
	                                                 "<h4>NAME: "+name+"</h4>"+
	                                                 "<img src="+sign+".jpg>"+
	                                                 "<h4>ROLL NO.: "+roll+"</h4>"+
	                                                 "<h4>DATE OF BIRTH: "+dob+"</h4>"+
	                                                 "<h4>PROGRAMME: "+prog+"</h4>"+
	                                                 "<h4>BRANCH: "+branch+"</h4>"+
	                                                 "<h4>BATCH: "+batch+"</h4>"+
	                                                 "<h4>ADDRESS: "+preaddress+"</h4>"+
	                                                 "<h4>MOBILE NO.: "+mob+"</h4>"+
	                                                 "<h4>ALTERNATE MOBILE NO.: "+pmob+"</h4>"+
	                                                 "<h4>CGPA: "+cgpa+"</h4>"+
	                                                 "<h4>SKILLS: "+skills+"</h4>";
  Export2Word('exportContent')
}   

 function Export2Word(element, filename = ''){
    var preHtml = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'><head><meta charset='utf-8'><title>Export HTML To Doc</title></head><body>";
    var postHtml = "</body></html>";
    var html = preHtml+document.getElementById(element).innerHTML+postHtml;

    var blob = new Blob(['\ufeff', html], {
        type: 'application/msword'
    });
    
    // Specify link url
    var url = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(html);
    
    // Specify file name
    filename = filename?filename+'.doc':'resume.doc';
    
    // Create download link element
    var downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);
    
    if(navigator.msSaveOrOpenBlob ){
        navigator.msSaveOrOpenBlob(blob, filename);
    }else{
        // Create a link to the file
        downloadLink.href = url;
        
        // Setting the file name
        downloadLink.download = filename;
        
        //triggering the function
        downloadLink.click();
    }
    
    document.body.removeChild(downloadLink);
}
 
const paragraph = document.getElementById("edit");
const paragraph1 = document.getElementById("edit1");
 
const edit_button = document.getElementById("edit-button");
const end_button = document.getElementById("end-editing");

edit_button.addEventListener("click", function() {
  paragraph.contentEditable = true;
  paragraph1.contentEditable = true;
  paragraph.style.backgroundColor = "#FAEBD7";
  paragraph1.style.backgroundColor = "#FAEBD7";

} );

end_button.addEventListener("click", function() {
  paragraph.contentEditable = false;
  paragraph1.contentEditable = false;
  paragraph.style.backgroundColor = "#FFFFFF";
  paragraph1.style.backgroundColor = "#FFFFFF";
} )