
# Traffic

<p>Write an AI to identify which traffic sign appears in a photograph.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python traffic.py gtsrb
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
Epoch 4/10
500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
Epoch 8/10
500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
Epoch 9/10
500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
Epoch 10/10
500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
333/333 - 5s - loss: 0.1616 - accuracy: 0.9535
</code></pre></div></div>



<h2 id="background">Background</h2>

<p>As research continues in the development of self-driving cars, one of the key challenges is <a href="https://en.wikipedia.org/wiki/Computer_vision">computer vision</a>, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.</p>

<p>In this project, you’ll use <a href="https://www.tensorflow.org/">TensorFlow</a> to build a neural network to classify road signs based on an image of those signs. To do so, you’ll need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.</p>

<p>Several such data sets exist, but for this project, we’ll use the <a href="http://benchmark.ini.rub.de/?section=gtsrb&amp;subsection=news">German Traffic Sign Recognition Benchmark</a> (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs.</p>



<h2 id="understanding">Understanding</h2>

<p>First, take a look at the data set by opening the <code class="language-plaintext highlighter-rouge">gtsrb</code> directory. You’ll notice 43 subdirectories in this dataset, numbered <code class="language-plaintext highlighter-rouge">0</code> through <code class="language-plaintext highlighter-rouge">42</code>. Each numbered subdirectory represents a different category (a different type of road sign). Within each traffic sign’s directory is a collection of images of that type of traffic sign.</p>

<p>Next, take a look at <code class="language-plaintext highlighter-rouge">traffic.py</code>. In the <code class="language-plaintext highlighter-rouge">main</code> function, we accept as command-line arguments a directory containing the data and (optionally) a filename to which to save the trained model. The data and corresponding labels are then loaded from the data directory (via the <code class="language-plaintext highlighter-rouge">load_data</code> function) and split into training and testing sets. After that, the <code class="language-plaintext highlighter-rouge">get_model</code> function is called to obtain a compiled neural network that is then fitted on the training data. The model is then evaluated on the testing data. Finally, if a model filename was provided, the trained model is saved to disk.</p>

<p>The <code class="language-plaintext highlighter-rouge">load_data</code> and <code class="language-plaintext highlighter-rouge">get_model</code> functions are left to you to implement.</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementation of <code class="language-plaintext highlighter-rouge">load_data</code> and <code class="language-plaintext highlighter-rouge">get_model</code> in <code class="language-plaintext highlighter-rouge">traffic.py</code>.</p>

<ul>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">load_data</code> function should accept as an argument <code class="language-plaintext highlighter-rouge">data_dir</code>, representing the path to a directory where the data is stored, and return image arrays and labels for each image in the data set.
    <ul>
      <li data-marker="*">You may assume that <code class="language-plaintext highlighter-rouge">data_dir</code> will contain one directory named after each category, numbered <code class="language-plaintext highlighter-rouge">0</code> through <code class="language-plaintext highlighter-rouge">NUM_CATEGORIES - 1</code>. Inside each category directory will be some number of image files.</li>
      <li data-marker="*">Use the OpenCV-Python module (<code class="language-plaintext highlighter-rouge">cv2</code>) to read each image as a <code class="language-plaintext highlighter-rouge">numpy.ndarray</code> (a <code class="language-plaintext highlighter-rouge">numpy</code> multidimensional array). To pass these images into a neural network, the images will need to be the same size, so be sure to resize each image to have width <code class="language-plaintext highlighter-rouge">IMG_WIDTH</code> and height <code class="language-plaintext highlighter-rouge">IMG_HEIGHT</code>.</li>
      <li data-marker="*">The function should return a tuple <code class="language-plaintext highlighter-rouge">(images, labels)</code>. <code class="language-plaintext highlighter-rouge">images</code> should be a list of all of the images in the data set, where each image is represented as a <code class="language-plaintext highlighter-rouge">numpy.ndarray</code> of the appropriate size. <code class="language-plaintext highlighter-rouge">labels</code> should be a list of integers, representing the category number for each of the corresponding images in the <code class="language-plaintext highlighter-rouge">images</code> list.</li>
      <li data-marker="*">Your function should be platform-independent: that is to say, it should work regardless of operating system. Note that on macOS, the <code class="language-plaintext highlighter-rouge">/</code> character is used to separate path components, while the <code class="language-plaintext highlighter-rouge">\</code> character is used on Windows. Use <a href="https://docs.python.org/3/library/os.html"><code class="language-plaintext highlighter-rouge">os.sep</code></a> and <a href="https://docs.python.org/3/library/os.path.html#os.path.join"><code class="language-plaintext highlighter-rouge">os.path.join</code></a> as needed instead of using your platform’s specific separator character.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">get_model</code> function should return a compiled neural network model.
    <ul>
      <li data-marker="*">You may assume that the input to the neural network will be of the shape <code class="language-plaintext highlighter-rouge">(IMG_WIDTH, IMG_HEIGHT, 3)</code> (that is, an array representing an image of width <code class="language-plaintext highlighter-rouge">IMG_WIDTH</code>, height <code class="language-plaintext highlighter-rouge">IMG_HEIGHT</code>, and <code class="language-plaintext highlighter-rouge">3</code> values for each pixel for red, green, and blue).</li>
      <li data-marker="*">The output layer of the neural network should have <code class="language-plaintext highlighter-rouge">NUM_CATEGORIES</code> units, one for each of the traffic sign categories.</li>
      <li data-marker="*">The number of layers and the types of layers you include in between are up to you. You may wish to experiment with:
        <ul>
          <li data-marker="*">different numbers of convolutional and pooling layers</li>
          <li data-marker="*">different numbers and sizes of filters for convolutional layers</li>
          <li data-marker="*">different pool sizes for pooling layers</li>
          <li data-marker="*">different numbers and sizes of hidden layers</li>
          <li data-marker="*">dropout</li>
        </ul>
      </li>
    </ul>
  </li>
  <li data-marker="*">In a separate file called <em>README.md</em>, document (in at least a paragraph or two) your experimentation process. What did you try? What worked well? What didn’t work well? What did you notice?</li>
</ul>

<p>Ultimately, much of this project is about exploring documentation and investigating different options in <code class="language-plaintext highlighter-rouge">cv2</code> and <code class="language-plaintext highlighter-rouge">tensorflow</code> and seeing what results you get when you try them!</p>

<p>You should not modify anything else in <code class="language-plaintext highlighter-rouge">traffic.py</code> other than the functions the specification calls for you to implement, though you may write additional functions and/or import other Python standard library modules. You may also import <code class="language-plaintext highlighter-rouge">numpy</code> or <code class="language-plaintext highlighter-rouge">pandas</code>, if familiar with them, but you should not use any other third-party Python modules. You may modify the global variables defined at the top of the file to test your program with other values.</p>

