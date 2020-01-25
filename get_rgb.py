import cv2
import os
import roslaunch
import rospy

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sound_play.libsoundplay import SoundClient
from sound_play.msg import SoundRequest

cnt = 0 
image_folder = "."

def frames_to_video():
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=os.path.getmtime)

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter("out.avi", 0, 30, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
   
    for img in images:
        os.remove(img)


def callback(data):
    global cnt
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imwrite(str(cnt) + ".png", cv_image)
    cnt += 1
    
    # rospy.loginfo("I heard %s %s", str(data.height), str(data.width))
    
def listener():
    rospy.Subscriber("/webcam/image_raw", Image, callback)
    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()


rospy.init_node('rgb_getter_node', anonymous=True)
bridge = CvBridge()
listener()

uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/comy/sim/video.launch"])
launch.start()
rospy.loginfo("started")

while(1):
    try:
        rospy.wait_for_message("/webcam/image_raw", Image, timeout=5)
    except:
        print("Gata")
        frames_to_video()
        break

# TODO(Cosmina): Add HAR module.

result = "play the guitar"

soundhandle = SoundClient()
rospy.sleep(1)
voice = 'voice_kal_diphone'
# voice = 'voice_us1_mbrola'
volume = 1.0

soundhandle.say(result, voice, volume)

launch.shutdown()
rospy.spin()

