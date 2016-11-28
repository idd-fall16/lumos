<!DOCTYPE html>
<html >
<head>
  <meta charset="UTF-8">
  <title>Simple jQuery Slideshow</title>
  
  
  
      <link rel="stylesheet" href="css/style.css">

  
</head>

<body>
  <?php

  // open this directory 
  $myDirectory = opendir("uploads");

  // get each entry
  while($entryName = readdir($myDirectory)) {
    $dirArray[] = $entryName;
  }

  // close directory
  closedir($myDirectory);

  //  count elements in array
  $indexCount = count($dirArray);
  // echo $indexCount

  ?>

  <div id="slideshow">
    <?php
      for($index=0; $index < $indexCount; $index++) {
        $extension = substr($dirArray[$index], -3);
        if ($extension == 'jpg' || $extension == 'png' || $extension == 'jpeg' || $extension == 'gif'){ 
          // $dirArray[$index] IS THE NAME OF THE FILE CAN USE THAT IN SOME HTML
          // save this in an array and use for slideshow
          // echo $dirArray[$index];
          echo '<div id="show"><img src="./uploads/' . $dirArray[$index] . '" alt="Image"></div>';
        } 
      }
    ?>
  </div>

<!--      <img src="http://farm6.static.flickr.com/5224/5658667829_2bb7d42a9c_m.jpg">
   </div>
   <div>
     <img src="http://farm6.static.flickr.com/5230/5638093881_a791e4f819_m.jpg">
   </div>
   <div>
     Pretty cool eh? This slide is proof the content can be anything.
   </div>
</div> -->
  
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>

    <script src="js/index.js"></script>

</body>
</html>



<!--
Copyright (c) 2016 by Chris Coyier (http://codepen.io/chriscoyier/pen/zKbYzP)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-->
