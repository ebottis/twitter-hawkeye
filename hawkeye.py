from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import deets
from TwitterAPI import TwitterAPI

camera = PiCamera()

consumer_key = deets.twitter_consumer_key
consumer_secret = deets.twitter_consumer_secret
access_token_key = deets.twitter_access_token_key
access_token_secret = deets.twitter_access_token_secret


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=takePhoto, bouncetime=300)


def takePhoto(pin):
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    print("Takephoto")
    camera.capture('hawk.jpg')
    sleep(.1)
    file = open('hawk.jpg', 'rb')
    data = file.read()
    r = api.request('statuses/update_with_media', {'status':'Brownie Hawkeye Twitter Cam #T550 #remix #week6'}, {'media[]':data})
    print(r.status_code)

def write_csv(*args):
    try:
        with open('kid_data.csv', 'a', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            data_list = list(args)
            data_list.insert(0, datetime.datetime.now())
            data_writer.writerow(data_list)
    except Exception as e:
        print(e)
        pass

def send_sms(msg):
    try:
        client = Client(deets.twilio_sid, deets.twilio_token)
        message = client.messages.create(
        to= deets.my_phone, 
        from_= deets.twilio_phone,body=deets.card + " " + msg)
    
    except Exception as e:
        write_csv("sms error", str(e))

setup()

try:
    while True:
        pass
except Exception as e:
    write_csv("error: ", str(e))
    send_sms("error: " + str(e))
