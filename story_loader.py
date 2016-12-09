"""MovieQA - Story Understanding Benchmark.

Story loaders for reading plots, subtitles, DVS, etc.

http://movieqa.cs.toronto.edu/

Release: v1.0
Date: 18 Nov 2015
"""

import os
import re
import pysrt

import config
PKG = config.PACKAGE_DIRECTORY

dvs_rep = re.compile('^\d+-\d+')
dvs_cur = re.compile('\{.+?\}')
quote_matches = re.compile('<.+?>')


class StoryLoader(object):
    """Data loader class."""

    def __init__(self):
        self.available_types = ['plot', 'split_plot', 'subtitle', 'dvs', 'script']

    def _check_exists(self, filename):
        """Check that the story file exists and is OK to load.
        """
        if os.path.exists(filename):  # git repo OK!
            return True
        return False

    def _read_plot(self, plot_filename):
        """Read a plot synopsis file.
        Also used to read split plots, where each line contains one sentence of the plot.
        """
        with open(plot_filename) as f:
            plot = f.readlines()
        plot = [p.strip() for p in plot]
        plot = [p for p in plot if p]
        return plot

    def _read_subtitle(self, subtitle_filename):
        """Read the subtitle file and output dialogs.
        """
        subtitle_text = pysrt.open(subtitle_filename, encoding='iso-8859-1')
        subtitle_text = [l.strip() for l in subtitle_text.text.split('\n')]
        subtitle_text = [quote_matches.sub('', l).strip() for l in subtitle_text]

        # Prepare dialogs
        dialogs = []
        create_new_dialog = True
        for l in subtitle_text:
            if not l: # Get rid of newlines
                continue
            if create_new_dialog:
                dialogs.append([l])  # Start new dialog
            else:
                dialogs[-1].append(l)  # Append to last dialog

            # Decide what to do with next line based on current line ending
            create_new_dialog = False
            if l[-1] in ['.', '!', '?', ':', ')']:
                create_new_dialog = True

        # Join the lists to form single dialogs
        for d in range(len(dialogs)):
            dialogs[d] = ' '.join(dialogs[d])

        return dialogs

    def _read_dvs(self, dvs_filename):
        """Read a DVS file.
        """
        dvs_text = pysrt.open(dvs_filename, encoding='iso-8859-1')
        dvs_text = [l.strip() for l in dvs_text.text.split('\n')]
        dvs_text = [quote_matches.sub('', l).strip() for l in dvs_text]

        # Cleanup DVS (remove the DVS index and stuff in {})
        for k in range(len(dvs_text)):
            dvs_text[k] = dvs_rep.sub('', dvs_text[k]).strip()
            dvs_text[k] = dvs_cur.sub('', dvs_text[k]).strip()

        return dvs_text

    def load_story(self, movies_map, story_type='plot'):
        """Load story files for given set of movies.

        Args:
          movies_map: Dictionary of movie named tuples.
          story_type: 'plot', 'split_plot', 'subtitle', 'dvs', 'script'.

        Returns:
          story: Story for each movie indexed by imdb_key.

        Raises:
          ValueError: If input story type is not supported.
        """
        story = {}
        for imdb_key, movie in movies_map.iteritems():
            if story_type == 'plot':
                if not movie.text.plot:
                    continue
                plot_filename = os.path.join(PKG, movie.text.plot)
                if not self._check_exists(plot_filename):
                    continue
                this_story = self._read_plot(plot_filename)

            elif story_type == 'split_plot':
                fname = 'story/split_plot/' + imdb_key + '.split.wiki'
                split_plot_filename = os.path.join(PKG, fname)
                if not self._check_exists(split_plot_filename):
                    continue
                this_story = self._read_plot(split_plot_filename)

            elif story_type == 'subtitle':
                if not movie.text.subtitle:
                    continue
                subtitle_filename = os.path.join(PKG, movie.text.subtitle)
                if not self._check_exists(subtitle_filename):
                    continue
                this_story = self._read_subtitle(subtitle_filename)

            elif story_type == 'dvs':
                if not movie.text.dvs:
                    continue
                dvs_filename = os.path.join(PKG, movie.text.dvs)
                if not self._check_exists(dvs_filename):
                    continue
                this_story = self._read_subtitle(dvs_filename)

            elif story_type == 'script':
                if not movie.text.script:
                    continue
                script_filename = os.path.join(PKG, movie.text.script)
                if not self._check_exists(script_filename):
                    continue
                this_story = self._read_plot(script_filename)

            else:
                raise ValueError('Unsupported story type!')

            story[imdb_key] = this_story

        if not story:
            raise ValueError('Story returned empty!')

        return story
