%def head():
    <link rel="stylesheet" href="/static/movie.css" />
    <script src="/static/controls.js"></script>
%end

%rebase master title=item["title"], head=head

<h1>{{item["title"]}}</h1>
%if item['image'] is not None:
  <img id="cover" src="{{item['image']}}" alt="{{item['title']}}" width="125px" />
%end if
<p class="summary hyphenate">
  {{item["description"]}} <span class="duration">{{item["duration"]}}</span>
</p>

<div id="rating">
%if item["rating"] is not None:
  %for i in range(item["rating"]):
    <img src="/static/heart.png" height="24px" alt="*" />
  %end for
  %for i in range(item["rating"], 5):
    <img src="/static/noheart.png" height="24px" alt="." />
  %end for
%end if
</div>

%include controls hosts=hosts, heg=heg, is_playing=is_playing
