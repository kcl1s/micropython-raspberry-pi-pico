import myWifi
from machine import Pin
from neopixel import NeoPixel


numP = 60
neo_pin = Pin(16, Pin.OUT)   
pixels = NeoPixel(neo_pin, numP)
    

def webpage():
    #Template HTML
    html = f"""
           <!DOCTYPE html>
            <html>
            <head>
            <script src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"></script>
            </head>
            <body>

            <h1 style="text-align:center;">Please choose your Neopixel Color</h1>
            <div id="picker" style= "margin:auto;width:50%;"></div>
            <br>
            <h2 id="values" style="color:blue;text-align:center;" ></h2>
            </body>
            <script>
            var colorPicker = new iro.ColorPicker('#picker', {{
              width: 280,
              color: "rgb(255, 0, 0)",
              borderWidth: 1,
              borderColor: "#fff",
            }});
            colorPicker.on('input:end', function(color) {{
                values.innerHTML = [
                "rgb: " + color.rgbString,
                ].join("<br>");
                var xhr = new XMLHttpRequest();
                xhr.open("GET", color.rgbString, true);
                xhr.send();
            }});
            </script>
            </html>
            """
    return str(html)

def serve(connection):
    global demo_number
    #Start a web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print (request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        print (request)
        if '/rgb' in request:
            color_str = request[5:-1]
            print (color_str)
            color_tuple = tuple(map(int, color_str.split(',%20')))
            print (color_tuple)
            pixels.fill(color_tuple)
            pixels.write()
        html = webpage()
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(html)
        client.close()
        
      
connection = myWifi.connect()
serve(connection)
