<!DOCTYPE html>
<?php include("/Applications/MAMP/htdocs/php-file-uploader/password_protect.php"); ?>

<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Lumos | Send Light</title>

    <!-- Bootstrap core CSS -->
    <link href="./boostrap/css/bootstrap.min.css" rel="stylesheet">
   
  </head>

  <body>

    <!-- Static navbar -->
    <div class="navbar navbar-default navbar-static-top">
      <div class="container">
        <div class="navbar-header">
          <div class="navbar-brand"> LUMOS | Send Light</div>
        </div>
      </div>
    </div>


    <div class="container">
    	<div class="profile">Upload photos for <strong>Mimmy Chong</strong> to view in her room.  Your photos will be projected onto the room's ceiling. </div>
    
    	<div class="row">
	       <?php 
	       	//scan "uploads" folder and display them accordingly
	       $folder = "uploads";
	       $results = scandir('uploads');
	       foreach ($results as $result) {
	       	if ($result === '.' or $result === '..') continue;
	       
	       	if (is_file($folder . '/' . $result)) {
	       		echo '
	       		<div class="col-md-3">
		       		<div class="thumbnail">
			       		<img src="'.$folder . '/' . $result.'" alt="...">
				       		<div class="caption">
				       		<p><a href="remove.php?name='.$result.'" class="btn btn-danger btn-xs" role="button">Remove</a></p>
			       		</div>
		       		</div>
	       		</div>';
	       	}
	       }
	       ?>
    	</div>
    	
		

	      <div class="row">
	      	<div class="col-lg-12">
	           <form class="well" action="upload.php" method="post" enctype="multipart/form-data">
				  <div class="form-group">
				    <label for="file">Select a file to upload</label>
				    <input type="file" name="file">
				    <p class="help-block">Upload JPG, JPEG, PNG and GIF files with maximum size of 1 MB.</p>
				  </div>
				  <input type="submit" class="btn btn-lg btn-primary" value="Upload">
				</form>
			</div>
	      </div>
    </div> <!-- /container -->

  </body>
</html>