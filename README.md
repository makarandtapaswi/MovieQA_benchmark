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

---

#### qa.json
- <code>qid</code>: A unique id for every question. Also indicates, train|val|test sets
- <code>imdb_key</code>: The movie this question belongs to
- <code>question</code>: The question string
- <code>answers</code>: The five answer options
- <code>correct_index</code>: Correct answer option (indexed by 0)
- <code>plot_alignment</code>: split_plot file line numbers, to which this question corresponds
- <code>video_clips</code>: Clips that are aligned with the question, to be used for answering


#### movies.json
- <code>imdb_key</code>: A unique id for every movie. Corresponds to that used by IMDb
- <code>name</code>: Movie title
- <code>year</code>: Movie release year
- <code>genre</code>: Movie genre classification
- <code>text</code>: Text sources that are available for that movie


----

### Data Releaselog
- 2017.01.14: Alignments between question and plot sentence, plot sentence and video clips
- 2016.11.08: Patch for 65 missing video clips
- 2016.09.10: Video meta-data released: Shot boundaries, frame-timestamp correspondence
- 2016.04.06: Removed missing video clips from qa.json
- 2016.03.30: v1.0 data release


----

### Requirements
- numpy
- pysrt


