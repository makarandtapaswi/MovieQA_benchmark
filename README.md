# MovieQA

<strong>MovieQA: Understanding Stories in Movies through Question-Answering</strong>  
Makarand Tapaswi, Yukun Zhu, Rainer Stiefelhagen, Antonio Torralba, Raquel Urtasun, and Sanja Fidler  
IEEE Conference on Computer Vision and Pattern Recognition (CVPR), Las Vegas, June 2016.  
[Project page](http://movieqa.cs.toronto.edu) |
[arXiv preprint](http://arxiv.org/abs/1512.02902) |
[Read the paper](http://movieqa.cs.toronto.edu/static/files/CVPR2016_MovieQA.pdf) |
[Explore the data](http://movieqa.cs.toronto.edu/examples/)

----

### Benchmark Data
The data is made available in simple JSON / text files for easy access in any environment. We provide Python scripts to help you get started by providing simple data loaders.

To obtain access to the stories, and evaluate new approaches on the test data, please register at our [benchmark website](http://movieqa.cs.toronto.edu/).


### Python data loader
<code>import MovieQA</code>  
<code>mqa = MovieQA.DataLoader()</code>

#### Explore
Movies are indexed using their corresponding IMDb keys. For example  
<code>mqa.pprint_movie(mqa.movies_map['tt0133093'])</code>

QAs are stored as a standard Python list  
<code>mqa.pprint_qa(mqa.qa_list[0])</code>

#### Use
Get the list of movies in a particular split, use  
<code>movie_list = mqa.get_split_movies(split='train')</code>

To get train or test splits of the QA along with a particular story, use  
<code>story, qa = mqa.get_story_qa_data('train', 'plot')</code>

Supported splits are: <code>train, val, test, full</code> and story forms are: <code>plot, subtitle, dvs, script</code>

Video lists can be obtained per QA, or per movie using  
<code>vl_qa, _ = get_video_list('train', 'qa_clips')  % per QA</code>  
<code>vl_movie, _ = get_video_list('train', 'all_clips')  % per movie</code>


#### Build your own data/story loaders
We provide a simple interface to load all the data (QAs, movies) and stories through the code above.
If you wish to modify something, you are welcome to use your own data loaders and access the raw data directly.
The evaluation server submissions are simple text files (explained after login) and are independent of any data loaders.

----

### Requirements
- numpy
- pysrt


