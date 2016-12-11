import os
import requests
import datetime
from pytz import timezone

dt=datetime.datetime.now()
loc_tz = timezone('US/Pacific')
utc_tz = timezone('UTC')

utc_dt=utc_tz.localize(dt)
loc_dt=utc_dt.astimezone(loc_tz)
time=loc_dt.strftime("%Y-%m-%d %H:%M:%S")

html_str1 = """
<!DOCTYPE html>
<html lang="en">
  <head>
</head>
<body>
Updated at: 
"""

html_str2 = time

html_str3 = """
<br>
Raspi3 = 
"""

r=requests.get('http://ipecho.net/plain')
html_str4 = r.content

html_str5 = """
   </body>
</html>
"""
str_out= html_str1 + html_str2 + html_str3 + html_str4 + html_str5

##################################################################

Html_file= open("/home/pi/weather/web/address.html","w")
Html_file.write(str_out)
Html_file.close()
