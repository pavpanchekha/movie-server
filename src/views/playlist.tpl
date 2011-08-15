%def head():
    <link rel="stylesheet" href="/static/playlist.css" />
    <script src="/static/controls.js"></script>
    <script src="/static/playlist.js"></script>
%end

%rebase master title=item["title"], head=head

<h1>{{item["title"]}}</h1>
<form method="post" action="/">
  <input type="hidden" name="action" value="skip" />
  <ol start="{{item['position']}}">
  %for id, song in item["songs"]:
    %if id + 1 == item["position"]:
      <li id="song{{id}}" class="active"><button class="song" name="position" value="{{id}}">{{song}}</button></li>
    %else:
      <li id="song{{id}}"><button class="song" name="position" value="{{id}}">{{song}}</button></li>
    %end if
  %end for
  </ol>
</form>

%include controls hosts=hosts, heg=heg, is_playing=is_playing
