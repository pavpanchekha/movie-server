%def head():
    <link rel="stylesheet" href="/static/movie.css" />
    <script src="/static/controls.js"></script>
%end

%rebase master title=item["title"], head=head

<div id="cover">
%if item['image'] is not None:
  <img src="{{item['image']}}" alt="{{item['title']}}" width="125px" />
%end if
  <div id="rating">
    %include stars rating=item["rating"]
  </div>
</div>
<h2>{{item["title"]}}</h2>
<p class="summary hyphenate">
  {{item["description"]}} <span class="duration">{{item["duration"]}}</span>
</p>


%include controls hosts=hosts, heg=heg, is_playing=is_playing, mod="playlist", name=name
