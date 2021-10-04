## Useful material on wildfire detection

### Datasets
* https://www.sciencedirect.com/science/article/pii/S1389128621001201
  
  #### Summary: 
  Hardware: \
  3 different cameras (FLIR, IR), different resolutions and FOVs 
  
  Data: \
  4 types of videos converted to frames (normal spectrum, fusion, white-hot, green-hot). \
  Videos of fire and no-fire. \
  2003 frames for Ground Truth Masks. 
  
  Method: \
  Xception model for binary classification. Code on GitHub, works with Tensorflow 2.3.0 and Keras 2.4.0 \
  U-Net for semantic segmentation \
  !!Note!!: only the visible spectrum videos where used for both.
  
  
  #### Citing Papers:
  * https://www.sciencedirect.com/science/article/pii/S0165168421003467
  * https://ieeexplore.ieee.org/document/9425170
* https://www.researchgate.net/publication/318284024_Computer_vision_for_wildfire_research_An_evolving_image_dataset_for_processing_and_analysis
  * https://www.researchgate.net/publication/340150420_Information-Guided_Flame_Detection_based_on_Faster_R-CNN
  * https://www.researchgate.net/publication/354880874_Squeezed_fire_binary_segmentation_model_using_convolutional_neural_network_for_outdoor_images_on_embedded_device
  * https://www.researchgate.net/publication/348438779_Convolutional_neural_network_for_smoke_and_fire_semantic_segmentation
  * https://www.researchgate.net/publication/344457693_Early_Fire_Detection_Based_on_Aerial_360-Degree_Sensors_Deep_Convolution_Neural_Networks_and_Exploitation_of_Fire_Dynamic_Textures
  * https://www.researchgate.net/publication/344727435_Fire_segmentation_using_a_DeepLabv3_architecture
  * https://www.researchgate.net/publication/348317293_Semantic_Fire_Segmentation_Model_Based_on_Convolutional_Neural_Network_for_Outdoor_Image
  * https://www.researchgate.net/publication/332995092_Application_of_KNN_Algorithm_Based_on_Particle_Swarm_Optimization_in_Fire_Image_Segmentation
  * https://www.researchgate.net/publication/353723135_Color-based_Superpixel_Semantic_Segmentation_for_Fire_Data_Annotation
  * https://www.researchgate.net/publication/330934497_Fire_Detection_from_Images_using_Faster_R-CNN_and_Multidimensional_Texture_Analysis
  * https://www.researchgate.net/publication/337527021_A_new_artificial_bee_colony_algorithm-based_color_space_for_fireflame_detection
  * https://www.researchgate.net/publication/327326242_Low-Light_Forest_Flame_Image_Segmentation_Based_on_Color_Features
* https://www.mdpi.com/2673-2688/1/2/10
  * https://www.mdpi.com/1424-8220/20/22/6442
* https://github.com/aiformankind/wildfire-smoke-dataset
  * https://www.sciencedirect.com/science/article/abs/pii/S0379711216301059
  * https://www.inf.fu-berlin.de/inst/ag-ki/rojas_home/documents/Betreute_Arbeiten/Master-Hohberg.pdf
