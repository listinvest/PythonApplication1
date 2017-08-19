import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import RPi.GPIO as GPIO
import time

#GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        try:
            self.write_message("Connected...")
        
        except Exception as a:
            print(a)


    def on_message(self, message):
        try:
            print message
            data = message.split( " " )

            # while message:
            #   data = message.split( " " )
            #   GPIO.output(12,True)
            #   GPIO.output(15,True)
            #   if not me:
            #       break 


            if ( data [0] == "1" and data [1] == "0" and data [2] == "0" ):

                GPIO.output(12,True)
                GPIO.output(15,True)
            
            elif ( data [0] == "0" and data [1] == "1" and data [2] == "0" ):

                GPIO.output(11,True)
                GPIO.output(15,True)

            elif ( data [0] == "0" and data [1] == "-1" and data [2] == "0" ):

                GPIO.output(12,True)
                GPIO.output(13,True)

            else:
                #print "ELSE"
                GPIO.output(11,False)
                GPIO.output(12,False)
                GPIO.output(13,False)
                GPIO.output(15,False)               

        except Exception as a:
            print("Error: ", a)

        # else:
        #   print "ELSE"
        #   GPIO.output(11,False)
        #   GPIO.output(12,False)
        #   GPIO.output(13,False)
        #   GPIO.output(15,False)

        finally:
            print "FINALLY"
            GPIO.output(11,False)
            GPIO.output(12,False)
            GPIO.output(13,False)
            GPIO.output(15,False)

 

    def on_close(self):
        print ("closing sockets")
        GPIO.output(11,False)
        GPIO.output(12,False)
        GPIO.output(13,False)
        GPIO.output(15,False)   


    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r"/ws", WSHandler),
])


if __name__ == "__main__":

    try:
        http_server = tornado.httpserver.HTTPServer(application)
        print ("Waiting client connection via browser port 8888")
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        print "Exiting..."

    except:
        print "Other error or exception occurred!"

    finally:
        GPIO.cleanup()
        print "GPIO clean"