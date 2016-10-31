from weather_webplot import wplot


[script,div,latest] = wplot()

##################################################################

html_str1 = """

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="images/favicon.ico">

    <title>Warner Weather</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="css/bootstrap-theme.min.css" rel="stylesheet">

    <!-- Fonts from Font Awsome -->
    <link rel="stylesheet" href="css/font-awesome.min.css">
    <!-- Magnific popup -->
    <link rel="stylesheet" href="css/magnific-popup.css">
    <!-- Custom styles for this template -->
    <link rel="stylesheet" href="css/main.css">
    
    <!-- Color styles -->
    <link rel="stylesheet" href="css/colors/green.css">
    
    <!-- Bokeh --> 
    <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.3.min.css" type="text/css" />
    <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.3.min.js"></script>

"""
##################################################################


html_str2=script



##################################################################


html_str3 = """
    <!-- Feature detection -->
    <script src="js/modernizr-2.6.2.min.js"></script>
    <!-- Fonts -->
    <link href='http://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,900,300italic,400italic,600italic,700italic,900italic' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Oxygen:400,700' rel='stylesheet' type='text/css'>
    
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body role="document">

  <!--===============================================================================-->

    <!-- Fixed navbar -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
	    <li><a href="">Current Conditions</a></li>
            <li><a href="about.html">Documentation</a></li>
	    <li><a href="days/index.html">Archive</a></li>
	    <li><a href="http://jetolan.github.io/">About Me</a></li>
              </ul>
            </li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    <!--===============================================================================-->

    <!-- Current Conditions -->
    <div id="current">
    <section id="page-profile" class="page-profile">
      <div class="container">
                <header class="section-header">
                    <h2 class="section-title">Current Conditions</h2>
                </header>
            <div class="row">
               <div class="col-md-9">
                 <p style="font-size: 22px">Time :   """+str(latest['time'])[:-10]+"""</p>
                 <p style="font-size: 22px">Air Temperature :   """+str(latest['temp'])[:-8]+""" C</p>
                 <p style="font-size: 22px">Barometric Pressure :   """+str(latest['pressure'])[:-8]+""" inHg</p>
                 <p style="font-size: 22px">Humidity :   """+str(latest['humidity'])[:-8]+""" %</p>
                 <p style="font-size: 22px">Dew Point :   """+str(latest['dew_point'])[:-8]+""" C</p>
               </div>
            </div>
      </div> 
    </section><!-- current -->
</div>

    <!--===============================================================================-->

    <!-- Plot -->
    <div id="plot">
    <section id="page-profile" class="page-profile">
      <div class="container">
            <div class="row">
            <center>
            """

##################################################################

html_str4 = div

##################################################################

html_str5 = """
           </center>
	    </div>
      </div> 
    </section><!-- plot -->
</div>
    <!--===============================================================================-->


<!-- END ROW -->

</div>
</section>
</div>
     <!--===============================================================================-->
   <!-- Footer -->
	<footer id="footer">
	


 		<div class="copyright">
			<div class="menu">
				<p>&copy; Jamie Tolan 2016</p>
				<a href="#">Back to top</a></p>

	</footer>


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    
    <script src="js/jquery.scrollTo.js"></script>
    <script src="js/jquery.nav.js"></script>
    <script src="js/jquery.sticky.js"></script>
    <script src="js/jquery.easypiechart.min.js"></script>
    <script src="js/jquery.vegas.min.js"></script>
    <script src="js/jquery.isotope.min.js"></script>
    <script src="js/jquery.magnific-popup.min.js"></script>
    <script src="js/jquery.validate.js"></script>
    <script src="js/waypoints.min.js"></script>
    <script src="js/main.js"></script>
    <script src="js/contact_me.js"></script>
    <script src="js/jqBootstrapValidation.js"></script>

  </body>
</html>


"""


##################################################################


str_out=html_str1+html_str2+html_str3+html_str4+html_str5


##################################################################

Html_file= open("index.html","w")
Html_file.write(str_out)
Html_file.close()
