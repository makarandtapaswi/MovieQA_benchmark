"""MovieQA - Story Understanding Benchmark.

Data loader for reading movies and multiple-choice QAs

http://movieqa.cs.toronto.edu/

Release: v1.0
Date: 18 Nov 2015
"""

from collections import namedtuple
import json

import config as cfg
import story_loader


TextSource = namedtuple('TextSource', 'plot dvs subtitle script')

# TODO: add characters info
MovieInfo = namedtuple('Movie', 'name year genre text video')

QAInfo = namedtuple('QAInfo',
                    'qid question answers correct_index imdb_key video_clips')

class DataLoader(object):
    """MovieQA: Data loader class"""

    def __init__(self):
        self.load_me_stories = story_loader.StoryLoader()

        self.movies_map = dict()
        self.qa_list = list()
        self.data_split = dict()

        self._populate_movie()
        self._populate_splits()
        self._populate_qa()
        print 'Initialized MovieQA data loader!'

    # region Initialize and Load class data
    def _populate_movie(self):
        """Create a map of (imdb_key, MovieInfo) and its inversed map.
        """
        with open(cfg.MOVIES_JSON, 'r') as f:
            movies_json = json.load(f)

        for movie in movies_json:
            t = movie['text']
            ts = TextSource(t['plot'], t['dvs'], t['subtitle'], t['script'])
            vs = None
            self.movies_map[movie['imdb_key']] = MovieInfo(
                movie['name'], movie['year'], movie['genre'], ts, vs)

        self.movies_map_inv = {(v.name + ' ' + v.year):k
                               for k, v in self.movies_map.iteritems()}

    def _populate_qa(self):
        """Create a list of QaInfo for all question and answers.
        """
        with open(cfg.QA_JSON, 'r') as f:
            qa_json = json.load(f)

        for qa in qa_json:
            self.qa_list.append(
                QAInfo(qa['qid'], qa['question'], qa['answers'], qa['correct_index'],
                       qa['imdb_key'], qa['video_clips']))

    def _populate_splits(self):
        """Get the list of movies in each split.
        """
        with open(cfg.SPLIT_JSON, 'r') as f:
            self.data_split = json.load(f)

    # endregion

    # region Pretty-Print :)
    def pprint_qa(self, qa):
        """Pretty print a QA.
        """
        print '----------------------------------------'
        movie = self.movies_map[qa.imdb_key]
        print 'Movie: %s %s' % (movie.name, movie.year)
        print 'Question: %s' % qa.question
        print 'Options:'
        for k, ans in enumerate(qa.answers):
            if qa.correct_index == k:
                print '***',
            print '\t%s' % ans
        print '----------------------------------------'


    def pprint_movie(self, movie):
        """Pretty print a Movie.
        """
        print '----------------------------------------'
        print 'Movie: %s %s' % (movie.name, movie.year)
        print 'Genre: %s' % movie.genre
        print 'Available texts:'
        for k, v in movie.text._asdict().iteritems():
            print '%s: %s' % (k.rjust(12), v)
        print '----------------------------------------'

    # endregion

    def get_split_movies(self, split):
        """Get the list of movies in this split.

        Raises:
          ValueError:   If input split type is unrecognized.
        """
        this_split_movies = []
        if split == 'train':
            this_split_movies = self.data_split['train']
        elif split == 'val':
            this_split_movies = self.data_split['val']
        elif split == 'test':
            this_split_movies = self.data_split['test']
        elif split == 'full':
            this_split_movies = list(self.data_split['train'])
            this_split_movies.extend(self.data_split['val'])
            this_split_movies.extend(self.data_split['test'])
        else:
            raise ValueError('Invalid split type. Use "train", "val", "test", or "full"')

        return this_split_movies


    def get_story_qa_data(self, split='train', story_type='plot'):
        """Provide data based on a particular split and story-type.

        Args:
          split:        'train' OR 'val' OR 'test' OR 'full'.
          story_type:   'plot', 'split_plot', 'subtitle', 'dvs', 'script'.

        Returns:
          story:        Story for each movie indexed by imdb_key.
          qa:           The list of QAs in this split.
        """
        this_split_movies = self.get_split_movies(split)

        # Load story
        this_movies_map = {k: v for k, v in self.movies_map.iteritems()
                           if k in this_split_movies}
        story = self.load_me_stories.load_story(this_movies_map, story_type)

        # Restrict this split movies to ones which have a story,
        # get restricted QA list
        this_split_movies = [m for m in this_split_movies if m in story]
        qa = [qa for qa in self.qa_list if qa.imdb_key in this_split_movies]

        return story, qa


    def get_video_list(self, split='train', video_type='qa_clips'):
        """Provide data for a particular split and video type.

        Args:
          split:        'train' OR 'val' OR 'test' OR 'full'.
          video_type:   'qa_clips', 'all_clips'.

        Returns:
          video_list:   List of videos indexed by qid (for clips) or movie (for full).
          qa:           The list of QAs in this split.

        Raises:
          ValueError:   If input video type is unrecognized.
        """
        this_split_movies = self.get_split_movies(split)

        # Get all video QAs
        qa = [qa for qa in self.qa_list if qa.video_clips and qa.imdb_key in this_split_movies]

        video_list = {}
        if video_type == 'qa_clips':
            # add each qa's video clips to video list
            for qa_one in qa:
                video_list.update({qa_one.qid:qa_one.video_clips})

        elif video_type == 'all_clips':
            # collect list of clips by movie
            for qa_one in qa:
                if qa_one.imdb_key in video_list.keys():
                    video_list[qa_one.imdb_key].extend(qa_one.video_clips)
                else:
                    video_list.update({qa_one.imdb_key:list(qa_one.video_clips)})

            # keep non-repeated clips
            for imdb_key in video_list.keys():
                video_list[imdb_key] = list(set(video_list[imdb_key]))

        else:
            raise ValueError('Invalid video type. Use "qa_clips" or "all_clips"')

        return video_list, qa

