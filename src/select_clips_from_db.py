#!/usr/bin/env python
# Select clips from creators
# Keep in mind view count, duration to till 10mins and avoid duplicates
from logging import raiseExceptions
from pathlib import Path
import datetime
from dateutil.relativedelta import relativedelta
import subprocess

import pandas as pd
from InquirerPy import prompt

from model.mydb import Mydb
from cfg.data import CLUSTERS
from model.clips import Clip, Compilation


class ClipsSelector:
    def __init__(self, args):
        self.clips = []
        self.nclips = {}
        self.viewtime = {}
        self.duration = 0
        self.df = self._read_clips_from_db(args)
        self.clips_removed = []


    def _read_clips_from_db(self, args):
        def read_clips_from_db(args):
            db = Mydb()
            df_categories =  pd.DataFrame()
            df_clip_ids =  pd.DataFrame()
            df_clusters =  pd.DataFrame()
            df_creators = pd.DataFrame()
            df_game_ids =  pd.DataFrame()
            self.creators = []
            if args.clusters: 
                for c in args.clusters:
                    self.creators += CLUSTERS.by_name(c).names
                df_creators = db.read_clips_creators_df_from_db(self.creators)
                self.creators += df_creators["creator"].unique().tolist()
            if args.creators: 
                df_creators = db.read_clips_creators_df_from_db(args.creators)
                self.creators += df_creators["creator"].unique().tolist()
            if args.categories:
                df_categories = db.read_clips_categories_df_from_db(args.categories)
                self.creators += df_categories["creator"].unique().tolist()
            if args.clip_ids:
                urls = [f'https://clips.twitch.tv/{clip_id}' for clip_id in args.clip_ids]
                df_clip_ids = db.read_clips_clip_urls_df_from_db(urls)
                self.creators += df_clip_ids["creator"].unique().tolist()
            if args.clip_urls:
                df_clip_ids = db.read_clips_clip_urls_df_from_db(args.clip_urls)
                self.creators += df_clip_ids["creator"].unique().tolist()
            if args.game_ids:
                df_game_ids = db.read_clips_categories_by_id_df_from_db(args.game_ids)
                self.creators += df_game_ids["creator"].unique().tolist()
            db.close()
            self.creators = list(set(self.creators))
            return pd.concat([
                df_creators, df_clusters, df_categories,
                df_clip_ids, df_game_ids
                ]).drop_duplicates().reset_index(drop=True)
        def discard_invalid_clips(df, args):
            def _date_n_days_ago(days: str ='7') -> str:
                days = int(days)
                today = datetime.date.today()
                date = today - relativedelta(days=days)
                return str(date.isoformat())
            if not args.published_ok:
                # Only keep clips that have not been published
                df = df[df['published']==0]
            # Ignore broken clips
            df = df[df['broken']==0]
            # Filter lang
            df = df[df['language']==args.lang]
            # Only keep clips between args.days and now
            df = df[df['created_at']>=_date_n_days_ago(days=args.days)]
            return df
        df = read_clips_from_db(args)
        df = discard_invalid_clips(df, args)
        df = df.sort_values(by=['view_count','duration'], ascending=False) 
        return df
    

    def load_compilation(self, args, compilation_with_errors: Compilation):
        # Remove elements from compilation if no longer present on disk
        # Rename files from elements if wrong order ID
        compilation_with_errors.sync_compilation_with_disk()
        def _handle_errors(errors):
            db = Mydb()
            for e in errors:
                url = e.clip.url
                db.set_broken(url)
                print(f"Set broken clip:\n\t{e.clip.to_string()}")
            db.commit()
            db.close()
            for e in errors:
                e.remove_from_disk()
        # Setup where we left off
        # Update DB with existing compilation
        errors = [e for e in compilation_with_errors if e.error]
        _handle_errors(errors)
        # Sort compilation_with_errors
        compilation_without_errors = [e for e in compilation_with_errors if not e.error]
        sorted_compilation_without_errors = sorted(compilation_without_errors, key=lambda e: e.order)
        self.clips = [e.clip for e in sorted_compilation_without_errors]
        self.duration = sum([c.duration for c in self.clips])
        # Read clips from db
        self.df = self._read_clips_from_db(args)

    def select_and_add_clips(self, args):
        while self.duration <= int(args.duration):
            self.prompt_choices_add_clip()
        return self.clips

    def remove_selected_clip(self, choice: Clip):
        self.duration -= int(choice.duration)
        self.clips.remove(choice)
        self.clips_removed.append(choice)

    def swap_selected_clips_index(self, idx0: int, idx1: int):
        self.clips[idx0], self.clips[idx1] = self.clips[idx1], self.clips[idx0]

    def add_selected_clip(self, choice: Clip, position: int = -1):
        if position == -1:
            self.clips.append(choice)
        else:
            self.clips.insert(position, choice)
        self.duration += int(choice.duration)

    def edit_clips(self, args):
        def _print_clips(clips):
            print('\n')
            for i, clip in enumerate(clips):
                print(f'{i+1:03d} {clip.to_string()}')
        _print_clips(self.clips)
        print(f'Total Duration: {int(self.duration)}')
        self.prompt_choices_edit_compilation()

    def _choices_str(self, choices):
        return [f'{i+1:03d}-{c.to_string()}' for i,c in enumerate(choices)]

    def prompt_choices_swap_clips(self):
        def _gen_choices(self) -> list:
            self.choices = self.clips[:]
            self.choices_str = self._choices_str(self.choices)
            return self.choices_str
        choices = _gen_choices(self)
        questions = [
            {
                'type': 'checkbox',
                'qmark': '😃',
                'message': 'Select clips to swap (2)',
                'name': 'swap',
                'choices': choices
            }
        ]
        answers = prompt(questions)['swap']
        idx0 = self.choices_str.index(answers[0])
        idx1 = self.choices_str.index(answers[1])
        self.swap_selected_clips_index(idx0, idx1)

    def prompt_choices_replace_clips(self):
        def _gen_choices(self) -> list:
            self.choices = self.clips[:]
            self.choices_str = self._choices_str(self.choices)
            return self.choices_str
        choices = _gen_choices(self)
        questions = [
            {
                'type': 'checkbox',
                'qmark': '😃',
                'message': 'Select clips to replace',
                'name': 'replace',
                'choices': choices
            }
        ]
        answers = prompt(questions)['replace']
        for answer in answers:
            idx = self.choices_str.index(answer)
            clip = self.choices[idx]
            self.remove_selected_clip(clip)
        for answer in answers:
            self.prompt_choices_add_clip()


    def prompt_choices_remove_clips(self):
        def _gen_choices(self) -> list:
            self.choices = self.clips[:]
            self.choices_str = self._choices_str(self.choices)
            return self.choices_str
        choices = _gen_choices(self)
        questions = [
            {
                'type': 'checkbox',
                'qmark': '😃',
                'message': 'Select clips to remove',
                'name': 'remove',
                'choices': choices
            }
        ]
        answers = prompt(questions)['remove']
        for answer in answers:
            idx = self.choices_str.index(answer)
            clip = self.choices[idx]
            self.remove_selected_clip(clip)

    def prompt_choices_edit_compilation(self):
        self.commands = ['add', 'swap', 'replace', 'remove', 'quit']
        def _gen_choices(self) -> list:
            return self.commands
        choices = _gen_choices(self)
        questions = [
            {
                'type': 'list',
                'name': 'edit',
                'message': 'Add/Swap/Remove',
                'choices': choices,
            },
        ]
        answer = prompt(questions)['edit']
        def parse_answer_from_command(self, cmd) -> str:
            def add(self) -> str:
                self.prompt_choices_add_clip()
            def swap(self) -> str:
                self.prompt_choices_swap_clips()
            def remove(self) -> str:
                self.prompt_choices_remove_clips()
            def replace(self) -> str:
                self.prompt_choices_replace_clips()
            # Custom commands to select answer for us
            if cmd == 'add':
                answer = add(self)
            elif cmd == 'swap':
                answer = swap(self)
            elif cmd == 'remove':
                answer = remove(self)
            elif cmd == 'replace':
                answer = replace(self)
            elif cmd == 'quit':
                return
            return answer
        if answer in self.commands:
            answer = parse_answer_from_command(self, answer)

    def prompt_choices_add_clip(self):
        self.commands = ['pick_max_view', 'pick_low_duration', 'pick_low_n']
        def _update_nclips_viewtime(self):
            for c in self.creators:
                self.nclips[c] = sum([x.creator == c for x in self.clips])
                self.viewtime[c] = sum(int(x.duration) if x.creator == c else 0 for x in self.clips)
            self.choices_creators_names = [c.creator.name for c in self.choices]
            for c in self.creators:
                if c not in self.choices_creators_names:
                    del self.nclips[c]
                    del self.viewtime[c]
        def _status_text(self) -> str:
            status_str = [f'duration: {self.duration}']
            for c in self.choices_creators_names:
                status_str.append(f"{c}:{self.nclips[c]} {self.viewtime[c]}s")
            return ';'.join(status_str)
        def _gen_choices(self) -> list:
            choices = []
            count = {}
            for x in self.creators:
                count[x] = 0
            max = 1
            for _, row in self.df.iterrows():
                if count[row.creator] >= max:
                    continue
                url = row['url']
                if url in [x.url for x in self.clips]:
                    continue
                choice_clip = Clip(from_row=True,row=row)
                if choice_clip in self.clips_removed:
                    continue
                choices.append(choice_clip)
                count[row.creator] += 1
            self.choices = choices
            self.choices_str = self._choices_str(choices)
            _update_nclips_viewtime(self)
            return self.commands + self.choices_str
        choices = _gen_choices(self)
        questions = [
            {
                'type': 'list',
                'name': 'clips',
                'message': 'Select {}'.format(_status_text(self)),
                'choices': choices,
            },
        ]
        answer = prompt(questions)['clips']
        def parse_answer_from_command(self, cmd) -> str:
            def pick_low_n(self) -> str:
                creator = min(self.nclips, key=self.nclips.get)
                for x in self.choices:
                    if x.creator.name == creator:
                        return x
            def pick_low_duration(self) -> str:
                creator = min(self.viewtime, key=self.viewtime.get)
                for x in self.choices:
                    if x.creator.name == creator:
                        return x
            def pick_max_views(self) -> str:
                max, maxc = 0, None
                for c in self.choices:
                    views = int(c.view_count) 
                    if views > max:
                        maxc, max = c, views 
                return maxc
            # Custom commands to select answer for us
            if cmd == 'pick_low_n':
                clip = pick_low_n(self)
            elif cmd == 'pick_low_duration':
                clip = pick_low_duration(self)
            elif cmd == 'pick_max_view':
                clip = pick_max_views(self)
            return clip
        if answer in self.commands:
            clip = parse_answer_from_command(self, answer)
            self.add_selected_clip(clip)
        else:
            idx = self.choices_str.index(answer)
            clip = self.choices[idx]
            self.add_selected_clip(clip)

def select_compilation_from_db(args):
    sh = ClipsSelector(args)
    if args.console:
        sh.select_and_add_clips(args)
        # Write to url.txt
        compilation = Compilation(wd=args.wd, clips=sh.clips, project=args.project)
    else:
        # Save choices to clips.json
        clips_json = sh.df.reset_index().to_json(orient='index')
        file = Path('./clips.json')
        with file.open('w') as f:
            f.write(clips_json)
        # Clear compilation.json
        file = Path('./compilation.json')
        if file.exists():
            file.unlink()
        # Wait for GUI edit
        subprocess.call([
            './gui.AppImage',
        ])
        is_prompt_confirm('Read compilation.csv')
        # Read URLs from CSV in a txt file. Then read from DB
        file = Path('./compilation.csv')
        urls = file.read_text().strip().split(',')
        db = Mydb()
        df = db.read_clips_clip_urls_df_from_db(urls)
        db.close()
        # df is not ordered like csv
        clips = []
        for url in urls:
            result = df[df['url'] == url].iloc[0]
            clips.append(Clip(from_row=True,row=result))
        compilation = Compilation(wd=args.wd, clips=clips, project=args.project)
    print(compilation.to_string())
    compilation.sync_compilation_with_disk()
    compilation.dump(args.wd)

def load_compilation_from_published_project(args):
    sh = ClipsSelector(args)
    args.days = 9999
    df = sh._read_clips_from_db(args) # Also discards clips args.published_ok
    # df is not ordered as args.clip_urls
    clips = []
    # Sort clips by order in args.clip_urls
    for url in args.clip_urls:
        try:
            result = df[df['url'] == url].iloc[0]
        except IndexError:
            print(f'URL no longer present in DB:\n\t{url}')
            continue
        clips.append(Clip(from_row=True,row=result))
    compilation = Compilation(wd=args.wd, clips=clips, project=args.project)
    print(compilation.to_string())
    compilation.dump(args.wd)

def edit_compilation(args):
    sh = ClipsSelector(args)
    compilation = Compilation.load(args.wd)
    sh.load_compilation(args, compilation)
    if args.console:
        sh.edit_clips(args)
        while is_prompt_confirm('Continue Edit clips'):
            sh.edit_clips(args)
        compilation = Compilation(wd=args.wd, clips=sh.clips, project=args.project)
    else:
        # Save choices to clips.json
        clips_json = sh.df.reset_index().to_json(orient='index')
        file = Path('./clips.json')
        # Wait for GUI edit
        is_prompt_confirm('Save compilation.json')
        with file.open('w') as f:
            f.write(clips_json)
        # Save compilations to compilation.json
        try:
            compilation_json = compilation.to_json()
            file = Path('./compilation.json')
            with file.open('w') as f:
                f.write(compilation_json)
        except TypeError as e:
            print("Error saving JSON")
            print(e)
        # Wait for GUI edit
        subprocess.call([
            './gui.AppImage', 
        ])
        is_prompt_confirm('Read compilation.csv')
        # Read URLs from CSV in a txt file. Then read from DB
        file = Path('./compilation.csv')
        urls = file.read_text().strip().split(',')
        db = Mydb()
        df = db.read_clips_clip_urls_df_from_db(urls)
        db.close()
        # df is not ordered like csv
        clips = []
        for url in urls:
            result = df[df['url'] == url].iloc[0]
            clips.append(Clip(from_row=True,row=result))
        compilation = Compilation(wd=args.wd, clips=clips, project=args.project)
    print(compilation.to_string())
    compilation.sync_compilation_with_disk()
    compilation.dump(args.wd)

def is_prompt_confirm(step: str):
    questions = [
        {
            'type': 'confirm',
            'message': f'Do you want to {step}?',
            'name': 'confirm',
            'default': True,
        },
    ]
    answers = prompt(questions)
    return answers['confirm']