<?php
// prevent timezone warnings
date_default_timezone_set('America/New_York');

// set the upload location
$UPLOADDIR = "images/";

// if the form has been submitted then save and display the image(s)
if(isset($_POST['Submit'])){
    // loop through the uploaded files
    foreach ($_FILES as $key => $value){
        $image_tmp = $value['tmp_name'];
        $image = $value['name'];
        $image_file = "{$UPLOADDIR}{$image}";

        // move the file to the permanent location
        if(move_uploaded_file($image_tmp,$image_file)){
            echo <<<HEREDOC
<div style="float:left;margin-right:10px">
    <img src="{$image_file}" alt="file not found" /></br>
</div>
HEREDOC;
        }
        else{
            echo "<h1>image file upload failed, image too big after compression</h1>";
        }
    }
}
else{
    ?>
<form name='newad' method='post' enctype='multipart/form-data' action=''>
    <table>
    <tr>
        <td><input type='file' name='image'></td>
    </tr>
    <tr>
        <td><input name='Submit' type='submit' value='Upload image'></td>
    </tr>
</table>
</form>
<?php
}
?>