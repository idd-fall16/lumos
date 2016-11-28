<!DOCTYPE html>
<html>
<body>

<form enctype="multipart/form-data" action="uploader.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="100000" />
Choose a file to upload: <input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />


<!-- <form method="post" action="uploader.php" enctype="multipart/form-data">
  <input name="filesToUpload[]" id="filesToUpload" type="file" multiple="" />
  <input type="submit" value="Upload File" />
 -->
<!-- </form>
 -->
<?php

// Where the file is going to be placed 
$target_path = "../uploads/";

/* Add the original filename to our target path.  
Result is "uploads/filename.extension" */
$target_path = $target_path . basename( $_FILES['uploadedfile']['name']); 

if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
    echo "The file ".  basename( $_FILES['uploadedfile']['name']). 
    " has been uploaded";
} else{
    echo "There was an error uploading the file, please try again!";
}

?>


</form>
</body>
</html>
