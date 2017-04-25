import os
import shutil
import numpy as np
import tensorflow as tf
from PIL import Image

#Disables depracation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

imageFilePath = 'images/'
reviewFilePath = 'review (Confidence < 0.65)/'
labeledFilePath = 'labeled (Confidence > 0.65)/'
modelFullPath = 'assets/output_graph.pb'
labelsFullPath = 'assets/output_labels.txt'
logPath = 'log.csv'

TOP_K = 1


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
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
        f = open(labelsFullPath, 'rb')
        log = open(logPath, 'a+')
        lines = f.readlines()
        labels = [w.decode("utf-8").replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            
            try:
                print('%s - %s (score = %.5f)' % (imagePath[imagePath.index('/')+1:], human_string, score))
                time = imagePath[imagePath.rindex('_')+1:imagePath.rindex('.')]
                time = time[:time.index('m')] + ':' + time[time.index('m')+1:time.index('s')]
                log.write('%s, %s, %s, %s, %.5f \n' % (imagePath[imagePath.index('/')+1:], imagePath[imagePath.rindex('_')+1:imagePath.rindex('.')], human_string, time, score))
                if score < 0.65:
                    shutil.copy(imagePath, reviewFilePath)
                else:
                    shutil.copy(imagePath, labeledFilePath)
            except:
                pass

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


if __name__ == '__main__':

    # Creates graph from saved GraphDef.
    print('Setting up computation graph.')
    create_graph()
    
    print('Converting images to correct file type.')
    convert_all_pngs_to_jpg(imageFilePath)
    print('Done converting. All images are now jpegs.')

    print('Starting inferences')
    run_inference_on_images(imageFilePath)
    print('Finished all inferences. Terminating.')











