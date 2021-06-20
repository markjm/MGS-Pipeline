import sys
import os
import errno
import shutil
import argparse
import numpy as np
import tensorflow.compat.v1 as tf
from PIL import Image

FLAGS = None

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

TOP_K = 1

def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(FLAGS.model, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[TOP_K:][::-1]
        f = open(FLAGS.labels, 'rb')
        log = open(FLAGS.log, 'a+')
        lines = f.readlines()
        labels = [w.decode("utf-8").replace("\n", "") for w in lines]
        print('------------------RESULTS-------------------------')
        for node_id in top_k:
            human_string = labels[node_id].strip()
            score = predictions[node_id]

            print('%s - %s (score = %.5f)' %
                  (imagePath[imagePath.index('/')+1:], human_string, score))

            time = ''
            try:
                time = imagePath[imagePath.rindex('_')+1:imagePath.rindex('.')]
                time = time[:time.index('m')] + ':' + time[time.index('m')+1:time.index('s')]
            except:
                time = '0:0'

            log.write('%s, %s, %s, %.5f\n' %
                      (imagePath[imagePath.index('/')+1:], time, human_string, score))

            if FLAGS.copy_images:
                if score < FLAGS.threshold:
                    shutil.copy(imagePath, reviewNC)
                else:
                    shutil.copy(imagePath, reviewC)
        print('---------------------------------------------------')
        answer = labels[top_k[0]]
        return answer


def run_inference_on_images(path):
    for obj in os.listdir(path):
        further_path = os.path.join(path, obj)
        if os.path.isdir(further_path):
            run_inference_on_images(further_path)
        if obj.endswith('.jpg'):
            run_inference_on_image(further_path)


def convert_png_to_jpg(path):
    im = Image.open(path)
    (name, extenstion) = os.path.splitext(path)
    im.save(name +".jpg", "JPEG")
    os.remove(path)

def convert_all_pngs_to_jpg(path):
    for obj in os.listdir(path):
        further_path = os.path.join(path, obj)
        if os.path.isdir(further_path):
            convert_all_pngs_to_jpg(further_path)
        if obj.endswith('.png'):
            convert_png_to_jpg(further_path)

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def restricted_float(x):
    x = float(x)
    if x < 0.5 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

def main(_):
    
    reviewNC = FLAGS.review + 'not_confident/'
    reviewC = FLAGS.review + 'confident/'


    make_sure_path_exists(FLAGS.image_dir)
    make_sure_path_exists(FLAGS.review)
    make_sure_path_exists(reviewNC)
    make_sure_path_exists(reviewC)

    
    # Creates graph from saved GraphDef.
    print('Setting up computation graph.')
    create_graph()
    
    print('Converting images to correct file type.')
    convert_all_pngs_to_jpg(FLAGS.image_dir)
    print('Done converting. All images are now jpegs.')
    
    print('Starting inferences')
    run_inference_on_images(FLAGS.image_dir)
    print('Finished all inferences. Terminating.')


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--image_dir',
      type=str,
      default='images/',
      help='Path to folders of images to be classified.'
  )
  parser.add_argument(
      '--model',
      type=str,
      default='assets/model-v3.pb',
      help='Where the trained graph is saved.'
  )
  parser.add_argument(
      '--labels',
      type=str,
      default='assets/model-v3.txt',
      help='Where the trained graph\'s labels are saved.'
  )
  parser.add_argument(
      '--review',
      type=str,
      default='review/',
      help='Where reviewed images are copied to if copy_images is set to True.'
  )
  parser.add_argument(
      '--log',
      type=str,
      default='log.csv',
      help='Where the log should be generated.'
  )
  parser.add_argument(
      '--copy_images',
      type=bool,
      default=False,
      help='Should images be copied for review.'
  )
  parser.add_argument(
      '--threshold',
      type=restricted_float,
      default=0.65,
      help='Threshold that images below-which are ignored.'
  )
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)











